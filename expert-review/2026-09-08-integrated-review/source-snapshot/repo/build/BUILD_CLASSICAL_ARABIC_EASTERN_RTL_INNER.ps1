param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("primary", "replay")]
  [string]$BuildRole,

  [Parameter(Mandatory = $true)]
  [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._-]{7,79}$')]
  [string]$BuildRunId,

  [Parameter(Mandatory = $true)]
  [string]$SourceClosureReceipt,

  [Parameter(Mandatory = $true)]
  [string]$RTLClosureReceipt,

  [Parameter(Mandatory = $true)]
  [string]$MaterializationReceipt,

  [string]$ReferenceBuildReceipt = "",

  [Parameter(Mandatory = $true)]
  [string]$FinalOutputDirectory,

  [Parameter(Mandatory = $true)]
  [string]$WorkDirectory
)

$ErrorActionPreference = "Stop"
$guardWorkingDirectory = (Get-Location).ProviderPath
$releaseRoot = Split-Path -Parent $PSScriptRoot
$localeRoot = Join-Path $releaseRoot "source\locale\ar-classical"
$readerDriverName = "open-logic-complete-ar-classical-eastern-rtl.tex"
$closureDriverName = "open-logic-closure-supplement-ar-classical-eastern-rtl.tex"
$readerJob = [IO.Path]::GetFileNameWithoutExtension($readerDriverName)
$closureJob = [IO.Path]::GetFileNameWithoutExtension($closureDriverName)
$readerAsset = "OPENLOGIC_ar_CLASSICAL_LINKED_READER_642_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf"
$closureAsset = "OPENLOGIC_ar_CLASSICAL_CLOSURE_SUPPLEMENT_80_UNITS_EASTERN_ARABIC_RTL_OLP-0722.pdf"
$completeAsset = "OPENLOGIC_ar_CLASSICAL_COMPLETE_722_UNIT_READER_EASTERN_ARABIC_RTL_OLP-0722.pdf"
$repairScript = Join-Path $PSScriptRoot "repair_rtl_link_rects_letter_ar.py"
$routingScript = Join-Path $PSScriptRoot "verify_classical_reader_routing.py"
$assemblerScript = Join-Path $PSScriptRoot "assemble_classical_722_reader.py"
$materializerScript = Join-Path $PSScriptRoot "materialize_classical_notation.py"
$rtlClosureValidator = Join-Path $PSScriptRoot `
  "validate_classical_rtl_closure_receipt.py"
$buildContract = Join-Path $PSScriptRoot "classical_reader_build_contract.py"
$defaultMaterializationReceipt = Join-Path $releaseRoot `
  "evidence\classical\NOTATION_MATERIALIZATION_RECEIPT.json"

if ($BuildRole -eq "replay" -and
    [string]::IsNullOrWhiteSpace($ReferenceBuildReceipt)) {
  throw "Replay builds require ReferenceBuildReceipt"
}
if ($BuildRole -eq "primary" -and
    -not [string]::IsNullOrWhiteSpace($ReferenceBuildReceipt)) {
  throw "Primary builds must not supply ReferenceBuildReceipt"
}

foreach ($commandName in @("lualatex", "bibtex", "python")) {
  if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
    throw "Required command is unavailable: $commandName"
  }
}
foreach ($required in @(
  (Join-Path $localeRoot $readerDriverName),
  (Join-Path $localeRoot $closureDriverName),
  $repairScript,
  $routingScript,
  $assemblerScript,
  $materializerScript,
  $rtlClosureValidator,
  $buildContract,
  $SourceClosureReceipt,
  $RTLClosureReceipt,
  $MaterializationReceipt
)) {
  if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
    throw "Required Classical build input is missing: $required"
  }
}
if ((Resolve-Path -LiteralPath $MaterializationReceipt).Path -ne
    (Resolve-Path -LiteralPath $defaultMaterializationReceipt).Path) {
  throw "MaterializationReceipt must be the generator's canonical repository receipt"
}
$resolvedSourceClosureReceipt = (Resolve-Path -LiteralPath $SourceClosureReceipt).Path
$resolvedRTLClosureReceipt = (Resolve-Path -LiteralPath $RTLClosureReceipt).Path
$resolvedMaterializationReceipt = (Resolve-Path -LiteralPath $MaterializationReceipt).Path
$resolvedReferenceBuildReceipt = $null
if ($BuildRole -eq "replay") {
  if (-not (Test-Path -LiteralPath $ReferenceBuildReceipt -PathType Leaf)) {
    throw "Reference primary build receipt is missing: $ReferenceBuildReceipt"
  }
  $resolvedReferenceBuildReceipt = (Resolve-Path -LiteralPath $ReferenceBuildReceipt).Path
}

