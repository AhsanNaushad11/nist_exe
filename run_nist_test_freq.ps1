$dllPath = Join-Path $PSScriptRoot "sts-2.1.2\assess.dll"

$code = @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class NistSTSLauncherTest2 {
    [DllImport("$($dllPath.Replace('\','\\'))", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int main(int argc, string[] argv);

    public static void RunNist(int testNum) {
        // Run only 1 specific test to see if a specific test is causing the crash
        // testNum corresponds to the test number (01 to 15)
        string testSelection = new String('0', 16).Remove(testNum, 1).Insert(testNum, "1");
        
        string responses = "0\nmy_random_data.bin\n0\n" + testSelection + "\n0\n1\n1\n";
        Console.SetIn(new StringReader(responses));

        string[] args = new string[] { "assess", "16777216" };
        main(2, args);
    }
}
"@

Add-Type -TypeDefinition $code

Push-Location (Join-Path $PSScriptRoot "sts-2.1.2")
$previousProcessDir = [Environment]::CurrentDirectory
[Environment]::CurrentDirectory = (Get-Location).Path

try {
    # Test just the Frequency test (01)
    [NistSTSLauncherTest2]::RunNist(1)
} finally {
    [Environment]::CurrentDirectory = $previousProcessDir
    Pop-Location
}
