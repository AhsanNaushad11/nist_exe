import os
import glob

src_dir = r"c:\my_projects\nist_exe\sts-2.1.2\src"
inc_dir = r"c:\my_projects\nist_exe\sts-2.1.2\include"

files = glob.glob(os.path.join(src_dir, "*.cpp")) + glob.glob(os.path.join(inc_dir, "*.h"))

for f in files:
    with open(f, "r") as file:
        content = file.read()
    
    # Replace standard headers with C++ equivalents
    content = content.replace("#include <stdio.h>", "#include <iostream>\n#include <fstream>\n#include <cstdio>")
    content = content.replace("#include <stdlib.h>", "#include <cstdlib>")
    content = content.replace("#include <math.h>", "#include <cmath>")
    content = content.replace("#include <string.h>", "#include <cstring>\n#include <string>")
    
    with open(f, "w") as file:
        file.write(content)
print("Headers modernized across all files.")
