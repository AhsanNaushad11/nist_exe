# Modernize C-Style Standard Libraries to C++

You have requested to completely replace C-style standard libraries (like `<stdio.h>`, `printf`, `FILE*`, `malloc`) with their modern C++ equivalents (like `<iostream>`, `std::cout`, `std::fstream`, `std::vector`) across the entire NIST STS codebase to resolve the IDE's `'stdio.h' file not found` error.

> [!IMPORTANT]
> **CRITICAL CLARIFICATION BEFORE WE PROCEED**
> 
> The error `'stdio.h' file not found` almost certainly means your IDE's IntelliSense cannot find the root folder for **ANY** standard library headers. 
> 
> If we replace `<stdio.h>` with `<iostream>`, your IDE will most likely just show a new error: `'iostream' file not found`. This is because the underlying issue isn't that `<stdio.h>` is a C library, but rather that VSCode doesn't know where your MinGW compiler's include folder is. 
> 
> Before we undertake a massive rewrite of 22 files, could you try changing `#include <stdio.h>` to `#include <iostream>` manually in `assess.cpp` and see if the red squiggle simply moves to `<iostream>`?

## Proposed Changes (If we proceed with the rewrite)

If you still want to modernize the codebase to use purely C++ standard libraries, it is a significant architectural change. Here is the plan:

### 1. I/O and File Handling
- **[MODIFY]** All 22 source files
- Replace `#include <stdio.h>` with `#include <iostream>`, `#include <fstream>`, and `#include <iomanip>`.
- Replace all `printf(...)` with `std::cout << ...`.
- Replace all `fprintf(fp, ...)` with `std::ofstream` objects.
- Replace all `FILE *` and `fopen`/`fclose` with `std::ifstream` and `std::ofstream`.
- Replace `fscanf` and `fseek` with C++ stream extraction (`>>`) and `seekg`.

### 2. Memory Management
- **[MODIFY]** All array allocations
- Replace `#include <stdlib.h>` calls like `malloc` and `calloc` with modern C++ equivalents.
- For dynamic arrays, use `std::vector<T>`.
- For single allocations, use the `new` operator.

### 3. Strings and Mathematics
- **[MODIFY]** Core utilities
- Replace `#include <string.h>` with `#include <string>` and `<cstring>`.
- Replace `#include <math.h>` with `#include <cmath>`.

## Open Questions

1. **IDE Verification**: Could you test if `#include <iostream>` also gives a "file not found" error in your IDE?
2. **Scope of Rewrite**: Do you want me to proceed with the massive rewrite of `printf` -> `std::cout`, `FILE*` -> `std::fstream`, and `malloc` -> `std::vector`/`new` across all 22 files? This will touch almost every function in the project.

## Verification Plan

### Automated Tests
- Run `mingw32-make` to ensure all files compile with the new C++ I/O.
- Run `run_nist_final_test.ps1` to ensure the generated statistics files and console output match the original formats perfectly.
