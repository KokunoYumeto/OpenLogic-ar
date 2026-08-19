param(
  [Parameter(Mandatory = $true)]
  [string]$OutputPath
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$releaseRoot = Split-Path -Parent $PSScriptRoot
$inventoryRelative = "evidence\inventories\SCREEN_BUNDLE_SHA256.tsv"
$inventoryPath = Join-Path $releaseRoot $inventoryRelative
$fixedTimestamp = [DateTimeOffset]::new(2026, 8, 19, 0, 0, 0, [TimeSpan]::Zero)
$utf8 = [Text.UTF8Encoding]::new($false)
$tab = [char]9
$lf = [char]10

$entries = @(
  @{Source="build\BUILD_SCREEN_REQUIREMENTS.md"; Destination="build/BUILD_SCREEN_REQUIREMENTS.md"},
  @{Source="build\BUILD_SCREEN.ps1"; Destination="build/BUILD_SCREEN.ps1"},
  @{Source="build\BUILD_SCREEN_BUNDLE.ps1"; Destination="build/BUILD_SCREEN_BUNDLE.ps1"},
  @{Source="build\repair_rtl_link_rects_ar.py"; Destination="build/repair_rtl_link_rects_ar.py"},
  @{Source="evidence\SCREEN_LAYOUT_RELEASE.md"; Destination="README.md"},
  @{Source="evidence\PUBLIC_PATH_SANITIZATION_SCREEN.md"; Destination="evidence/PUBLIC_PATH_SANITIZATION.md"},
  @{Source="evidence\provenance\final-build-screen-16x9\PUBLIC_PATH_SANITIZATION_RECEIPT.json"; Destination="evidence/final-build-screen/PUBLIC_PATH_SANITIZATION_RECEIPT.json"},
  @{Source="evidence\provenance\final-build-screen-16x9\open-logic-complete-ar-screen.log"; Destination="evidence/final-build-screen/open-logic-complete-ar-screen.log"},
  @{Source="evidence\provenance\final-build-screen-16x9\open-logic-complete-ar-screen.fls"; Destination="evidence/final-build-screen/open-logic-complete-ar-screen.fls"},
  @{Source="evidence\provenance\final-build-screen-16x9\open-logic-complete-ar-screen.aux"; Destination="evidence/final-build-screen/open-logic-complete-ar-screen.aux"},
  @{Source="evidence\provenance\final-build-screen-16x9\open-logic-complete-ar-screen.bbl"; Destination="evidence/final-build-screen/open-logic-complete-ar-screen.bbl"},
  @{Source="evidence\provenance\final-build-screen-16x9\open-logic-complete-ar-screen.blg"; Destination="evidence/final-build-screen/open-logic-complete-ar-screen.blg"},
  @{Source="evidence\provenance\final-build-screen-16x9\open-logic-closure-supplement-ar-screen.log"; Destination="evidence/final-build-screen/open-logic-closure-supplement-ar-screen.log"},
  @{Source="evidence\provenance\final-build-screen-16x9\open-logic-closure-supplement-ar-screen.fls"; Destination="evidence/final-build-screen/open-logic-closure-supplement-ar-screen.fls"},
  @{Source="evidence\provenance\final-build-screen-16x9\open-logic-closure-supplement-ar-screen.aux"; Destination="evidence/final-build-screen/open-logic-closure-supplement-ar-screen.aux"},
  @{Source="evidence\final-qa\ARABIC_SCREEN_REFLOW_FINAL_QA.json"; Destination="evidence/final-qa/ARABIC_SCREEN_REFLOW_FINAL_QA.json"},
  @{Source="evidence\provenance\rtl-link-rect-repair\open-logic-complete-ar-screen.rtl-link-rect-repair.public.json"; Destination="evidence/link-repair/open-logic-complete-ar-screen.rtl-link-rect-repair.json"},
  @{Source="evidence\provenance\rtl-link-rect-repair\open-logic-closure-supplement-ar-screen.rtl-link-rect-repair.public.json"; Destination="evidence/link-repair/open-logic-closure-supplement-ar-screen.rtl-link-rect-repair.json"},
  @{Source="evidence\provenance\rtl-link-rect-repair\RAW_AND_FINAL_SHA256.tsv"; Destination="evidence/link-repair/RAW_AND_FINAL_SHA256.tsv"},
  @{Source="evidence\inventories\RAW_SCREEN_BUILD_EVIDENCE_SHA256.tsv"; Destination="inventories/RAW_SCREEN_BUILD_EVIDENCE_SHA256.tsv"},
  @{Source="evidence\inventories\SCREEN_SOURCE_BINDING_SHA256.tsv"; Destination="inventories/SCREEN_SOURCE_BINDING_SHA256.tsv"},
  @{Source=$inventoryRelative; Destination="inventories/SCREEN_BUNDLE_SHA256.tsv"},
  @{Source="source\locale\ar\open-logic-complete-ar-screen.tex"; Destination="source/locale/ar/open-logic-complete-ar-screen.tex"},
  @{Source="source\locale\ar\open-logic-closure-supplement-ar-screen.tex"; Destination="source/locale/ar/open-logic-closure-supplement-ar-screen.tex"}
)

$resolvedEntries = @()
$seen = @{}
foreach ($entry in $entries) {
  $sourcePath = Join-Path $releaseRoot $entry.Source
  if ($entry.Source -ne $inventoryRelative -and
      -not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
    throw "Bundle input is missing: $sourcePath"
  }
  if ($seen.ContainsKey($entry.Destination)) {
    throw "Duplicate ZIP destination: $($entry.Destination)"
  }
  $seen[$entry.Destination] = $true
  $resolvedEntries += [pscustomobject]@{
    Source = $sourcePath
    Destination = $entry.Destination
  }
}

$inventoryRows = @(
  ("sha256" + $tab + "bytes" + $tab + "path"),
  "# Every bundle file except this inventory; rows use ordinal ZIP paths."
)
foreach ($entry in ($resolvedEntries | Where-Object {$_.Destination -ne "inventories/SCREEN_BUNDLE_SHA256.tsv"} | Sort-Object Destination)) {
  $item = Get-Item -LiteralPath $entry.Source
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Source).Hash
  $inventoryRows += ($hash + $tab + $item.Length + $tab + $entry.Destination)
}
[IO.File]::WriteAllText($inventoryPath, (($inventoryRows -join $lf) + $lf), $utf8)