# Bind the integrated reader build to the exact current isolated RTL-math
# sources and to the guarded primary/replay products before any TeX engine can
# run.  The validator rejects duplicate JSON keys, stale receipts, failed or
# incomplete runtime predicates, and manifest/guard identity drift.
& python $rtlClosureValidator `
  --repo $releaseRoot `
  --receipt $resolvedRTLClosureReceipt
if ($LASTEXITCODE -ne 0) {
  throw "Classical RTL closure receipt preflight failed"
}
& python -c "import pypdf"
if ($LASTEXITCODE -ne 0) {
  throw "Python dependency pypdf is required"
}

# This runs inside the already acquired machine-wide TeX mutex and before the
# first engine process.  It recomputes all 722 transformations and refuses a
# working snapshot, an unknown source-closure schema, source drift, output
# drift, a failed inverse, or even one untreated notation candidate.
& python $materializerScript `
  --repo $releaseRoot `
  --mode final `
  --action verify `
  --source-closure $resolvedSourceClosureReceipt
if ($LASTEXITCODE -ne 0) {
  throw "Final Classical notation materialization preflight failed"
}
$materializationData = Get-Content -LiteralPath $resolvedMaterializationReceipt `
  -Raw -Encoding UTF8 | ConvertFrom-Json
if ($materializationData.schema -ne
    "openlogic-classical-notation-materialization-receipt-v1" -or
    $materializationData.status -ne "PASS" -or
    $materializationData.release_eligible -ne $true -or
    $materializationData.mode -ne "final" -or
    $materializationData.summary.units -ne 722 -or
    $materializationData.summary.untreated_candidates -ne 0 -or
    $materializationData.summary.source_files_with_failed_inverse -ne 0) {
  throw "Canonical notation-materialization receipt is not a 722-unit final PASS"
}
$materializationCoverageMarker =
  "OL-CLASSICAL-MATERIALIZATION-COVERAGE=formulas-{0};ascii-{1};text-digits-{2};greek-{3};replacements-{4};untreated-0" -f `
    $materializationData.summary.formula_segments, `
    $materializationData.summary.ascii_candidate_scalars, `
    $materializationData.summary.text_digit_candidate_scalars, `
    $materializationData.summary.greek_candidate_commands, `
    $materializationData.summary.replacement_records
