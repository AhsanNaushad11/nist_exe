$dllPath = Join-Path $PSScriptRoot "sts-2.1.2\assess.dll"

# Build the C# interop class
$code = @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class NistSTSLauncher {
    [DllImport("$($dllPath.Replace('\','\\'))", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int main(int argc, string[] argv);

    public static void RunNist(string inputFilePath) {
        // Prepare automated responses for scanf prompts:
        //   0              = Generator: Input File
        //   <filepath>     = Path to binary data file
        //   1              = Run ALL tests
        //   0              = Accept default parameters
        //   1              = Number of bitstreams
        //   1              = Binary file format
        string responses = "0\n" + inputFilePath + "\n1\n0\n1\n1\n";
        Console.SetIn(new StringReader(responses));

        string[] args = new string[] { "assess", "16777216" };
        main(2, args);
    }
}
"@

Add-Type -TypeDefinition $code

# Set working directory to sts-2.1.2 so relative paths for experiments/ and templates/ work
Push-Location (Join-Path $PSScriptRoot "sts-2.1.2")
try {
    [NistSTSLauncher]::RunNist("..\my_random_data.bin")
} finally {
    Pop-Location
}
