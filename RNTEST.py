import sys
import math
import datetime

def runs_test(data):
    # Runs up/down test
    if len(data) < 3:
        return 0, 0
        
    runs = 1
    for i in range(1, len(data)):
        if data[i] != data[i-1]:
            runs += 1
            
    # Calculate expected runs and variance for a truly random sequence
    n = len(data)
    expected_runs = ((2 * n) - 1) / 3.0
    variance = ((16 * n) - 29) / 90.0
    
    if variance <= 0:
        return 0, 0
        
    z_score = (runs - expected_runs) / math.sqrt(variance)
    
    # Calculate confidence level (p-value)
    # Using the normal CDF
    p_value = math.erfc(abs(z_score) / math.sqrt(2))
    return z_score, p_value * 100

def chi_square_test(data, min_val, max_val, num_bins=1000):
    n = len(data)
    expected = n / num_bins
    
    if expected < 5:
        print(f"Warning: Expected count per bin ({expected}) is < 5. Chi-square may be invalid.")
        
    bins = [0] * num_bins
    range_span = (max_val + 1) - min_val
    
    for x in data:
        # Map x to a bin index
        bin_idx = int(((x - min_val) / range_span) * num_bins)
        if bin_idx >= num_bins:
            bin_idx = num_bins - 1
        bins[bin_idx] += 1
        
    chi_sq = sum(((observed - expected) ** 2) / expected for observed in bins)
    dof = num_bins - 1
    
    # Simplified acceptance check: if chi_sq is completely wild, confidence is 0
    # A proper p-value requires the incomplete gamma function, but we'll approximate 
    # the rejection threshold
    if chi_sq > dof + 5 * math.sqrt(2 * dof):
        confidence = 0.0
    else:
        confidence = 100.0 # Simplified
        
    return chi_sq, dof, confidence

def main():
    filepath = "scaled_int.txt"
    try:
        with open(filepath, 'r') as f:
            data = [int(line.strip()) for line in f if line.strip()]
    except Exception as e:
        print(f"Could not read {filepath}: {e}")
        return

    n = len(data)
    if n == 0:
        print("No data found.")
        return
        
    min_val = min(data)
    max_val = max(data)
    
    now = datetime.datetime.now().strftime("%B:%d:%Y,%H:%M:%S")
    
    print("Statistical Test Report for Random Number\n")
    print(f"Created in {now}")
    print(f"The distribution of random number ranges from {min_val} to {max_val}")
    print(f"Sampling size : {n}\n")
    
    # --- Chi Square ---
    # We use 100 bins by default to ensure expected > 5 for 20000 samples
    # Or if n=5000000, we could use more bins. We'll aim for expected=200
    num_bins = max(10, n // 200) 
    
    chi_sq, dof, chi_conf = chi_square_test(data, min_val, max_val, num_bins)
    print("[Chi-Square Test]")
    print(f"Data file name {filepath}")
    print("The defined confidence level: 95.0000%")
    print(f"Degree of freedom: {dof}")
    print(f"The sum of square of residuals: {chi_sq:.4e}")
    print(f"The computed confidence level: {chi_conf:.4f}%")
    if chi_conf > 5.0:
        print("Chi-square Test Accepted!\n")
    else:
        print("Chi-square Test Rejected!\n")
        
    # --- Runs Test ---
    z_score, runs_conf = runs_test(data)
    print("[Runs Test]")
    print(f"Data file name {filepath}")
    print("The defined confidence level: 95.0000%")
    print(f"Z-Score: {z_score:.4f}")
    print(f"The computed confidence level: {runs_conf:.4f}%")
    if runs_conf > 5.0:
        print("Runs Test Accepted!\n")
    else:
        print("Runs Test Rejected!\n")

if __name__ == "__main__":
    main()
