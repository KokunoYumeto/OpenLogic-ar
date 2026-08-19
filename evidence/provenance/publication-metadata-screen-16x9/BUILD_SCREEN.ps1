param(
  [string]$OutputDirectory = "",
  [string]$ExpectedCompleteSha256 = "4ED132D20A4E5D5F34DDC5DEC28AB0A6FDD4E96E75F61E1357BA6822F11B1200",
  [string]$ExpectedSupplementSha256 = "B45A1A034E7A1C0386188E2678221C0970A88CAE196F39558BC755E99DA1209E",
  [switch]$StageReleaseAssets
)

$ErrorActionPreference = "Stop"

$releaseRoot = Split-Path -Parent $PSScriptRoot
$localeRoot = Join-Path $releaseRoot "source\locale\ar"
$repairScript = Join-Path $PSScriptRoot "repair_rtl_link_rects_ar.py"
$completeDriverName = "open-logic-complete-ar-screen.tex"
$supplementDriverName = "open-logic-closure-supplement-ar-screen.tex"
$completeDriver = Join-Path $localeRoot $completeDriverName
$supplementDriver = Join-Path $localeRoot $supplementDriverName
$completeJob = [IO.Path]::GetFileNameWithoutExtension($completeDriverName)
$supplementJob = [IO.Path]::GetFileNameWithoutExtension($supplementDriverName)
$version = "OLP-0722-REFLOW-16X9-20260819"
$expectedConceptDoi = "10.5281/zenodo.21921850"
$metadataVersionDoi = "10.5281/zenodo.22015759"
$forbiddenPdfDois = @(
  "10.5281/zenodo.21921851",
  "10.5281/zenodo.21987686",
  $metadataVersionDoi
)
$expectedCompletePages = 1542
$expectedSupplementPages = 209
$expectedCompleteLinks = 3000
$expectedSupplementLinks = 138
$expectedCompleteRawSha256 = "9CE18B39DA14D522547A152834E054A670A4FB4418E7DE937307FA0320FFB66D"
$expectedSupplementRawSha256 = "46EE090911A3770F990C40039A513718324F2F00F0877887D28EE36A32CDC3FD"

foreach ($driver in @($completeDriver, $supplementDriver)) {
  if (-not (Test-Path -LiteralPath $driver -PathType Leaf)) {
    throw "Packaged 16:9 driver is missing: $driver"
  }
  $driverText = [IO.File]::ReadAllText($driver)
  if (-not $driverText.Contains($expectedConceptDoi)) {
    throw "Stable concept DOI is absent from $driver"
  }
  foreach ($forbiddenDoi in $forbiddenPdfDois) {
    if ($driverText.Contains($forbiddenDoi)) {
      throw "Version DOI must remain metadata-only and is forbidden in the PDF driver: $driver"
    }
  }
}

if (-not (Test-Path -LiteralPath $repairScript -PathType Leaf)) {
  throw "RTL link repair script is missing: $repairScript"
}

foreach ($commandName in @("lualatex", "bibtex", "python")) {
  if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
    throw "Required command is unavailable: $commandName"
  }
}

& python -c "import pdfplumber, pypdf"
if ($LASTEXITCODE -ne 0) {
  throw "Python dependencies pdfplumber and pypdf are required"
}

if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
  $OutputDirectory = Join-Path $PSScriptRoot "output-ar-screen-16x9-OLP-0722"
}
if (Test-Path -LiteralPath $OutputDirectory) {
  $existing = Get-ChildItem -LiteralPath $OutputDirectory -Force | Select-Object -First 1
  if ($null -ne $existing) {
    throw "Output directory must be empty: $OutputDirectory"
  }
} else {
  New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}
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
    if ($LASTEXITCODE -ne 0) { throw "16:9 reader LuaLaTeX pass 1 failed" }

    & bibtex (Join-Path $resolvedOutput $completeJob)
    if ($LASTEXITCODE -ne 0) { throw "16:9 reader BibTeX pass failed" }

    for ($pass = 2; $pass -le 3; $pass++) {
      & lualatex @latexArguments $completeDriverName
      if ($LASTEXITCODE -ne 0) { throw "16:9 reader LuaLaTeX pass $pass failed" }
    }

    for ($pass = 1; $pass -le 2; $pass++) {
      & lualatex @latexArguments $supplementDriverName
      if ($LASTEXITCODE -ne 0) { throw "16:9 supplement LuaLaTeX pass $pass failed" }
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
$completeRaw = Join-Path $resolvedOutput "$completeJob.raw-before-link-repair.pdf"
$supplementRaw = Join-Path $resolvedOutput "$supplementJob.raw-before-link-repair.pdf"
$completeEvidence = Join-Path $resolvedOutput "$completeJob.link-rect-repair-receipt.json"
$supplementEvidence = Join-Path $resolvedOutput "$supplementJob.link-rect-repair-receipt.json"

foreach ($pdf in @($completePdf, $supplementPdf)) {
  if (-not (Test-Path -LiteralPath $pdf -PathType Leaf)) {
    throw "Expected compiled PDF is missing: $pdf"
  }
}
Move-Item -LiteralPath $completePdf -Destination $completeRaw
Move-Item -LiteralPath $supplementPdf -Destination $supplementRaw

$completeRawHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $completeRaw).Hash
$supplementRawHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $supplementRaw).Hash
if ($completeRawHash -ne $expectedCompleteRawSha256) {
  throw "Raw reader SHA-256 mismatch: expected $expectedCompleteRawSha256, got $completeRawHash"
}
if ($supplementRawHash -ne $expectedSupplementRawSha256) {
  throw "Raw supplement SHA-256 mismatch: expected $expectedSupplementRawSha256, got $supplementRawHash"
}

