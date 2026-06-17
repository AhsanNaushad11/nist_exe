$dllPath = Join-Path $PSScriptRoot "sts-2.1.2\assess.dll"

$code = @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class NistSTSLauncherTest {
    [DllImport("$($dllPath.Replace('\','\\'))", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int main(int argc, string[] argv);

    public static void RunNist() {
        string responses = "0\nmy_random_data.bin\n1\n0\n1\n1\n";
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
    [NistSTSLauncherTest]::RunNist()
} finally {
    [Environment]::CurrentDirectory = $previousProcessDir
    Pop-Location
}
