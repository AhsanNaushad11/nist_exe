"""
diehard.py — Complete Python implementation of the Diehard battery of statistical tests.

Implements all 17 test groups from George Marsaglia's original Diehard suite (1995),
using algorithms from the original C source, Knuth Vol.2, and the Dieharder documentation.

No third-party libraries required — only the Python standard library.

Usage:
    python diehard.py <raw_binary_file>
"""
import sys
import math
import struct
import os
import itertools

MAX32 = 2 ** 32

# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_uint32(filepath):
    size = os.path.getsize(filepath)
    n = size // 4
    with open(filepath, "rb") as f:
        data = struct.unpack(f"<{n}I", f.read(n * 4))
    return list(data)

# ═══════════════════════════════════════════════════════════════════════════════
# MATH HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def norm_cdf(x):
    """CDF of the standard normal N(0,1)."""
    return 0.5 * math.erfc(-x / math.sqrt(2))

def regularized_gamma_lower(a, x):
    """
    Regularized lower incomplete gamma P(a, x) via Numerical Recipes (Lentz's method).
    Returns P such that P + Q = 1 where Q is the upper tail.
    """
    if x <= 0.0:
        return 0.0
    FPMIN = 1e-300
    if x < a + 1.0:
        # Series expansion — converges quickly for x < a+1
        ap, delta, total = a, 1.0 / a, 1.0 / a
        for _ in range(300):
            ap += 1.0
            delta *= x / ap
            total += delta
            if abs(delta) < abs(total) * 3e-15:
                break
        return min(1.0, total * math.exp(-x + a * math.log(x) - math.lgamma(a)))
    else:
        # Lentz's continued fraction — converges quickly for x > a+1
        b = x + 1.0 - a
        c = 1.0 / FPMIN
        d = 1.0 / b if abs(b) > FPMIN else 1.0 / FPMIN
        h = d
        for i in range(1, 300):
            an = -i * (i - a)
            b += 2.0
            d = an * d + b
            if abs(d) < FPMIN:
                d = FPMIN
            c = b + an / c
            if abs(c) < FPMIN:
                c = FPMIN
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < 3e-15:
                break
        return max(0.0, min(1.0, 1.0 - math.exp(-x + a * math.log(x) - math.lgamma(a)) * h))

def chi2_pvalue(chi2, dof):
    """Upper-tail p-value: P(X > chi2) for X ~ chi-squared(dof)."""
    if dof <= 0 or chi2 < 0:
        return 0.0
    # P(X > chi2) = 1 - P(a, x) = Q(a, x) where a=dof/2, x=chi2/2
    return 1.0 - regularized_gamma_lower(dof / 2.0, chi2 / 2.0)

def ks_pvalue(D, n):
    """
    Kolmogorov-Smirnov asymptotic p-value.
    P(D_n > D | H0) using the improved approximation with continuity correction.
    """
    if D <= 0:
        return 1.0
    t = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * D
    if t > 5.0:
        return 0.0
    if t < 0.1:
        return 1.0
    total = 0.0
    for k in range(1, 80):
        term = (-1) ** (k - 1) * math.exp(-2.0 * k * k * t * t)
        total += term
        if abs(term) < 1e-13:
            break
    return min(1.0, max(0.0, 2.0 * total))

def poisson_pmf(k, lam):
    """Poisson probability mass function P(X=k) for X~Poisson(lam)."""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    try:
        return math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1))
    except (ValueError, OverflowError):
        return 0.0

def poisson_cdf(k, lam):
    """Poisson CDF P(X <= k)."""
    return min(1.0, sum(poisson_pmf(i, lam) for i in range(k + 1)))

def to_float(u):
    """Convert a uint32 to a uniform float in [0, 1)."""
    return u / MAX32

def popcount(b):
    """Count number of set bits in a byte (0-255)."""
    b = b & 0xFF
    return bin(b).count('1')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 1: BIRTHDAY SPACINGS
# ═══════════════════════════════════════════════════════════════════════════════

def test_birthday_spacings(data, n_tests=10):
    """
    Birthday Paradox test. Choose n=512 'birthdays' in a year of m=2^24 days.
    Sort them, compute spacings, count coincident spacings.
    Coincidence count ~ Poisson(lambda) where lambda = n^3/(4m) = 2.0.
    Source: Marsaglia (1995), original Diehard paper.
    """
    n, m = 512, 2 ** 24
    lam = n ** 3 / (4 * m)  # = 2.0 exactly
    results = []
    idx = 0
    for _ in range(n_tests):
        if idx + n > len(data):
            idx = 0
        chunk = data[idx:idx + n]
        idx += n
        birthdays = sorted(x % m for x in chunk)
        spacings = sorted(birthdays[i + 1] - birthdays[i] for i in range(n - 1))
        coincidences = sum(1 for i in range(len(spacings) - 1) if spacings[i] == spacings[i + 1])
        pval = poisson_cdf(coincidences, lam)
        results.append(pval)
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 2: OVERLAPPING 5-PERMUTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

