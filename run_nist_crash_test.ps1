$dllPath = Join-Path $PSScriptRoot "sts-2.1.2\assess.dll"

$code = @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class NistSTSLauncherCrashTest {
    [DllImport("$($dllPath.Replace('\','\\'))", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int main(int argc, string[] argv);

    public static void RunNist(int testNum) {
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
    for ($i = 1; $i -le 15; $i++) {
        Write-Host "Running Test $i..."
        try {
            [NistSTSLauncherCrashTest]::RunNist($i)
            Write-Host "Test $i passed"
        } catch {
            Write-Host "Test $i CRASHED: $($_.Exception.Message)"
        }
    }
} finally {
    [Environment]::CurrentDirectory = $previousProcessDir
    Pop-Location
}