$requiredLogMarkers = @(
  "OL-CLASSICAL-EDITION=classical-eastern-rtl-v1",
  "OL-CLASSICAL-CONTENT-LOCALE=ar-classical-presentation",
  "OL-CLASSICAL-PRINTED-DIGITS=U+0660--U+0669",
  "OL-CLASSICAL-LETTERS=typed-opt-in-nucleus-v1",
  "OL-ARABIC-SETS=typed-dynamic-xits-v2",
  "OL-ARABIC-SETS-NAT-INCLUDES-ZERO=true",
  "OL-CLASSICAL-RTL-MATH-SOURCE-ORDER=unchanged",
  "OL-CLASSICAL-RTL-MATH=native-mathdirection-TRT",
  "OL-CLASSICAL-RTL-MATH-MIRRORING=typed-registry-and-scoped-ltr-v5",
  "OL-CLASSICAL-RTL-MATH-NONDIRECTIONAL-ACCENTS=boxed-registry-v3",
  "OL-CLASSICAL-RTL-MATH-TAGS=physical-left-v1",
  "OL-CLASSICAL-NAT-INCLUDES-ZERO=true",
  "OL-CLASSICAL-MATERIALIZATION=source-addressed-wrappers-v2",
  "OL-CLASSICAL-MATERIALIZATION-STATUS=PASS",
  "OL-CLASSICAL-MATERIALIZATION-MODE=final",
  "OL-CLASSICAL-MATERIALIZATION-RELEASE-ELIGIBLE=true",
  "OL-CLASSICAL-MATERIALIZATION-SOURCE-TREE-SHA256=$($materializationData.source_tree_sha256)",
  "OL-CLASSICAL-MATERIALIZATION-PRESENTATION-TREE-SHA256=$($materializationData.presentation_tree_sha256)",
  $materializationCoverageMarker
)
if ($requiredLogMarkers.Count -lt 19 -or
    @($requiredLogMarkers | Where-Object { [string]::IsNullOrWhiteSpace($_) }).Count -ne 0) {
  throw "Classical log-marker contract is incomplete before TeX"
}

foreach ($directory in @($FinalOutputDirectory, $WorkDirectory)) {
  if (Test-Path -LiteralPath $directory) {
    $existing = Get-ChildItem -LiteralPath $directory -Force |
      Where-Object { $_.Name -ne "TEX_MUTEX_RECEIPT.json" } |
      Select-Object -First 1
    if ($null -ne $existing) {
      throw "Build directory must be empty: $directory"
    }
  } else {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
  }
}

$resolvedFinal = (Resolve-Path -LiteralPath $FinalOutputDirectory).Path
$resolvedWork = (Resolve-Path -LiteralPath $WorkDirectory).Path
$resolvedLocale = (Resolve-Path -LiteralPath $localeRoot).Path
$resolvedSource = (Resolve-Path -LiteralPath (Join-Path $releaseRoot "source")).Path
if ($resolvedFinal -eq $resolvedWork) {
  throw "Final and working directories must be distinct"
}
foreach ($destination in @($resolvedFinal, $resolvedWork)) {
  if ($destination.StartsWith($resolvedSource + [IO.Path]::DirectorySeparatorChar,
      [StringComparison]::OrdinalIgnoreCase)) {
    throw "Build output must not be written beneath any source tree"
  }
}
if ($resolvedFinal.StartsWith($resolvedWork + [IO.Path]::DirectorySeparatorChar,
    [StringComparison]::OrdinalIgnoreCase) -or
    $resolvedWork.StartsWith($resolvedFinal + [IO.Path]::DirectorySeparatorChar,
    [StringComparison]::OrdinalIgnoreCase)) {
  throw "Final and working directories must not contain one another"
}

# Capture authoritative source/presentation/receipt/tool bytes before the first
# engine. Replay references are consumed and validated here, not merely accepted
# as command-line parameters. This capture and all immediate QA remain guarded.
$inputCapturePath = Join-Path $resolvedWork "CLASSICAL_BUILD_INPUTS.json"
$prepareArguments = @(
  $buildContract, "prepare", "--repo", $releaseRoot,
  "--role", $BuildRole, "--run-id", $BuildRunId,
  "--source-closure", $resolvedSourceClosureReceipt,
  "--rtl-closure", $resolvedRTLClosureReceipt,
  "--materialization", $resolvedMaterializationReceipt,
  "--work", $resolvedWork, "--final", $resolvedFinal,
  "--shell", (Get-Process -Id $PID).Path,
  "--python", (Get-Command python -CommandType Application | Select-Object -First 1).Source,
  "--lualatex", (Get-Command lualatex -CommandType Application | Select-Object -First 1).Source,
  "--bibtex", (Get-Command bibtex -CommandType Application | Select-Object -First 1).Source,
  "--inner-pid", $PID, "--guard-working-directory", $guardWorkingDirectory,
  "--output", $inputCapturePath
)
if ($BuildRole -eq "replay") {
  $prepareArguments += @("--reference", $resolvedReferenceBuildReceipt)
}
& python @prepareArguments
if ($LASTEXITCODE -ne 0) { throw "Classical build input/reference capture failed" }