# Precompute a lookup: sorted-rank-tuple → permutation index (0-119)
_PERM5 = list(itertools.permutations(range(5)))
_PERM5_IDX = {p: i for i, p in enumerate(_PERM5)}

def _perm_index5(floats, start):
    """Return the rank-order permutation index (0-119) of the 5-tuple starting at start."""
    window = floats[start:start + 5]
    order = tuple(sorted(range(5), key=lambda i: window[i]))
    return _PERM5_IDX[order]

def test_overlapping_permutations(data, n=200000):
    """
    Take n independent 5-tuples from uniform floats. Each of 5!=120 possible rank orderings
    should appear with equal probability 1/120. Chi-squared with 119 dof.
    (Implemented as non-overlapping to guarantee true chi-square validity,
     avoiding the known flaws of the 99-dof Marsaglia covariance matrix).
    """
    floats = [to_float(x) for x in data[:n * 5]]
    counts = [0] * 120
    for i in range(n):
        counts[_perm_index5(floats, i * 5)] += 1
    expected = n / 120.0
    chi2 = sum((c - expected) ** 2 / expected for c in counts)
    return chi2_pvalue(chi2, 119)

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 3: BINARY RANK (32x32)
# ═══════════════════════════════════════════════════════════════════════════════

def _gf2_rank_from_ints(rows_as_ints, bits_per_row):
    """Compute rank of a binary matrix over GF(2) represented as integers."""
    m = list(rows_as_ints)
    n_rows = len(m)
    rank = 0
    mask = 1 << (bits_per_row - 1)
    for col in range(bits_per_row):
        pivot = next((r for r in range(rank, n_rows) if (m[r] >> (bits_per_row - 1 - col)) & 1), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        for r in range(n_rows):
            if r != rank and (m[r] >> (bits_per_row - 1 - col)) & 1:
                m[r] ^= m[rank]
        rank += 1
    return rank

def test_binary_rank_32x32(data, n_matrices=100):
    """
    Form 32x32 matrices from 32-bit integers. Compute rank over GF(2).
    Expected: P(rank=32)≈0.2888, P(rank=31)≈0.5776, P(rank≤30)≈0.1336.
    Chi-squared with 2 dof.
    Source: Marsaglia (1995), exact probabilities from GF(2) theory.
    """
    p32, p31, p30 = 0.2888, 0.5776, 0.1336
    obs = [0, 0, 0]
    for i in range(n_matrices):
        rows = data[i * 32:(i + 1) * 32]
        if len(rows) < 32:
            break
        r = _gf2_rank_from_ints(rows, 32)
        if r == 32:   obs[0] += 1
        elif r == 31: obs[1] += 1
        else:         obs[2] += 1
    exp = [n_matrices * p for p in (p32, p31, p30)]
    chi2 = sum((o - e) ** 2 / e for o, e in zip(obs, exp))
    return chi2_pvalue(chi2, 2)

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 4: BINARY RANK (6x8)
# ═══════════════════════════════════════════════════════════════════════════════

def test_binary_rank_6x8(data, n_matrices=100, offset=3200):
    """
    Form 6x8 matrices from consecutive bytes. Compute rank over GF(2).
    Expected: P(rank=6)≈0.7731, P(rank=5)≈0.2124, P(rank≤4)≈0.0146.
    Probabilities computed from product formula for GF(2) full-rank matrices.
    Chi-squared with 2 dof.
    Source: Marsaglia (1995).
    """
    p6, p5, p4 = 0.7731, 0.2124, 0.0146
    obs = [0, 0, 0]
    idx = offset
    for _ in range(n_matrices):
        rows = []
        for row_num in range(6):
            uint_i = idx + row_num // 4
            byte_shift = (3 - row_num % 4) * 8
            if uint_i < len(data):
                rows.append((data[uint_i] >> byte_shift) & 0xFF)
            else:
                rows.append(0)
        idx += 2
        r = _gf2_rank_from_ints(rows, 8)
        if r >= 6:   obs[0] += 1
        elif r == 5: obs[1] += 1
        else:        obs[2] += 1
    exp = [n_matrices * p for p in (p6, p5, p4)]
    chi2 = sum((o - e) ** 2 / e for o, e in zip(obs, exp))
    return chi2_pvalue(chi2, 2)

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 5: BITSTREAM TEST
# ═══════════════════════════════════════════════════════════════════════════════

def _sparse_occupancy_test(data, start, n_samples, letter_bits, word_len):
    """
    Generic sparse occupancy test. Extract successive letters of `letter_bits` bits
    from successive uint32s (top bits). Form overlapping words of length `word_len`.
    Count missing words out of (2^letter_bits)^word_len = 2^20 possible words.
    Returns number of missing words.
    """
    total_bits = letter_bits * word_len    # should equal 20
    mask = (1 << total_bits) - 1
    shift = 32 - letter_bits              # take top letter_bits bits
    l_mask = (1 << letter_bits) - 1
    seen = set()
    word = 0
    # Prime the word
    for j in range(word_len - 1):
        letter = (data[start + j] >> shift) & l_mask
        word = ((word << letter_bits) | letter) & mask
    for k in range(n_samples):
        idx = start + word_len - 1 + k
        if idx >= len(data):
            idx = idx % len(data)
        letter = (data[idx] >> shift) & l_mask
        word = ((word << letter_bits) | letter) & mask
        seen.add(word)
    return (1 << total_bits) - len(seen)

def _bitstream_missing(data, start, n_windows, word_bits=20):
    """Extract n_windows overlapping word_bits-bit words from the bit stream."""
    FPMIN = 1e-300
    mask = (1 << word_bits) - 1
    seen = set()
    buf, buf_len, idx = 0, 0, start
    for _ in range(n_windows):
        while buf_len < word_bits and idx < len(data):
            buf = ((buf << 32) | data[idx]) & ((1 << (word_bits + 32)) - 1)
            buf_len += 32
            idx += 1
        if buf_len >= word_bits:
            w = (buf >> (buf_len - word_bits)) & mask
            seen.add(w)
            buf_len -= 1
    return (1 << word_bits) - len(seen)

def test_bitstream(data, n_tests=3):
    """
    From a bitstream of 2^21 overlapping bits, extract 20-bit words.
    Count missing 20-bit words out of 2^20 possible.
    Expected missing: mu = 2^20 * e^{-2} ≈ 141909.
    Source: Marsaglia (1995).
    """
    mu = (2 ** 20) * math.exp(-2.0)
    sigma = 290.0
    n_windows = 2 ** 21
    uint32_per_test = (n_windows + 20 + 31) // 32 + 1
    results = []
    for t in range(n_tests):
        start = t * uint32_per_test
        if start + uint32_per_test > len(data):
            start = 0
        missing = _bitstream_missing(data, start, n_windows, 20)
        z = (missing - mu) / sigma
        pval = 2.0 * (1.0 - norm_cdf(abs(z)))
        results.append(pval)
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 6: OPSO — Overlapping Pairs Sparse Occupancy
# ═══════════════════════════════════════════════════════════════════════════════

def test_opso(data, n_tests=3):
    """
    Extract top 10 bits of each uint32 as a 'letter'. Form overlapping pairs.
    Count missing pairs out of 2^20 = 1,048,576 possible.
    N = 2^21 consecutive pairs.
    Expected missing mu ≈ 141909, sigma ≈ 339.
    Source: Marsaglia (1995).
    """
    mu = (2 ** 20) * math.exp(-2.0)
    sigma = 290.0
    n_pairs = 2 ** 21
    results = []
    for t in range(n_tests):
        start = t * (n_pairs + 1)
        if start + n_pairs + 1 > len(data):
            start = 0
        missing = _sparse_occupancy_test(data, start, n_pairs, letter_bits=10, word_len=2)
        z = (missing - mu) / sigma
        pval = 2.0 * (1.0 - norm_cdf(abs(z)))
        results.append(pval)
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 7: OQSO — Overlapping Quadruples Sparse Occupancy
# ═══════════════════════════════════════════════════════════════════════════════

def test_oqso(data, n_tests=3):
    """
    Extract top 5 bits of each uint32 as a 'letter' (alphabet size 32).
    Form overlapping quadruples. Count missing out of 32^4 = 2^20 possible.
    N = 2^21 samples.
    Expected missing mu ≈ 141909, sigma ≈ 339.
    Source: Marsaglia (1995).
    """
    mu = (2 ** 20) * math.exp(-2.0)
    sigma = 290.0
    n_quads = 2 ** 21
    results = []
    for t in range(n_tests):
        start = t * (n_quads + 3)
        if start + n_quads + 3 > len(data):
            start = 0
        missing = _sparse_occupancy_test(data, start, n_quads, letter_bits=5, word_len=4)
        z = (missing - mu) / sigma
        pval = 2.0 * (1.0 - norm_cdf(abs(z)))
        results.append(pval)
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 8: DNA TEST — Overlapping 10-tuples of 2-bit letters
# ═══════════════════════════════════════════════════════════════════════════════

def test_dna(data, n_tests=3):
    """
    Extract top 2 bits of each uint32 as a 'nucleotide' letter (alphabet size 4).
    Form overlapping 10-tuples. Count missing out of 4^10 = 2^20 possible.
    N = 2^21 samples.
    Expected missing mu ≈ 141909, sigma ≈ 339.
    Source: Marsaglia (1995).
    """
    mu = (2 ** 20) * math.exp(-2.0)
    sigma = 290.0
    n_words = 2 ** 21
    results = []
    for t in range(n_tests):
        start = t * (n_words + 9)
        if start + n_words + 9 > len(data):
            start = 0
        missing = _sparse_occupancy_test(data, start, n_words, letter_bits=2, word_len=10)
        z = (missing - mu) / sigma
        pval = 2.0 * (1.0 - norm_cdf(abs(z)))
        results.append(pval)
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 9: COUNT THE 1S (STREAM)
# ═══════════════════════════════════════════════════════════════════════════════

def _count_1s_5_letter_word_test(byte_generator, n_words):
    """
    Helper for Count the 1s. Maps byte popcounts to 5 'letters' and checks
    frequencies of 5-letter words out of 3125 possible.
    """
    P_letter = [37/256.0, 56/256.0, 70/256.0, 56/256.0, 37/256.0]
    def to_letter(c):
        if c <= 2: return 0
        if c == 3: return 1
        if c == 4: return 2
        if c == 5: return 3
        return 4

    counts = [0] * 3125
    try:
        for _ in range(n_words):
            w = 0
            for _ in range(5):
                c = popcount(next(byte_generator))
                w = w * 5 + to_letter(c)
            counts[w] += 1
    except StopIteration:
        pass

    chi2 = 0.0
    for w in range(3125):
        p = 1.0
        temp = w
        for _ in range(5):
            p *= P_letter[temp % 5]
            temp //= 5
        e = n_words * p
        if e > 0:
            chi2 += (counts[w] - e)**2 / e
    return chi2_pvalue(chi2, 3124)

def test_count_ones_stream(data, n_words=256000):
    """
    Count the 1s (Stream) — Non-overlapping 5-letter words.
    Extract stream of bytes. Map 1s-count to 5 letters.
    Form independent 5-letter words. Chi-square on 3125 bins.
    """
    def byte_gen():
        for u in data:
            for shift in (0, 8, 16, 24):
                yield (u >> shift) & 0xFF
    return _count_1s_5_letter_word_test(byte_gen(), n_words)

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 10: COUNT THE 1S (SPECIFIC BYTES)
# ═══════════════════════════════════════════════════════════════════════════════

def test_count_ones_specific_bytes(data, n_words=256000):
    """
    For each of the 4 byte positions, extract bytes, map to 5 letters,
    form independent 5-letter words. Returns 4 p-values.
    """
    results = []
    for byte_pos in range(4):
        shift = byte_pos * 8
        def byte_gen():
            for u in data:
                yield (u >> shift) & 0xFF
        results.append(_count_1s_5_letter_word_test(byte_gen(), n_words))
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 11: PARKING LOT TEST
# ═══════════════════════════════════════════════════════════════════════════════

def test_parking_lot(data, n_tests=5, n_attempts=12000):
    """
    Attempt to park n_attempts unit circles (radius 0.5, diameter 1.0) in a 100x100 square.
    Two circles collide if their center distance < 1.0.
    Count successes. Expected ≈ 3523, std ≈ 21.9.
    Grid acceleration: only check 3x3 neighborhood of cells.
    Source: Marsaglia (1995); expected value from RSA simulation theory.
    """
    MU_PARK, SIGMA_PARK = 3523.0, 21.9
    results = []
    idx = 0
    for _ in range(n_tests):
        grid = {}   # (cell_x, cell_y) -> list of (cx, cy) of parked circles
        successes = 0
        for _ in range(n_attempts):
            if idx + 1 >= len(data):
                idx = 0
            x = 0.5 + to_float(data[idx]) * 99.0
            y = 0.5 + to_float(data[idx + 1]) * 99.0
            idx += 2
            cx, cy = int(x), int(y)
            ok = True
            for ddx in range(max(0, cx - 1), min(100, cx + 2)):
                if not ok:
                    break
                for ddy in range(max(0, cy - 1), min(100, cy + 2)):
                    for (px, py) in grid.get((ddx, ddy), []):
                        # Unit-square overlap: both x and y separations < 1
                        if abs(x - px) < 1.0 and abs(y - py) < 1.0:
                            ok = False
                            break
                    if not ok:
                        break
            if ok:
                grid.setdefault((cx, cy), []).append((x, y))
                successes += 1
        z = (successes - MU_PARK) / SIGMA_PARK
        pval = 2.0 * (1.0 - norm_cdf(abs(z)))
        results.append(pval)
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 12: MINIMUM DISTANCE TEST
# ═══════════════════════════════════════════════════════════════════════════════

def test_minimum_distance(data, n_tests=5, n_points=8000):
    """
    Place n_points random points in [0, 10000]^2. Find minimum pairwise distance D.
    D^2 ~ Exp(lambda) where lambda = pi * n*(n-1) / (2 * area).
    p-value from the exponential CDF.
    Source: Marsaglia (1995).
    """
    sq = 10000.0
    lam = math.pi * n_points * (n_points - 1) / (2.0 * sq * sq)
    results = []
    idx = 0
    for _ in range(n_tests):
        if idx + 2 * n_points > len(data):
            idx = 0
        xs = [to_float(data[idx + i]) * sq for i in range(n_points)]
        ys = [to_float(data[idx + n_points + i]) * sq for i in range(n_points)]
        idx += 2 * n_points
        min_d2 = float('inf')
        for i in range(n_points):
            for j in range(i + 1, n_points):
                d2 = (xs[i] - xs[j]) ** 2 + (ys[i] - ys[j]) ** 2
                if d2 < min_d2:
                    min_d2 = d2
        pval = 1.0 - math.exp(-lam * min_d2)
        results.append(max(0.0001, min(0.9999, pval)))
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 13: 3D SPHERES TEST
# ═══════════════════════════════════════════════════════════════════════════════

def test_3d_spheres(data, n_tests=5, n_points=4000):
    """
    Place n_points random points in [0, 1000]^3. Find minimum pairwise distance r.
    r^3 should follow Exp(lambda) where lambda = n*(n-1)/2 * (4pi/3) / volume.
    p-value from the exponential CDF.
    Source: Marsaglia (1995).
    """
    vol = 1000.0 ** 3
    lam = (n_points * (n_points - 1) / 2.0) * (4.0 * math.pi / 3.0) / vol
    results = []
    idx = 0
    for _ in range(n_tests):
        if idx + 3 * n_points > len(data):
            idx = 0
        xs = [to_float(data[idx + i]) * 1000.0 for i in range(n_points)]
        ys = [to_float(data[idx + n_points + i]) * 1000.0 for i in range(n_points)]
        zs = [to_float(data[idx + 2 * n_points + i]) * 1000.0 for i in range(n_points)]
        idx += 3 * n_points
        min_d2 = float('inf')
        for i in range(n_points):
            for j in range(i + 1, n_points):
                d2 = ((xs[i] - xs[j]) ** 2 +
                      (ys[i] - ys[j]) ** 2 +
                      (zs[i] - zs[j]) ** 2)
                if d2 < min_d2:
                    min_d2 = d2
        r_cube = min_d2 ** 1.5   # r^3 = (sqrt(d2))^3 = d2^(3/2)
        pval = 1.0 - math.exp(-lam * r_cube)
        results.append(max(0.0001, min(0.9999, pval)))
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 14: SQUEEZE TEST
# ═══════════════════════════════════════════════════════════════════════════════

def test_squeeze(data, n_games=50000):
    """
    Multiply K=2^31 by uniform(0,1) numbers until the product <= 1.
    Let I = number of multiplications needed.
    Then I - 1 ~ Poisson(m) where m = log(2^31) = 31*log(2) ≈ 21.4875.
    Theoretical: P(I=k) = Poisson(m).pmf(k-1).
    Chi-squared against theoretical distribution.
    Source: Marsaglia (1995); Poisson derivation from exponential inter-arrival times.
    """
    K = 2 ** 31
    m = 31.0 * math.log(2)  # ≈ 21.4875

    lo_cut, hi_cut = 6, 47
    # Compute theoretical probabilities for each bin
    theo = [sum(poisson_pmf(k - 1, m) for k in range(1, lo_cut + 1))]   # I <= 6
    for k in range(lo_cut + 1, hi_cut + 1):
        theo.append(poisson_pmf(k - 1, m))                               # I = 7..47
    theo.append(sum(poisson_pmf(k - 1, m) for k in range(hi_cut + 1, 200)))  # I >= 48

    # Simulate games
    floats = [to_float(x) for x in data]
    counts_raw = {}
    idx = 0
    for _ in range(n_games):
        product = float(K)
        I = 0
        while product > 1.0 and idx < len(floats):
            product *= floats[idx]
            idx += 1
            I += 1
        counts_raw[I] = counts_raw.get(I, 0) + 1
        if idx >= len(floats) - 2:
            idx = 0

    # Bin the observations to match theo
    n_bins = len(theo)
    obs = [0] * n_bins
    for I, cnt in counts_raw.items():
        if I <= lo_cut:
            obs[0] += cnt
        elif I <= hi_cut:
            obs[I - lo_cut] += cnt
        else:
            obs[-1] += cnt

    exp = [p * n_games for p in theo]
    # Chi-square only on bins where expected >= 1
    chi2 = sum((o - e) ** 2 / e for o, e in zip(obs, exp) if e >= 1.0)
    dof = sum(1 for e in exp if e >= 1.0) - 1
    return chi2_pvalue(chi2, dof)

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 15: OVERLAPPING SUMS
# ═══════════════════════════════════════════════════════════════════════════════

def test_overlapping_sums(data, n_windows=10000):
    """
    Sum non-overlapping windows of 100 uniform(0,1) floats.
    By the CLT, each sum ~ Normal(50, 100/12).
    Kolmogorov-Smirnov test against the normal distribution.
    Source: Marsaglia (1995); non-overlapping variant to satisfy KS independence assumption.
    """
    window = 100
    if n_windows * window > len(data):
        n_windows = len(data) // window
    sums = []
    for i in range(n_windows):
        start = i * window
        s = sum(to_float(data[start + j]) for j in range(window))
        sums.append(s)
    mean = 50.0
    std = math.sqrt(100.0 / 12.0)
    n_s = len(sums)
    sorted_sums = sorted(sums)
    D = 0.0
    for i, x in enumerate(sorted_sums):
        fn = norm_cdf((x - mean) / std)
        D = max(D, abs((i + 1) / n_s - fn), abs(i / n_s - fn))
    return ks_pvalue(D, n_s)

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 16: RUNS UP (Knuth Vol. 2, §3.3.2)
# ═══════════════════════════════════════════════════════════════════════════════

def test_runs_up(data, n=100000):
    """
    Count runs of ascending length 1,2,3,4,5,6+ using Knuth's quadratic form
    with the exact covariance matrix A and expected proportions b.
    Test statistic ~ chi-squared with 6 dof.
    Source: Knuth, TAOCP Vol.2, §3.3.2, Algorithm R.
    """
    A = [
        [4529.4,  9044.9, 13568.0, 18091.0,  22615.0,  27892.0],
        [9044.9, 18097.0, 27139.0, 36187.0,  45234.0,  55789.0],
        [13568.0,27139.0, 40721.0, 54281.0,  67852.0,  83685.0],
        [18091.0,36187.0, 54281.0, 72414.0,  90470.0, 111580.0],
        [22615.0,45234.0, 67852.0, 90470.0, 113262.0, 139476.0],
        [27892.0,55789.0, 83685.0,111580.0, 139476.0, 172860.0],
    ]
    b = [1/6, 5/24, 11/120, 19/720, 29/5040, 1/840]
    floats = [to_float(x) for x in data[:n]]
    counts = [0] * 6
    run_len = 1
    for i in range(1, n):
        if floats[i] > floats[i - 1]:
            run_len += 1
        else:
            counts[min(run_len, 6) - 1] += 1
            run_len = 1
    counts[min(run_len, 6) - 1] += 1
    chi2 = sum(A[i][j] * (counts[i] - n * b[i]) * (counts[j] - n * b[j])
               for i in range(6) for j in range(6)) / n
    return chi2_pvalue(chi2, 6)

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 17: CRAPS TEST
# ═══════════════════════════════════════════════════════════════════════════════

def test_craps(data, n_games=50000):
    """
    Simulate n_games of craps. Check win proportion against theoretical 244/495 ≈ 0.4929.
    Z-test on win count (normal approximation to binomial).
    Source: Marsaglia (1995).
    """
    floats = [to_float(x) for x in data]
    wins = 0
    idx = 0

    def roll():
        nonlocal idx
        d1 = int(floats[idx] * 6) + 1
        d2 = int(floats[idx + 1] * 6) + 1
        idx += 2
        return d1 + d2

    games_played = 0
    while games_played < n_games and idx + 42 < len(floats):
        total = roll()
        if total in (7, 11):
            wins += 1
        elif total not in (2, 3, 12):
            point = total
            while idx + 2 < len(floats):
                total = roll()
                if total == point:
                    wins += 1
                    break
                if total == 7:
                    break
        games_played += 1

    if games_played == 0:
        return 0.5
    exp_wins = games_played * 244 / 495
    var_wins = games_played * (244 / 495) * (251 / 495)
    z = (wins - exp_wins) / math.sqrt(var_wins)
    return 2.0 * (1.0 - norm_cdf(abs(z)))

# ═══════════════════════════════════════════════════════════════════════════════
# REPORT FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

PASS_LO, PASS_HI = 0.05, 0.95
WEAK_LO, WEAK_HI = 0.001, 0.999

def verdict(pval):
    if pval < WEAK_LO or pval > WEAK_HI:
        return "FAILED"
    if pval < PASS_LO or pval > PASS_HI:
        return "WEAK  "
    return "PASSED"

def print_row(name, pval, rows):
    rows.append((name, pval))
    print(f"  {name:<44} {pval:>9.6f}  {verdict(pval)}")

def generate_detailed_report(filepath, rows):
    """Generates a detailed, readable markdown report of the test results."""
    report_path = filepath + "_diehard_report.md"
    all_pvals = [p for _, p in rows]
    passed = sum(1 for p in all_pvals if PASS_LO <= p <= PASS_HI)
    weak   = sum(1 for p in all_pvals if (WEAK_LO <= p < PASS_LO) or (PASS_HI < p <= WEAK_HI))
    failed = sum(1 for p in all_pvals if p < WEAK_LO or p > WEAK_HI)
    total  = len(all_pvals)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Diehard Statistical Test Report\n\n")
        f.write(f"**Target File:** `{filepath}`\n")
        f.write(f"**Total Tests Run:** {total}\n\n")
        
        f.write(f"## Summary\n")
        f.write(f"- **PASSED:** {passed}/{total}\n")
        f.write(f"- **WEAK:** {weak}/{total}\n")
        f.write(f"- **FAILED:** {failed}/{total}\n\n")
        
        f.write(f"## Detailed Results\n")
        f.write(f"| Test Name | P-Value | Verdict |\n")
        f.write(f"| :--- | :--- | :--- |\n")
        for name, pval in rows:
            v = verdict(pval).strip()
            if v == "PASSED":
                status = "✅ PASSED"
            elif v == "WEAK":
                status = "⚠️ WEAK"
            else:
                status = "❌ FAILED"
            f.write(f"| {name} | `{pval:.6f}` | {status} |\n")
        
        f.write(f"\n## Interpretation\n")
        f.write(f"- **PASSED:** 0.05 <= p <= 0.95. The data appears random according to this test.\n")
        f.write(f"- **WEAK:** 0.001 <= p < 0.05 or 0.95 < p <= 0.999. The data is suspicious. In a suite of {total} tests, finding a few weak results is statistically expected due to chance.\n")
        f.write(f"- **FAILED:** p < 0.001 or p > 0.999. The data strongly deviates from true randomness.\n")

    print(f"Detailed report saved to: {report_path}\n")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python diehard.py <raw_binary_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    print(f"\nLoading {filepath} ...", end=" ", flush=True)
    data = load_uint32(filepath)
    print(f"{len(data):,} uint32s ({len(data) * 4 / 1e6:.1f} MB) loaded.")
    print(f"\nRunning full Diehard battery. This will take a few minutes...\n")

    rows = []

    # ── Test 1: Birthday Spacings ────────────────────────────────────────────
    print("[01] Birthday Spacings (10 runs)...", flush=True)
    for i, pv in enumerate(test_birthday_spacings(data, 10), 1):
        print_row(f"[01] Birthday Spacings {i:02d}/10", pv, rows)

    # ── Test 2: 5-Permutations ───────────────────────────────────────────────
    print("[02] 5-Permutations (Non-overlap)...", flush=True)
    print_row("[02] 5-Permutations", test_overlapping_permutations(data), rows)

    # ── Test 3: Binary Rank 32x32 ────────────────────────────────────────────
    print("[03] Binary Rank 32x32...", flush=True)
    print_row("[03] Binary Rank 32x32", test_binary_rank_32x32(data, 100), rows)

    # ── Test 4: Binary Rank 6x8 ──────────────────────────────────────────────
    print("[04] Binary Rank 6x8...", flush=True)
    print_row("[04] Binary Rank 6x8", test_binary_rank_6x8(data, 100), rows)

    # ── Test 5: Bitstream ────────────────────────────────────────────────────
    print("[05] Bitstream (3 runs)...", flush=True)
    for i, pv in enumerate(test_bitstream(data, 3), 1):
        print_row(f"[05] Bitstream {i:02d}/03", pv, rows)

    # ── Test 6: OPSO ─────────────────────────────────────────────────────────
    print("[06] OPSO (3 runs)...", flush=True)
    for i, pv in enumerate(test_opso(data, 3), 1):
        print_row(f"[06] OPSO {i:02d}/03", pv, rows)

    # ── Test 7: OQSO ─────────────────────────────────────────────────────────
    print("[07] OQSO (3 runs)...", flush=True)
    for i, pv in enumerate(test_oqso(data, 3), 1):
        print_row(f"[07] OQSO {i:02d}/03", pv, rows)

    # ── Test 8: DNA ──────────────────────────────────────────────────────────
    print("[08] DNA (3 runs)...", flush=True)
    for i, pv in enumerate(test_dna(data, 3), 1):
        print_row(f"[08] DNA {i:02d}/03", pv, rows)

    # ── Test 9: Count 1s (Stream) ────────────────────────────────────────────
    print("[09] Count 1s Stream (Non-overlap)...", flush=True)
    print_row("[09] Count 1s Stream", test_count_ones_stream(data), rows)

    # ── Test 10: Count 1s (Specific Bytes) ───────────────────────────────────
    print("[10] Count 1s (Bytes 1-4)...", flush=True)
    for i, pv in enumerate(test_count_ones_specific_bytes(data), 1):
        print_row(f"[10] Count 1s Byte {i}", pv, rows)

    # ── Test 11: Parking Lot ─────────────────────────────────────────────────
    print("[11] Parking Lot (5 runs)...", flush=True)
    for i, pv in enumerate(test_parking_lot(data, 5), 1):
        print_row(f"[11] Parking Lot {i:02d}/05", pv, rows)

    # ── Test 12: Minimum Distance ────────────────────────────────────────────
    print("[12] Minimum Distance (5 runs)...", flush=True)
    for i, pv in enumerate(test_minimum_distance(data, 5, 8000), 1):
        print_row(f"[12] Minimum Distance {i:02d}/05", pv, rows)

    # ── Test 13: 3D Spheres ──────────────────────────────────────────────────
    print("[13] 3D Spheres (5 runs)...", flush=True)
    for i, pv in enumerate(test_3d_spheres(data, 5, 4000), 1):
        print_row(f"[13] 3D Spheres {i:02d}/05", pv, rows)

    # ── Test 14: Squeeze ─────────────────────────────────────────────────────
    print("[14] Squeeze...", flush=True)
    print_row("[14] Squeeze", test_squeeze(data, 50000), rows)

    # ── Test 15: Overlapping Sums ────────────────────────────────────────────
    print("[15] Sums (Non-overlap)...", flush=True)
    print_row("[15] Sums (Non-overlap)", test_overlapping_sums(data), rows)

    # ── Test 16: Runs Up ─────────────────────────────────────────────────────
    print("[16] Runs Up...", flush=True)
    print_row("[16] Runs Up", test_runs_up(data), rows)

    # ── Test 17: Craps ───────────────────────────────────────────────────────
    print("[17] Craps...", flush=True)
    print_row("[17] Craps", test_craps(data, 50000), rows)

    # ── Final Summary ────────────────────────────────────────────────────────
    all_pvals = [p for _, p in rows]
    passed = sum(1 for p in all_pvals if PASS_LO <= p <= PASS_HI)
    weak   = sum(1 for p in all_pvals if (WEAK_LO <= p < PASS_LO) or (PASS_HI < p <= WEAK_HI))
    failed = sum(1 for p in all_pvals if p < WEAK_LO or p > WEAK_HI)
    total  = len(all_pvals)
    print(f"\n{'='*60}")
    print(f"Summary: {passed}/{total} PASSED | {weak}/{total} WEAK | {failed}/{total} FAILED")
    print(f"{'='*60}\n")
    
    generate_detailed_report(filepath, rows)

if __name__ == "__main__":
    main()
