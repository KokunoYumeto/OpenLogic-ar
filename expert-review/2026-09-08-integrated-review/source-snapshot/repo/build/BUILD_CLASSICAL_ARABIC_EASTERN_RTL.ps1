param(
  [ValidateSet("primary", "replay")]
  [string]$BuildRole = "primary",

  [string]$BuildRunId = "",

  [Parameter(Mandatory = $true)]
  [string]$SourceClosureReceipt,

  [Parameter(Mandatory = $true)]
  [string]$RTLClosureReceipt,

  [string]$MaterializationReceipt = "",

  [string]$ReferenceBuildReceipt = "",

  [string]$FinalOutputDirectory = "",
  [string]$WorkDirectory = "",
  [ValidateRange(1, 3600)]
  [int]$MutexTimeoutSeconds = 600
)

$ErrorActionPreference = "Stop"
$releaseRoot = Split-Path -Parent $PSScriptRoot
$inner = Join-Path $PSScriptRoot "BUILD_CLASSICAL_ARABIC_EASTERN_RTL_INNER.ps1"
$mutexWrapper = Join-Path $PSScriptRoot "Invoke-WithInterlanguageTeXMutex.ps1"
$buildContract = Join-Path $PSScriptRoot "classical_reader_build_contract.py"
$contractPython = (Get-Command python -CommandType Application -ErrorAction Stop |
  Select-Object -First 1).Source

if ([string]::IsNullOrWhiteSpace($BuildRunId)) {
  $BuildRunId = "{0}-{1}" -f `
    [DateTimeOffset]::UtcNow.ToString("yyyyMMddTHHmmssZ"), `
    ([Guid]::NewGuid().ToString("N").Substring(0, 12))
}
if ($BuildRunId -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{7,79}$') {
  throw "BuildRunId must be 8--80 safe filename characters"
}
if ($BuildRole -eq "replay" -and
    [string]::IsNullOrWhiteSpace($ReferenceBuildReceipt)) {
  throw "Replay builds require ReferenceBuildReceipt"
}
if ($BuildRole -eq "primary" -and
    -not [string]::IsNullOrWhiteSpace($ReferenceBuildReceipt)) {
  throw "Primary builds must not supply ReferenceBuildReceipt"
}
if ([string]::IsNullOrWhiteSpace($MaterializationReceipt)) {
  $MaterializationReceipt = Join-Path $releaseRoot `
    "evidence\classical\NOTATION_MATERIALIZATION_RECEIPT.json"
}

if ([string]::IsNullOrWhiteSpace($FinalOutputDirectory)) {
  $FinalOutputDirectory = Join-Path $releaseRoot `
    "output\pdf\classical-arabic-eastern-rtl\$BuildRole-$BuildRunId"
}
if ([string]::IsNullOrWhiteSpace($WorkDirectory)) {
  $WorkDirectory = Join-Path $releaseRoot `
    "tmp\pdfs\classical-arabic-eastern-rtl-$BuildRole-$BuildRunId"
}

foreach ($required in @($inner, $mutexWrapper, $buildContract)) {
  if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
    throw "Required Classical build entry is missing: $required"
  }
}

$shell = (Get-Process -Id $PID).Path
$arguments = @(
  "-NoProfile",
  "-File", $inner,
  "-BuildRole", $BuildRole,
  "-BuildRunId", $BuildRunId,
  "-SourceClosureReceipt", $SourceClosureReceipt,
  "-RTLClosureReceipt", $RTLClosureReceipt,
  "-MaterializationReceipt", $MaterializationReceipt,
  "-FinalOutputDirectory", $FinalOutputDirectory,
  "-WorkDirectory", $WorkDirectory
)
if ($BuildRole -eq "replay") {
  $arguments += @("-ReferenceBuildReceipt", $ReferenceBuildReceipt)
}

# This is the sole process-launch boundary. The wrapper owns the named mutex
# continuously until the complete LuaLaTeX/BibTeX/Python process tree drains.
& $mutexWrapper `
  -Command $shell `
  -CommandArguments $arguments `
  -AcquisitionTimeoutSeconds $MutexTimeoutSeconds `
  -ReceiptPath (Join-Path $WorkDirectory "TEX_MUTEX_RECEIPT.json")
if ($LASTEXITCODE -ne 0) {
  throw "Classical-Arabic build failed with exit code $LASTEXITCODE"
}

# Only a completed outer guard can establish that the captured process tree
# drained. The inner receipt is deliberately pending, never a premature PASS.
# This phase invokes no TeX or bibliography process and cannot restart a build.
& $contractPython $buildContract finalize `
  --capture (Join-Path $WorkDirectory "CLASSICAL_BUILD_INPUTS.json") `
  --pending (Join-Path $FinalOutputDirectory "CLASSICAL_BUILD_PENDING.json") `
  --guard (Join-Path $WorkDirectory "TEX_MUTEX_RECEIPT.json") `
  --output (Join-Path $FinalOutputDirectory "CLASSICAL_BUILD_ARTIFACTS.json")
if ($LASTEXITCODE -ne 0) {
  throw "Classical build guard-drain/public artifact finalization failed"
}
