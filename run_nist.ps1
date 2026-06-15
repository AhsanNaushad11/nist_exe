$code = @"
using System;
using System.Runtime.InteropServices;

public class NistSTSLauncher {
    [DllImport(@"c:\my_projects\nist_exe\sts-2.1.2\assess.dll", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int main(int argc, string[] argv);

    public static void RunNist() {
        string[] args = new string[] { "assess", "16777216" };
        main(2, args);
    }
}
"@

Add-Type -TypeDefinition $code
[NistSTSLauncher]::RunNist()
