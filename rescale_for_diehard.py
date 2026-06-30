import sys
import struct
import os

def rescale_file(input_path, output_path, min_val, max_val):
    """
    Reads scaled integers from input_path, maps them from [min_val, max_val) 
    to the full 32-bit unsigned integer range [0, 4294967295], and writes 
    them as a raw binary file for Dieharder.
    """
    if min_val >= max_val:
        print("Error: min_val must be strictly less than max_val")
        return False
        
    range_span = (max_val - 1) - min_val
    if range_span <= 0:
        print("Error: The range must contain at least 2 distinct values")
        return False

    print(f"Reading from: {input_path}")
    print(f"Original range: [{min_val}, {max_val})")
    print(f"Mapping to 32-bit range: [0, 4294967295]")

    count = 0
    with open(input_path, 'r') as infile, open(output_path, 'wb') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                x = int(line)
            except ValueError:
                print(f"Warning: Skipping non-integer line: '{line}'")
                continue
                
            # Clamp the value to the expected range
            if x < min_val:
                x = min_val
            elif x >= max_val:
                x = max_val - 1
                
            # Rescale to [0, 4294967295]
            y = int(((x - min_val) / range_span) * 4294967295)
            
            # Pack as a 32-bit unsigned integer
            # '<I' represents little-endian 32-bit unsigned integer
            packed_data = struct.pack('<I', y)
            outfile.write(packed_data)
            count += 1

    print(f"Successfully processed {count} integers.")
    print(f"Binary file written to: {output_path} ({count * 4} bytes)")
    return True

def main():
    if len(sys.argv) < 5:
        print("Usage: python rescale_for_diehard.py <input_txt> <output_bin> <min> <max>")
        print("Example:")
        print("  python rescale_for_diehard.py scaled_int.txt rescaled_int.bin 100 900000")
        sys.exit(1)
        
    input_txt = sys.argv[1]
    output_bin = sys.argv[2]
    
    try:
        min_val = int(sys.argv[3])
        max_val = int(sys.argv[4])
    except ValueError:
        print("Error: min and max must be integers")
        sys.exit(1)
        
    if not os.path.exists(input_txt):
        print(f"Error: Input file does not exist: {input_txt}")
        sys.exit(1)
        
    success = rescale_file(input_txt, output_bin, min_val, max_val)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