$outputArgument = "-output-directory=$resolvedWork"
$latexArguments = @(
  "-interaction=nonstopmode",
  "-halt-on-error",
  "-file-line-error",
  "-recorder",
  "-synctex=1",
  $outputArgument
)

function Write-Utf8NoBom {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$Content
  )
  [IO.File]::WriteAllText(
    $Path, $Content, [Text.UTF8Encoding]::new($false)
  )
}

function Get-ConvergenceFingerprint {
  param(
    [Parameter(Mandatory = $true)][string]$Job,
    [Parameter(Mandatory = $true)][string[]]$Extensions
  )
  $entries = foreach ($extension in $Extensions) {
    $path = Join-Path $resolvedWork "$Job.$extension"
    if (Test-Path -LiteralPath $path -PathType Leaf) {
      "${extension}:$((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash)"
    }
  }
  if ($entries.Count -eq 0) {
    throw "No convergence-state files exist for $Job"
  }
  $bytes = [Text.Encoding]::UTF8.GetBytes(($entries -join "`n"))
  $hasher = [Security.Cryptography.SHA256]::Create()
  try {
    return -join ($hasher.ComputeHash($bytes) |
      ForEach-Object { $_.ToString("x2") })
  } finally {
    $hasher.Dispose()
  }
}

