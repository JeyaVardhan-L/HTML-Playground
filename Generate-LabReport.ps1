<#
.SYNOPSIS
    Automated WAF Lab Report Generator for HTML-Playground.

.DESCRIPTION
    Runs browser automation, tests interactions, captures evidence screenshots,
    and produces an academic Word (.docx) and PDF lab record for any specified assignment.

.PARAMETER Assignment
    The assignment number to generate a report for (e.g. 1, 2, 3, 4, 5, 6, 7). Default is 2.

.PARAMETER StudentName
    Optional student name to display on the cover page and header.

.PARAMETER RollNo
    Optional roll/registration number to display on the cover page.

.PARAMETER Port
    Optional preferred port to run the application server on.

.PARAMETER List
    Switch to list all supported assignments and exit.

.PARAMETER ValidateOnly
    Switch to validate assignment configuration and source files without generating documents.

.PARAMETER EvidenceOnly
    Switch to capture output screenshots and CLI logs without generating Word or PDF documents.

.PARAMETER SkipRender
    Switch to skip Word-to-PDF conversion and visual QA preview rendering.

.EXAMPLE
    .\Generate-LabReport.ps1 -Assignment 2
    .\Generate-LabReport.ps1 3
    .\Generate-LabReport.ps1 -Assignment 6 -StudentName "Jey" -RollNo "9057"
    .\Generate-LabReport.ps1 -List
    .\Generate-LabReport.ps1 -ValidateOnly
    .\Generate-LabReport.ps1 -Assignment 7 -EvidenceOnly
#>

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [int]$Assignment = 2,

    [Parameter()]
    [string]$StudentName = "",

    [Parameter()]
    [string]$RollNo = "",

    [Parameter()]
    [int]$Port = 0,

    [Parameter()]
    [switch]$List,

    [Parameter()]
    [switch]$ValidateOnly,

    [Parameter()]
    [switch]$EvidenceOnly,

    [Parameter()]
    [switch]$SkipRender
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

$Arguments = @($GenerateScript)

if ($List) {
    $Arguments += @("--list")
    & $PythonExe $Arguments
    exit $LASTEXITCODE
}

if ($ValidateOnly) {
    $Arguments += @("--validate-only")
    if ($PSBoundParameters.ContainsKey('Assignment')) {
        $Arguments += @("--assignment", $Assignment)
    }
    & $PythonExe $Arguments
    exit $LASTEXITCODE
}

$Arguments += @("--assignment", $Assignment)

if ($StudentName -ne "") {
    $Arguments += @("--student-name", $StudentName)
}

if ($RollNo -ne "") {
    $Arguments += @("--roll-no", $RollNo)
}

if ($Port -gt 0) {
    $Arguments += @("--port", $Port)
}

if ($EvidenceOnly) {
    $Arguments += @("--evidence-only")
}

if ($SkipRender) {
    $Arguments += @("--skip-render")
}

Write-Host ">>> Invoking WAF Lab Report Generator for Assignment $Assignment..." -ForegroundColor Cyan
& $PythonExe $Arguments
exit $LASTEXITCODE