if (Test-Path -LiteralPath $OutputPath) {
  throw "Refusing to overwrite existing bundle: $OutputPath"
}
$parent = Split-Path -Parent $OutputPath
if ([string]::IsNullOrWhiteSpace($parent)) {
  $parent = (Get-Location).Path
}
if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
  throw "Bundle parent directory does not exist: $parent"
}

$stream = [IO.File]::Open($OutputPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
try {
  $archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Create, $true)
  try {
    foreach ($entry in ($resolvedEntries | Sort-Object Destination)) {
      $zipEntry = $archive.CreateEntry($entry.Destination, [IO.Compression.CompressionLevel]::Optimal)
      $zipEntry.LastWriteTime = $fixedTimestamp
      $input = [IO.File]::OpenRead($entry.Source)
      $output = $zipEntry.Open()
      try {
        $input.CopyTo($output)
      } finally {
        $output.Dispose()
        $input.Dispose()
      }
    }
  } finally {
    $archive.Dispose()
  }
} finally {
  $stream.Dispose()
}

$zip = [IO.Compression.ZipFile]::OpenRead($OutputPath)
try {
  if ($zip.Entries.Count -ne $resolvedEntries.Count) {
    throw "ZIP entry count mismatch"
  }
  foreach ($entry in $resolvedEntries) {
    $zipEntry = $zip.GetEntry($entry.Destination)
    if ($null -eq $zipEntry) {
      throw "ZIP entry missing after creation: $($entry.Destination)"
    }
    $sourceItem = Get-Item -LiteralPath $entry.Source
    if ([int64]$zipEntry.Length -ne [int64]$sourceItem.Length) {
      throw "ZIP entry byte count mismatch: $($entry.Destination)"
    }
    $algorithm = [Security.Cryptography.SHA256]::Create()
    $entryStream = $zipEntry.Open()
    try {
      $entryHash = ([BitConverter]::ToString($algorithm.ComputeHash($entryStream))).Replace("-", "")
    } finally {
      $entryStream.Dispose()
      $algorithm.Dispose()
    }
    $sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Source).Hash
    if ($entryHash -ne $sourceHash) {
      throw "ZIP entry SHA-256 mismatch: $($entry.Destination)"
    }
  }
} finally {
  $zip.Dispose()
}

$zipItem = Get-Item -LiteralPath $OutputPath
[pscustomobject]@{
  OutputPath = $zipItem.FullName
  Entries = $resolvedEntries.Count
  UncompressedBytes = [int64](($resolvedEntries | ForEach-Object {(Get-Item -LiteralPath $_.Source).Length} | Measure-Object -Sum).Sum)
  ZipBytes = [int64]$zipItem.Length
  ZipSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $OutputPath).Hash
  FixedEntryTimestampUtc = $fixedTimestamp.ToString("o")
  Verification = "PASS"
}
