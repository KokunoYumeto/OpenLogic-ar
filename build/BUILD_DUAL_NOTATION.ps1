param(
  [string]$FinalOutputDirectory = "",
  [string]$WorkDirectory = "",
  [switch]$ResumeExisting,
  [ValidateRange(1, 3600)]
  [int]$MutexTimeoutSeconds = 600
)

$ErrorActionPreference = "Stop"
$releaseRoot = Split-Path -Parent $PSScriptRoot
$inner = Join-Path $PSScriptRoot "BUILD_DUAL_NOTATION_INNER.ps1"
$mutexWrapper = Join-Path $PSScriptRoot "Invoke-WithInterlanguageTeXMutex.ps1"

if ([string]::IsNullOrWhiteSpace($FinalOutputDirectory)) {
  $FinalOutputDirectory = Join-Path $releaseRoot "output\pdf"
}
if ([string]::IsNullOrWhiteSpace($WorkDirectory)) {
  $WorkDirectory = Join-Path $releaseRoot "tmp\pdfs\dual-notation-build"
}

$shell = (Get-Process -Id $PID).Path
$arguments = @(
  "-NoProfile",
  "-File", $inner,
  "-FinalOutputDirectory", $FinalOutputDirectory,
  "-WorkDirectory", $WorkDirectory
)
if ($ResumeExisting) {
  $arguments += "-ResumeExisting"
}

& $mutexWrapper `
  -Command $shell `
  -CommandArguments $arguments `
  -AcquisitionTimeoutSeconds $MutexTimeoutSeconds
if ($LASTEXITCODE -ne 0) {
  throw "Dual-notation build failed with exit code $LASTEXITCODE"
}