function Invoke-ConvergentLuaLaTeX {
  param(
    [Parameter(Mandatory = $true)][string]$Driver,
    [Parameter(Mandatory = $true)][string]$Job,
    [Parameter(Mandatory = $true)][string]$Stage,
    [Parameter(Mandatory = $true)][int]$FirstPass,
    [Parameter(Mandatory = $true)][int]$LastPass,
    [Parameter(Mandatory = $true)][string[]]$StateExtensions
  )
  $previous = $null
  foreach ($pass in $FirstPass..$LastPass) {
    & lualatex @latexArguments $Driver | Out-Null
    if ($LASTEXITCODE -ne 0) {
      throw "$Stage LuaLaTeX pass $pass failed"
    }
    $logPath = Join-Path $resolvedWork "$Job.log"
    $logText = [IO.File]::ReadAllText($logPath)
    $rerunRequested =
      $logText.Contains("Label(s) may have changed. Rerun to get cross-references right.") -or
      $logText.Contains("Rerun to get cross-references right.") -or
      $logText.Contains("Rerun to get citations correct")
    $fingerprint = Get-ConvergenceFingerprint `
      -Job $Job -Extensions $StateExtensions
    if ($null -ne $previous -and $fingerprint -eq $previous -and
        -not $rerunRequested) {
      return [pscustomobject]@{
        Stage = $Stage
        FinalPass = $pass
        StateSHA256 = $fingerprint.ToUpperInvariant()
        RerunRequested = $false
      }
    }
    $previous = $fingerprint
  }
  throw "$Stage did not converge by LuaLaTeX pass $LastPass"
}

function Assert-ClassicalLog {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$Component,
    [Parameter(Mandatory = $true)][string[]]$RequiredMarkers
  )
  $text = [IO.File]::ReadAllText($Path)
  # TeX wraps long typeout records at max_print_line, including SHA256 markers.
  # Remove only physical newlines; retain every other marker character.
  $unwrapped = $text.Replace("`r", "").Replace("`n", "")
  foreach ($forbidden in @(
    "Missing character:",
    "There were undefined references.",
    "There were undefined citations.",
    "There were multiply-defined labels.",
    "Label(s) may have changed. Rerun to get cross-references right.",
    "Rerun to get cross-references right.",
    "Rerun to get citations correct"
  )) {
    if ($text.Contains($forbidden)) {
      throw "$Component final TeX log contains: $forbidden"
    }
  }
  foreach ($required in $RequiredMarkers) {
    if (-not $unwrapped.Contains($required)) {
      throw "$Component final TeX log lacks required marker: $required"
    }
  }
}

function Get-ArtifactRecord {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$Role
  )
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    throw "Expected artifact is missing: $Path"
  }
  $item = Get-Item -LiteralPath $Path
  if ($item.Length -le 0) {
    throw "Expected artifact is empty: $Path"
  }
  return [ordered]@{
    Role = $Role
    File = $item.Name
    Bytes = $item.Length
    SHA256 = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
  }
}

$oldSourceDateEpoch = [Environment]::GetEnvironmentVariable(
  "SOURCE_DATE_EPOCH", "Process"
)
$oldForceSourceDate = [Environment]::GetEnvironmentVariable(
  "FORCE_SOURCE_DATE", "Process"
)
$oldTimeZone = [Environment]::GetEnvironmentVariable("TZ", "Process")
$oldTexInputs = [Environment]::GetEnvironmentVariable("TEXINPUTS", "Process")
$oldTemp = [Environment]::GetEnvironmentVariable("TEMP", "Process")
$oldTmp = [Environment]::GetEnvironmentVariable("TMP", "Process")
$convergence = @()

try {
  [Environment]::SetEnvironmentVariable(
    "SOURCE_DATE_EPOCH", "1783874174", "Process"
  )
  [Environment]::SetEnvironmentVariable("FORCE_SOURCE_DATE", "1", "Process")
  [Environment]::SetEnvironmentVariable("TZ", "UTC", "Process")
  [Environment]::SetEnvironmentVariable("TEMP", $resolvedWork, "Process")
  [Environment]::SetEnvironmentVariable("TMP", $resolvedWork, "Process")
  $texInputs = if ([string]::IsNullOrEmpty($oldTexInputs)) {
    "$resolvedWork;"
  } else {
    "$resolvedWork;$oldTexInputs"
  }
  [Environment]::SetEnvironmentVariable("TEXINPUTS", $texInputs, "Process")

  Push-Location $resolvedLocale
  try {
    & lualatex @latexArguments $readerDriverName | Out-Null
    if ($LASTEXITCODE -ne 0) {
      throw "Classical reader LuaLaTeX pass 1 failed"
    }
    & bibtex (Join-Path $resolvedWork $readerJob) | Out-Null
    if ($LASTEXITCODE -ne 0) {
      throw "Classical reader BibTeX failed"
    }
    $convergence += Invoke-ConvergentLuaLaTeX `
      -Driver $readerDriverName `
      -Job $readerJob `
      -Stage "Classical canonical reader" `
      -FirstPass 2 `
      -LastPass 7 `
      -StateExtensions @("aux", "bbl", "out", "pcr", "prb", "thm", "toc")

    $readerPdf = Join-Path $resolvedWork "$readerJob.pdf"
    $readerRawPdf = Join-Path $resolvedWork "$readerJob.raw-before-link-repair.pdf"
    $readerRepairReceipt = Join-Path $resolvedWork "$readerJob.rtl-link-rect-repair.json"
    Move-Item -LiteralPath $readerPdf -Destination $readerRawPdf
    & python $repairScript `
      --input $readerRawPdf `
      --output $readerPdf `
      --receipt $readerRepairReceipt
    if ($LASTEXITCODE -ne 0) {
      throw "Classical reader link repair failed"
    }
    Copy-Item -LiteralPath $readerPdf `
      -Destination (Join-Path $resolvedWork $readerAsset)

    $convergence += Invoke-ConvergentLuaLaTeX `
      -Driver $closureDriverName `
      -Job $closureJob `
      -Stage "Classical closure component" `
      -FirstPass 1 `
      -LastPass 6 `
      -StateExtensions @("aux", "out", "pcr", "prb", "thm", "toc")

    $closurePdf = Join-Path $resolvedWork "$closureJob.pdf"
    $closureRawPdf = Join-Path $resolvedWork "$closureJob.raw-before-link-repair.pdf"
    $closureRepairReceipt = Join-Path $resolvedWork "$closureJob.rtl-link-rect-repair.json"
    Move-Item -LiteralPath $closurePdf -Destination $closureRawPdf
    & python $repairScript `
      --input $closureRawPdf `
      --output $closurePdf `
      --receipt $closureRepairReceipt
    if ($LASTEXITCODE -ne 0) {
      throw "Classical closure link repair failed"
    }
  } finally {
    Pop-Location
  }
} finally {
  [Environment]::SetEnvironmentVariable(
    "SOURCE_DATE_EPOCH", $oldSourceDateEpoch, "Process"
  )
  [Environment]::SetEnvironmentVariable(
    "FORCE_SOURCE_DATE", $oldForceSourceDate, "Process"
  )
  [Environment]::SetEnvironmentVariable("TZ", $oldTimeZone, "Process")
  [Environment]::SetEnvironmentVariable("TEXINPUTS", $oldTexInputs, "Process")
  [Environment]::SetEnvironmentVariable("TEMP", $oldTemp, "Process")
  [Environment]::SetEnvironmentVariable("TMP", $oldTmp, "Process")
}

