# Task Tracker: NIST STS C++ Translation

- `[x]` Rename all `.c` files to `.cpp` in `sts-2.1.2/src`
- `[x]` Update `makefile` to use `g++` and compile `.cpp` files
- `[x]` Fix `assess.cpp` (add `extern "C"` to `main`)
- `[x]` Fix type casting and `malloc` errors across the `.cpp` files
- `[x]` Replace `int ifac[15]` with `std::vector<int>` in `dfft.cpp` and `discreteFourierTransform.cpp`
- `[x]` Fix `fseek` bug in `nonOverlappingTemplateMatchings.cpp`
- `[x]` Compile the codebase using `make` and fix any new C++ warnings/errors
- `[x]` Run `run_nist.ps1` with `my_random_data.bin` to test
- `[x]` Create walkthrough artifact
