param(
  [Parameter(Mandatory = $true)]
  [ValidateNotNullOrEmpty()]
  [string]$FinalOutputDirectory,

  [Parameter(Mandatory = $true)]
  [ValidateNotNullOrEmpty()]
  [string]$WorkDirectory,

  [switch]$ResumeExisting,
  [ValidateRange(1, 3600)]
  [int]$MutexTimeoutSeconds = 600
)

$ErrorActionPreference = "Stop"
$releaseRoot = Split-Path -Parent $PSScriptRoot
$inner = Join-Path $PSScriptRoot "BUILD_DUAL_NOTATION_INNER.ps1"
$mutexWrapper = Join-Path $PSScriptRoot "Invoke-WithInterlanguageTeXMutex.ps1"

function Get-NormalizedPath {
  param([Parameter(Mandatory = $true)][string]$Path)
  if ([string]::IsNullOrWhiteSpace($Path)) {
    throw "Build directories must be explicit, nonblank paths."
  }
  return [IO.Path]::GetFullPath($Path)
}

function Test-PathIsSameOrNested {
  param(
    [Parameter(Mandatory = $true)][string]$Candidate,
    [Parameter(Mandatory = $true)][string]$Root
  )
  if ($Candidate.Equals($Root, [StringComparison]::OrdinalIgnoreCase)) {
    return $true
  }
  $prefix = $Root.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
  return $Candidate.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)
}

$FinalOutputDirectory = Get-NormalizedPath -Path $FinalOutputDirectory
$WorkDirectory = Get-NormalizedPath -Path $WorkDirectory
if ((Test-PathIsSameOrNested -Candidate $FinalOutputDirectory -Root $WorkDirectory) -or
    (Test-PathIsSameOrNested -Candidate $WorkDirectory -Root $FinalOutputDirectory)) {
  throw "Final-output and private work directories must be distinct and non-nested."
}

# The previous r3/OLSIZ directory is historical evidence.  Its PDFs predate the
# current corrected source and must never be resumed, overwritten, or presented
# as the output of a fresh acceptance build.
$staleR3Root = Get-NormalizedPath -Path (Join-Path $releaseRoot "output\pdf\complete-722-r3-final-olsiz")
foreach ($candidate in @($FinalOutputDirectory, $WorkDirectory)) {
  if (Test-PathIsSameOrNested -Candidate $candidate -Root $staleR3Root) {
    throw "Refusing the stale historical r3/OLSIZ build root: $candidate"
  }
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

Push-Location $releaseRoot
try {
  & $mutexWrapper `
    -Command $shell `
    -CommandArguments $arguments `
    -AcquisitionTimeoutSeconds $MutexTimeoutSeconds `
    -ReceiptPath (Join-Path $WorkDirectory "TEX_MUTEX_RECEIPT.json")
  $buildExitCode = $LASTEXITCODE
} finally {
  Pop-Location
}
if ($buildExitCode -ne 0) {
  throw "Dual-notation build failed with exit code $buildExitCode"
}
