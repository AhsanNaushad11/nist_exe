import ctypes
import os
import sys

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sts_dir = os.path.join(base_dir, "sts-2.1.2")
    dll_path = os.path.join(sts_dir, "assess.dll")

    if not os.path.exists(dll_path):
        print(f"DLL not found: {dll_path}")
        sys.exit(1)

    # Change working directory so assess.dll outputs correctly
    os.chdir(sts_dir)

    # Write input.txt with the menu choices
    responses = "0\nmy_random_data.bin\n1\n128\n0\n1\n1\n"
    with open("input.txt", "w", encoding="ascii") as f:
        f.write(responses)

    # Redirect stdin at the OS level
    print("Redirecting stdin to input.txt...")
    fd = os.open("input.txt", os.O_RDONLY)
    os.dup2(fd, 0)
    
    # Load the DLL
    print("Loading assess.dll...")
    nist_dll = ctypes.CDLL(dll_path)

    # Prepare argc and argv
    args = [b"assess", b"16777216"]
    argc = len(args)
    argv_type = ctypes.c_char_p * argc
    argv = argv_type(*args)

    # Call main
    print("Calling main() from DLL...")
    nist_dll.main.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
    nist_dll.main.restype = ctypes.c_int
    try:
        result = nist_dll.main(argc, argv)
        print(f"Tests complete. Return code: {result}")
    except Exception as e:
        print(f"Exception calling DLL: {e}")

if __name__ == "__main__":
    main()
