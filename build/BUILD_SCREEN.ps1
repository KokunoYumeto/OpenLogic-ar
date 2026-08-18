param(
  [string]$OutputDirectory = "",
  [string]$ExpectedCompleteSha256 = "",
  [string]$ExpectedSupplementSha256 = "",
  [switch]$StageReleaseAssets
)

$ErrorActionPreference = "Stop"

$releaseRoot = Split-Path -Parent $PSScriptRoot
$localeRoot = Join-Path $releaseRoot "source\locale\ar"
$completeDriverName = "open-logic-complete-ar-screen.tex"
$supplementDriverName = "open-logic-closure-supplement-ar-screen.tex"
$completeDriver = Join-Path $localeRoot $completeDriverName
$supplementDriver = Join-Path $localeRoot $supplementDriverName
$completeJob = [IO.Path]::GetFileNameWithoutExtension($completeDriverName)
$supplementJob = [IO.Path]::GetFileNameWithoutExtension($supplementDriverName)
$expectedConceptDoi = "10.5281/zenodo.21921850"
$forbiddenVersionDois = @(
  "10.5281/zenodo.21921851",
  "10.5281/zenodo.21987686"
)
$expectedCompletePages = 946
$expectedSupplementPages = 136

foreach ($driver in @($completeDriver, $supplementDriver)) {
  if (-not (Test-Path -LiteralPath $driver -PathType Leaf)) {
    throw "Packaged screen driver is missing: $driver"
  }
  $driverText = [IO.File]::ReadAllText($driver)
  if (-not $driverText.Contains($expectedConceptDoi)) {
    throw "Stable concept DOI is absent from $driver"
  }
  foreach ($forbiddenDoi in $forbiddenVersionDois) {
    if ($driverText.Contains($forbiddenDoi)) {
      throw "Exact or obsolete version DOI must not be embedded in the screen driver: $driver"
    }
  }
}

foreach ($commandName in @("lualatex", "bibtex", "pdfinfo")) {
  if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
    throw "Required command is unavailable: $commandName"
  }
}

if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
  $OutputDirectory = Join-Path $PSScriptRoot "output-ar-screen-OLP-0722"
}
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$resolvedOutput = (Resolve-Path -LiteralPath $OutputDirectory).Path
$outputArgument = "-output-directory=$resolvedOutput"
$latexArguments = @(
  "-interaction=nonstopmode",
  "-halt-on-error",
  "-file-line-error",
  "-recorder",
  $outputArgument
)

$oldSourceDateEpoch = [Environment]::GetEnvironmentVariable("SOURCE_DATE_EPOCH", "Process")
$oldForceSourceDate = [Environment]::GetEnvironmentVariable("FORCE_SOURCE_DATE", "Process")
$oldTimeZone = [Environment]::GetEnvironmentVariable("TZ", "Process")
$oldTexInputs = [Environment]::GetEnvironmentVariable("TEXINPUTS", "Process")

function Get-PdfPageCount {
  param([Parameter(Mandatory = $true)][string]$Path)

  $metadata = & pdfinfo $Path
  if ($LASTEXITCODE -ne 0) {
    throw "pdfinfo failed for $Path with exit code $LASTEXITCODE"
  }
  $pageLine = $metadata | Where-Object { $_ -match "^Pages:\s+(\d+)\s*$" } | Select-Object -First 1
  if ($null -eq $pageLine) {
    throw "Unable to read the page count from $Path"
  }
  return [int]([regex]::Match([string]$pageLine, "^Pages:\s+(\d+)\s*$").Groups[1].Value)
}

