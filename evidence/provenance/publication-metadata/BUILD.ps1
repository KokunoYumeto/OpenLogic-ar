param(
  [string]$OutputDirectory = "",
  [string]$ExpectedCompleteSha256 = "",
  [string]$ExpectedSupplementSha256 = "",
  [switch]$StageReleaseAssets
)

$ErrorActionPreference = "Stop"

$releaseRoot = Split-Path -Parent $PSScriptRoot
$localeRoot = Join-Path $releaseRoot "source\locale\ar"
$completeDriverName = "open-logic-complete-ar.tex"
$supplementDriverName = "open-logic-closure-supplement-ar.tex"
$completeDriver = Join-Path $localeRoot $completeDriverName
$supplementDriver = Join-Path $localeRoot $supplementDriverName
$completeJob = [IO.Path]::GetFileNameWithoutExtension($completeDriverName)
$supplementJob = [IO.Path]::GetFileNameWithoutExtension($supplementDriverName)
$expectedVersionDoi = "10.5281/zenodo.21987686"
$obsoleteVersionDoi = "10.5281/zenodo." + "21921851"
$expectedCompletePages = 819
$expectedSupplementPages = 123

foreach ($driver in @($completeDriver, $supplementDriver)) {
  if (-not (Test-Path -LiteralPath $driver -PathType Leaf)) {
    throw "Packaged OLP-0722 driver is missing: $driver"
  }
  $driverText = [IO.File]::ReadAllText($driver)
  if (-not $driverText.Contains($expectedVersionDoi)) {
    throw "Reserved version DOI is absent from $driver"
  }
  if ($driverText.Contains($obsoleteVersionDoi)) {
    throw "Obsolete OLP-0010 version DOI remains in $driver"
  }
}

foreach ($commandName in @("lualatex", "bibtex", "pdfinfo")) {
  if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
    throw "Required command is unavailable: $commandName"
  }
}

if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
  $OutputDirectory = Join-Path $PSScriptRoot "output-ar-OLP-0722"
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
  $pdfInfoExitCode = $LASTEXITCODE
  if ($pdfInfoExitCode -ne 0) {
    throw "pdfinfo failed for $Path with exit code $pdfInfoExitCode"
  }
  $pageLine = $metadata | Where-Object { $_ -match "^Pages:\s+(\d+)\s*$" } | Select-Object -First 1
  if ($null -eq $pageLine) {
    throw "Unable to read the page count from $Path"
  }
  $pageMatch = [regex]::Match([string]$pageLine, "^Pages:\s+(\d+)\s*$")
  if (-not $pageMatch.Success) {
    throw "Unable to read the page count from $Path"
  }
  return [int]$pageMatch.Groups[1].Value
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
    if ($LASTEXITCODE -ne 0) { throw "Complete-reader LuaLaTeX pass 1 failed" }

    $bibtexJob = Join-Path $resolvedOutput $completeJob
    & bibtex $bibtexJob
    if ($LASTEXITCODE -ne 0) { throw "Complete-reader BibTeX pass failed" }

    for ($pass = 2; $pass -le 3; $pass++) {
      & lualatex @latexArguments $completeDriverName
      if ($LASTEXITCODE -ne 0) {
        throw "Complete-reader LuaLaTeX pass $pass failed"
      }
    }

    for ($pass = 1; $pass -le 2; $pass++) {
      & lualatex @latexArguments $supplementDriverName
      if ($LASTEXITCODE -ne 0) {
        throw "Closure-supplement LuaLaTeX pass $pass failed"
      }
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
  if (-not (Test-Path -LiteralPath $pdf -PathType Leaf)) {
    throw "Expected PDF is missing: $pdf"
  }
  if ((Get-Item -LiteralPath $pdf).Length -le 0) {
    throw "Expected PDF is empty: $pdf"
  }
}

$completePages = Get-PdfPageCount -Path $completePdf
$supplementPages = Get-PdfPageCount -Path $supplementPdf
if ($completePages -ne $expectedCompletePages) {
  throw "Complete reader has $completePages pages; expected $expectedCompletePages"
}
if ($supplementPages -ne $expectedSupplementPages) {
  throw "Closure supplement has $supplementPages pages; expected $expectedSupplementPages"
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
  throw "Complete-reader SHA-256 mismatch: expected $ExpectedCompleteSha256, got $completeHash"
}
if (-not [string]::IsNullOrWhiteSpace($ExpectedSupplementSha256) -and
    $supplementHash -ne $ExpectedSupplementSha256.ToUpperInvariant()) {
  throw "Closure-supplement SHA-256 mismatch: expected $ExpectedSupplementSha256, got $supplementHash"
}

if ($StageReleaseAssets) {
  $destinations = @(
    [pscustomobject]@{
      Source = $completePdf
      Destination = Join-Path $releaseRoot "00_OPENLOGIC_ar_COMPLETE_LINKED_READER_OLP-0722.pdf"
    }
    [pscustomobject]@{
      Source = $supplementPdf
      Destination = Join-Path $releaseRoot "01_OPENLOGIC_ar_CLOSURE_SUPPLEMENT_80_UNITS_OLP-0722.pdf"
    }
  )
  foreach ($item in $destinations) {
    $sourcePath = $item.Source
    $destinationPath = $item.Destination
    if (Test-Path -LiteralPath $destinationPath) {
      throw "Refusing to overwrite an existing release asset: $destinationPath"
    }
    Copy-Item -LiteralPath $sourcePath -Destination $destinationPath
  }
}

[pscustomobject]@{
  Version = "OLP-0722-20260818"
  CompletePdf = $completePdf
  CompletePages = $completePages
  CompleteSha256 = $completeHash
  SupplementPdf = $supplementPdf
  SupplementPages = $supplementPages
  SupplementSha256 = $supplementHash
  ReleaseAssetsStaged = [bool]$StageReleaseAssets
}
