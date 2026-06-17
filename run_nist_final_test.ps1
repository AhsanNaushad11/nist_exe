# This script runs the final NIST statistical test suite automatically via assess.dll
$dllPath = Join-Path $PSScriptRoot "sts-2.1.2\assess.dll"

if (!(Test-Path $dllPath)) {
    Write-Host "DLL not found: $dllPath"
    Write-Host "Please build assess.dll using mingw32-make."
    exit
}

Push-Location (Join-Path $PSScriptRoot "sts-2.1.2")

$env:PATH = "$($PWD.ProviderPath);" + $env:PATH
[Environment]::CurrentDirectory = $PWD.ProviderPath

# We write the input menu responses into input.txt, which assess.dll reads via freopen
$responses = "0`nmy_random_data.bin`n1`n128`n0`n1`n1`n"
Set-Content -Path "input.txt" -Value $responses -Encoding Ascii

# Define P/Invoke for the DLL
$code = @"
using System;
using System.Runtime.InteropServices;

public class NistTestRunner
{
    [DllImport("assess.dll", CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
    public static extern int nist_main(int argc, string[] argv);
}
"@

Add-Type -TypeDefinition $code -ErrorAction Stop

Write-Host "Running NIST tests via DLL..."
$cmdArgs = @("assess", "16777216")
[NistTestRunner]::nist_main(2, $cmdArgs)

Pop-Location
Write-Host "Tests complete."
