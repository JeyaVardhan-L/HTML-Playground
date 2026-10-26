<#
.SYNOPSIS
    Automated WAF Lab Report Generator for HTML-Playground.

.DESCRIPTION
    Runs browser automation, tests interactions, captures evidence screenshots,
    and produces an academic Word (.docx) lab record for any specified assignment.

.PARAMETER Assignment
    The assignment number to generate a report for (e.g. 2, 3, 4, 5, 6, 7). Default is 2.

.PARAMETER StudentName
    Optional student name to display on the cover page and header.

.PARAMETER RollNo
    Optional roll/registration number to display on the cover page.

.EXAMPLE
    .\Generate-LabReport.ps1 -Assignment 2
    .\Generate-LabReport.ps1 2
    .\Generate-LabReport.ps1 -Assignment 2 -StudentName "Jey" -RollNo "9057"
#>

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [int]$Assignment = 2,

    [Parameter()]
    [string]$StudentName = "",

    [Parameter()]
    [string]$RollNo = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ScriptDir "tools\lab-report-generator\.venv\Scripts\python.exe"
$GenerateScript = Join-Path $ScriptDir "tools\lab-report-generator\generate.py"

# Verify python executable
if (Test-Path $VenvPython) {
    $PythonExe = $VenvPython
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonExe = "python"
} else {
    Write-Error "Python executable not found. Please ensure Python is installed and accessible."
    exit 1
}

$Arguments = @($GenerateScript, "--assignment", $Assignment)

if ($StudentName -ne "") {
    $Arguments += @("--student-name", $StudentName)
}

if ($RollNo -ne "") {
    $Arguments += @("--roll-no", $RollNo)
}

Write-Host ">>> Invoking WAF Lab Report Generator for Assignment $Assignment..." -ForegroundColor Cyan
& $PythonExe $Arguments