try {
  [Environment]::SetEnvironmentVariable("SOURCE_DATE_EPOCH", "1783874174", "Process")
  [Environment]::SetEnvironmentVariable("FORCE_SOURCE_DATE", "1", "Process")
  [Environment]::SetEnvironmentVariable("TZ", "UTC", "Process")
  $texInputs = if ([string]::IsNullOrEmpty($oldTexInputs)) {
    "$resolvedOutput;"
  } else {
    "$resolvedOutput;$oldTexInputs"
  }
  [Environment]::SetEnvironmentVariable("TEXINPUTS", $texInputs, "Process")

  Push-Location $localeRoot
  try {
    & lualatex @latexArguments $completeDriverName
    if ($LASTEXITCODE -ne 0) { throw "Screen reader LuaLaTeX pass 1 failed" }

    & bibtex (Join-Path $resolvedOutput $completeJob)
    if ($LASTEXITCODE -ne 0) { throw "Screen reader BibTeX pass failed" }

    for ($pass = 2; $pass -le 3; $pass++) {
      & lualatex @latexArguments $completeDriverName
      if ($LASTEXITCODE -ne 0) { throw "Screen reader LuaLaTeX pass $pass failed" }
    }

    for ($pass = 1; $pass -le 2; $pass++) {
      & lualatex @latexArguments $supplementDriverName
      if ($LASTEXITCODE -ne 0) { throw "Screen supplement LuaLaTeX pass $pass failed" }
    }
  } finally {
    Pop-Location
  }
} finally {
  [Environment]::SetEnvironmentVariable("SOURCE_DATE_EPOCH", $oldSourceDateEpoch, "Process")
  [Environment]::SetEnvironmentVariable("FORCE_SOURCE_DATE", $oldForceSourceDate, "Process")
  [Environment]::SetEnvironmentVariable("TZ", $oldTimeZone, "Process")
  [Environment]::SetEnvironmentVariable("TEXINPUTS", $oldTexInputs, "Process")
}

$completePdf = Join-Path $resolvedOutput "$completeJob.pdf"
$supplementPdf = Join-Path $resolvedOutput "$supplementJob.pdf"
foreach ($pdf in @($completePdf, $supplementPdf)) {
  if (-not (Test-Path -LiteralPath $pdf -PathType Leaf)) { throw "Expected PDF is missing: $pdf" }
  if ((Get-Item -LiteralPath $pdf).Length -le 0) { throw "Expected PDF is empty: $pdf" }
}

$completePages = Get-PdfPageCount -Path $completePdf
$supplementPages = Get-PdfPageCount -Path $supplementPdf
if ($completePages -ne $expectedCompletePages) {
  throw "Screen reader has $completePages pages; expected $expectedCompletePages"
}
if ($supplementPages -ne $expectedSupplementPages) {
  throw "Screen supplement has $supplementPages pages; expected $expectedSupplementPages"
}

$completeHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $completePdf).Hash
$supplementHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $supplementPdf).Hash
foreach ($expected in @($ExpectedCompleteSha256, $ExpectedSupplementSha256)) {
  if (-not [string]::IsNullOrWhiteSpace($expected) -and $expected -notmatch "^[0-9A-Fa-f]{64}$") {
    throw "An expected SHA-256 value is not exactly 64 hexadecimal characters"
  }
}
if (-not [string]::IsNullOrWhiteSpace($ExpectedCompleteSha256) -and
    $completeHash -ne $ExpectedCompleteSha256.ToUpperInvariant()) {
  throw "Screen reader SHA-256 mismatch: expected $ExpectedCompleteSha256, got $completeHash"
}
if (-not [string]::IsNullOrWhiteSpace($ExpectedSupplementSha256) -and
    $supplementHash -ne $ExpectedSupplementSha256.ToUpperInvariant()) {
  throw "Screen supplement SHA-256 mismatch: expected $ExpectedSupplementSha256, got $supplementHash"
}

if ($StageReleaseAssets) {
  $destinations = @(
    [pscustomobject]@{
      Source = $completePdf
      Destination = Join-Path $releaseRoot "05_OPENLOGIC_ar_COMPLETE_LINKED_READER_SCREEN_OLP-0722.pdf"
    }
    [pscustomobject]@{
      Source = $supplementPdf
      Destination = Join-Path $releaseRoot "06_OPENLOGIC_ar_CLOSURE_SUPPLEMENT_80_UNITS_SCREEN_OLP-0722.pdf"
    }
  )
  foreach ($item in $destinations) {
    if (Test-Path -LiteralPath $item.Destination) {
      throw "Refusing to overwrite an existing release asset: $($item.Destination)"
    }
    Copy-Item -LiteralPath $item.Source -Destination $item.Destination
  }
}

[pscustomobject]@{
  Version = "OLP-0722-SCREEN-20260818"
  ConceptDoi = $expectedConceptDoi
  CompletePdf = $completePdf
  CompletePages = $completePages
  CompleteSha256 = $completeHash
  SupplementPdf = $supplementPdf
  SupplementPages = $supplementPages
  SupplementSha256 = $supplementHash
  ReleaseAssetsStaged = [bool]$StageReleaseAssets
}