$readerLog = Join-Path $resolvedWork "$readerJob.log"
$closureLog = Join-Path $resolvedWork "$closureJob.log"
Assert-ClassicalLog -Path $readerLog -Component "reader" `
  -RequiredMarkers $requiredLogMarkers
Assert-ClassicalLog -Path $closureLog -Component "closure" `
  -RequiredMarkers $requiredLogMarkers

foreach ($required in @(
  (Join-Path $resolvedWork "$readerJob.synctex.gz"),
  (Join-Path $resolvedWork "$closureJob.synctex.gz"),
  (Join-Path $resolvedWork "$readerJob.fls"),
  (Join-Path $resolvedWork "$closureJob.fls")
)) {
  if (-not (Test-Path -LiteralPath $required -PathType Leaf) -or
      (Get-Item -LiteralPath $required).Length -le 0) {
    throw "Required SyncTeX/recorder product is missing: $required"
  }
}

$routingReceipt = Join-Path $resolvedFinal "CLASSICAL_READER_ROUTING_QA.json"
& python $routingScript `
  --repo $releaseRoot `
  --compile-root $resolvedLocale `
  --reader-fls (Join-Path $resolvedWork "$readerJob.fls") `
  --closure-fls (Join-Path $resolvedWork "$closureJob.fls") `
  --materialization-receipt $resolvedMaterializationReceipt `
  --output $routingReceipt
if ($LASTEXITCODE -ne 0) {
  throw "Classical 722-unit routing verification failed"
}

$readerOutput = Join-Path $resolvedFinal $readerAsset
$closureOutput = Join-Path $resolvedFinal $closureAsset
Copy-Item -LiteralPath (Join-Path $resolvedWork "$readerJob.pdf") `
  -Destination $readerOutput
Copy-Item -LiteralPath (Join-Path $resolvedWork "$closureJob.pdf") `
  -Destination $closureOutput
Copy-Item -LiteralPath (Join-Path $resolvedWork "$readerJob.synctex.gz") `
  -Destination (Join-Path $resolvedFinal $readerAsset.Replace(".pdf", ".synctex.gz"))
Copy-Item -LiteralPath (Join-Path $resolvedWork "$closureJob.synctex.gz") `
  -Destination (Join-Path $resolvedFinal $closureAsset.Replace(".pdf", ".synctex.gz"))
Copy-Item -LiteralPath (Join-Path $resolvedWork "$readerJob.rtl-link-rect-repair.json") `
  -Destination (Join-Path $resolvedFinal "$readerAsset.rtl-link-rect-repair.json")
Copy-Item -LiteralPath (Join-Path $resolvedWork "$closureJob.rtl-link-rect-repair.json") `
  -Destination (Join-Path $resolvedFinal "$closureAsset.rtl-link-rect-repair.json")