& python $repairScript --input $completeRaw --output $completePdf --receipt $completeEvidence
if ($LASTEXITCODE -ne 0) { throw "Reader link-rectangle repair failed" }
& python $repairScript --input $supplementRaw --output $supplementPdf --receipt $supplementEvidence
if ($LASTEXITCODE -ne 0) { throw "Supplement link-rectangle repair failed" }

$pdfFactsProgram = @'
import json
import sys
from pypdf import PdfReader

reader = PdfReader(sys.argv[1])
root = reader.trailer["/Root"]
links = 0
overflow = 0
geometry_ok = True
rotation_ok = True
for page in reader.pages:
    media = [float(v) for v in page.mediabox]
    crop = [float(v) for v in page.cropbox]
    geometry_ok = geometry_ok and media == [0.0, 0.0, 960.0, 540.0] and crop == media
    rotation_ok = rotation_ok and int(page.get("/Rotate", 0)) == 0
    for ref in page.get("/Annots", []):
        annot = ref.get_object()
        if str(annot.get("/Subtype")) != "/Link":
            continue
        links += 1
        x0, y0, x1, y1 = [float(v) for v in annot["/Rect"]]
        if x0 < -0.01 or y0 < -0.01 or x1 > 960.01 or y1 > 540.01 or x1 < x0 or y1 < y0:
            overflow += 1
open_action = root.get("/OpenAction")
if hasattr(open_action, "get_object"):
    open_action = open_action.get_object()
if isinstance(open_action, dict):
    destination = open_action.get("/D")
else:
    destination = open_action
fit = str(destination[1]) if isinstance(destination, (list, tuple)) and len(destination) > 1 else ""
print(json.dumps({
    "pages": len(reader.pages),
    "encrypted": bool(reader.is_encrypted),
    "geometry_ok": geometry_ok,
    "rotation_ok": rotation_ok,
    "links": links,
    "link_overflow": overflow,
    "page_mode": str(root.get("/PageMode", "")),
    "page_layout": str(root.get("/PageLayout", "")),
    "open_view": fit,
}, separators=(",", ":")))
'@

function Get-PdfFacts {
  param([Parameter(Mandatory = $true)][string]$Path)
  $json = & python -c $pdfFactsProgram $Path
  if ($LASTEXITCODE -ne 0) { throw "PDF facts inspection failed for $Path" }
  return $json | ConvertFrom-Json
}

$completeFacts = Get-PdfFacts -Path $completePdf
$supplementFacts = Get-PdfFacts -Path $supplementPdf
$checks = @(
  @{Name="reader pages"; Actual=$completeFacts.pages; Expected=$expectedCompletePages},
  @{Name="supplement pages"; Actual=$supplementFacts.pages; Expected=$expectedSupplementPages},
  @{Name="reader links"; Actual=$completeFacts.links; Expected=$expectedCompleteLinks},
  @{Name="supplement links"; Actual=$supplementFacts.links; Expected=$expectedSupplementLinks},
  @{Name="reader link overflow"; Actual=$completeFacts.link_overflow; Expected=0},
  @{Name="supplement link overflow"; Actual=$supplementFacts.link_overflow; Expected=0}
)
foreach ($check in $checks) {
  if ($check.Actual -ne $check.Expected) {
    throw "$($check.Name) mismatch: expected $($check.Expected), got $($check.Actual)"
  }
}
foreach ($facts in @($completeFacts, $supplementFacts)) {
  if ($facts.encrypted -or -not $facts.geometry_ok -or -not $facts.rotation_ok) {
    throw "PDF encryption, geometry, or rotation gate failed"
  }
  if ($facts.page_mode -ne "/UseOutlines" -or $facts.page_layout -ne "/OneColumn" -or $facts.open_view -ne "/Fit") {
    throw "PDF viewer-preference gate failed"
  }
}

$completeHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $completePdf).Hash
$supplementHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $supplementPdf).Hash
foreach ($expected in @($ExpectedCompleteSha256, $ExpectedSupplementSha256)) {
  if ($expected -notmatch "^[0-9A-Fa-f]{64}$") {
    throw "An expected SHA-256 value is not exactly 64 hexadecimal characters"
  }
}
if ($completeHash -ne $ExpectedCompleteSha256.ToUpperInvariant()) {
  throw "Final reader SHA-256 mismatch: expected $ExpectedCompleteSha256, got $completeHash"
}
if ($supplementHash -ne $ExpectedSupplementSha256.ToUpperInvariant()) {
  throw "Final supplement SHA-256 mismatch: expected $ExpectedSupplementSha256, got $supplementHash"
}

if ($StageReleaseAssets) {
  $destinations = @(
    @{
      Source = $completePdf
      Destination = Join-Path $releaseRoot "05_OPENLOGIC_ar_COMPLETE_LINKED_READER_SCREEN_OLP-0722.pdf"
    },
    @{
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
  Version = $version
  MetadataVersionDoi = $metadataVersionDoi
  PdfConceptDoi = $expectedConceptDoi
  CompleteRawPdf = $completeRaw
  CompleteRawSha256 = $completeRawHash
  CompletePdf = $completePdf
  CompletePages = $completeFacts.pages
  CompleteLinks = $completeFacts.links
  CompleteSha256 = $completeHash
  SupplementRawPdf = $supplementRaw
  SupplementRawSha256 = $supplementRawHash
  SupplementPdf = $supplementPdf
  SupplementPages = $supplementFacts.pages
  SupplementLinks = $supplementFacts.links
  SupplementSha256 = $supplementHash
  ReleaseAssetsStaged = [bool]$StageReleaseAssets
}
