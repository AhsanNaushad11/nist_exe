# Diehard Statistical Test Report

**Target File:** `raw_fortuna_128.bin`
**Total Tests Run:** 49

## Summary
- **PASSED:** 40/49
- **WEAK:** 9/49
- **FAILED:** 0/49

## Detailed Results
| Test Name | P-Value | Verdict |
| :--- | :--- | :--- |
| [01] Birthday Spacings 01/10 | `0.676676` | ✅ PASSED |
| [01] Birthday Spacings 02/10 | `0.406006` | ✅ PASSED |
| [01] Birthday Spacings 03/10 | `0.676676` | ✅ PASSED |
| [01] Birthday Spacings 04/10 | `0.406006` | ✅ PASSED |
| [01] Birthday Spacings 05/10 | `0.947347` | ✅ PASSED |
| [01] Birthday Spacings 06/10 | `0.406006` | ✅ PASSED |
| [01] Birthday Spacings 07/10 | `0.406006` | ✅ PASSED |
| [01] Birthday Spacings 08/10 | `0.406006` | ✅ PASSED |
| [01] Birthday Spacings 09/10 | `0.857123` | ✅ PASSED |
| [01] Birthday Spacings 10/10 | `0.857123` | ✅ PASSED |
| [02] 5-Permutations | `0.104118` | ✅ PASSED |
| [03] Binary Rank 32x32 | `0.140421` | ✅ PASSED |
| [04] Binary Rank 6x8 | `0.189035` | ✅ PASSED |
| [05] Bitstream 01/03 | `0.001905` | ⚠️ WEAK |
| [05] Bitstream 02/03 | `0.075568` | ✅ PASSED |
| [05] Bitstream 03/03 | `0.007327` | ⚠️ WEAK |
| [06] OPSO 01/03 | `0.143411` | ✅ PASSED |
| [06] OPSO 02/03 | `0.396918` | ✅ PASSED |
| [06] OPSO 03/03 | `0.435127` | ✅ PASSED |
| [07] OQSO 01/03 | `0.570949` | ✅ PASSED |
| [07] OQSO 02/03 | `0.222635` | ✅ PASSED |
| [07] OQSO 03/03 | `0.033466` | ⚠️ WEAK |
| [08] DNA 01/03 | `0.030172` | ⚠️ WEAK |
| [08] DNA 02/03 | `0.413141` | ✅ PASSED |
| [08] DNA 03/03 | `0.604194` | ✅ PASSED |
| [09] Count 1s Stream | `0.283721` | ✅ PASSED |
| [10] Count 1s Byte 1 | `0.118939` | ✅ PASSED |
| [10] Count 1s Byte 2 | `0.533714` | ✅ PASSED |
| [10] Count 1s Byte 3 | `0.393131` | ✅ PASSED |
| [10] Count 1s Byte 4 | `0.363574` | ✅ PASSED |
| [11] Parking Lot 01/05 | `0.273127` | ✅ PASSED |
| [11] Parking Lot 02/05 | `0.017576` | ⚠️ WEAK |
| [11] Parking Lot 03/05 | `0.025257` | ⚠️ WEAK |
| [11] Parking Lot 04/05 | `0.005346` | ⚠️ WEAK |
| [11] Parking Lot 05/05 | `0.044523` | ⚠️ WEAK |
| [12] Minimum Distance 01/05 | `0.807288` | ✅ PASSED |
| [12] Minimum Distance 02/05 | `0.363268` | ✅ PASSED |
| [12] Minimum Distance 03/05 | `0.097636` | ✅ PASSED |
| [12] Minimum Distance 04/05 | `0.246973` | ✅ PASSED |
| [12] Minimum Distance 05/05 | `0.232963` | ✅ PASSED |
| [13] 3D Spheres 01/05 | `0.860595` | ✅ PASSED |
| [13] 3D Spheres 02/05 | `0.075793` | ✅ PASSED |
| [13] 3D Spheres 03/05 | `0.314541` | ✅ PASSED |
| [13] 3D Spheres 04/05 | `0.073697` | ✅ PASSED |
| [13] 3D Spheres 05/05 | `0.654338` | ✅ PASSED |
| [14] Squeeze | `0.982262` | ⚠️ WEAK |
| [15] Sums (Non-overlap) | `0.656930` | ✅ PASSED |
| [16] Runs Up | `0.086594` | ✅ PASSED |
| [17] Craps | `0.368490` | ✅ PASSED |

## Interpretation
- **PASSED:** 0.05 <= p <= 0.95. The data appears random according to this test.
- **WEAK:** 0.001 <= p < 0.05 or 0.95 < p <= 0.999. The data is suspicious. In a suite of 49 tests, finding a few weak results is statistically expected due to chance.
- **FAILED:** p < 0.001 or p > 0.999. The data strongly deviates from true randomness.