$completeOutput = Join-Path $resolvedFinal $completeAsset
$assemblyReceipt = $completeOutput.Replace(".pdf", ".assembly.json")
& python $assemblerScript `
  --reader $readerOutput `
  --closure $closureOutput `
  --output $completeOutput `
  --receipt $assemblyReceipt
if ($LASTEXITCODE -ne 0) {
  throw "Classical complete 722-unit assembly failed"
}

$artifacts = @(
  (Get-ArtifactRecord -Path $readerOutput -Role "canonical-reader-component"),
  (Get-ArtifactRecord -Path $closureOutput -Role "closure-component"),
  (Get-ArtifactRecord -Path $completeOutput -Role "standalone-722-unit-reader"),
  (Get-ArtifactRecord `
    -Path (Join-Path $resolvedFinal $readerAsset.Replace(".pdf", ".synctex.gz")) `
    -Role "reader-source-map"),
  (Get-ArtifactRecord `
    -Path (Join-Path $resolvedFinal $closureAsset.Replace(".pdf", ".synctex.gz")) `
    -Role "closure-source-map"),
  (Get-ArtifactRecord -Path $routingReceipt -Role "routing-receipt"),
  (Get-ArtifactRecord -Path $assemblyReceipt -Role "assembly-receipt"),
  (Get-ArtifactRecord `
    -Path (Join-Path $resolvedFinal "$readerAsset.rtl-link-rect-repair.json") `
    -Role "reader-link-repair-receipt"),
  (Get-ArtifactRecord `
    -Path (Join-Path $resolvedFinal "$closureAsset.rtl-link-rect-repair.json") `
    -Role "closure-link-repair-receipt")
)
foreach ($job in @($readerJob, $closureJob)) {
  foreach ($extension in @("log", "fls")) {
    $qaOutput = Join-Path $resolvedFinal "$job.$extension"
    Copy-Item -LiteralPath (Join-Path $resolvedWork "$job.$extension") -Destination $qaOutput
    $artifacts += Get-ArtifactRecord -Path $qaOutput -Role "$job-$extension"
  }
}

$buildReceiptPath = Join-Path $resolvedFinal "CLASSICAL_BUILD_COMPONENTS.json"
$buildReceipt = [ordered]@{
  Schema = "openlogic-classical-arabic-reader-build-v2"
  Status = "PENDING_GUARD_DRAIN"
  Edition = "classical-eastern-arabic-rtl"
  CompileRoot = "source/locale/ar-classical"
  Drivers = @($readerDriverName, $closureDriverName)
  TeXEngine = "LuaLaTeX"
  SyncTeX = [ordered]@{
    Enabled = $true
    Argument = "-synctex=1"
    RenamedWithComponentPDFs = $true
  }
  Coverage = [ordered]@{
    CanonicalReaderUnits = 642
    ClosureUnits = 80
    TotalUnits = 722
    MSAContentInputs = 0
  }
  Presentation = [ordered]@{
    PrintedDigits = "U+0660--U+0669"
    TypedMathematicalLetters = "Arabic Mathematical Alphabetic Symbols plus registered labels"
    TypedSetSymbols = $true
    NaturalNumbersIncludeZero = $true
    FormulaDirection = "RTL"
    SourceTokenOrder = "unchanged"
  }
  StableConceptDOI = "10.5281/zenodo.21921850"
  OutputDirectory = $resolvedFinal
  WorkingDirectory = $resolvedWork
  Convergence = $convergence
  Artifacts = $artifacts
}
Write-Utf8NoBom -Path $buildReceiptPath `
  -Content (($buildReceipt | ConvertTo-Json -Depth 8) + "`n")

# The inner tree cannot attest its own later drain. Rehash captured inputs,
# bind recorder dependencies, and compare all three replay PDFs while still
# guarded, then leave a pending production receipt for the outer caller.
& python $buildContract complete-inner `
  --capture $inputCapturePath --details $buildReceiptPath `
  --output (Join-Path $resolvedFinal "CLASSICAL_BUILD_PENDING.json")
if ($LASTEXITCODE -ne 0) { throw "Classical production/replay contract failed" }

$artifacts
