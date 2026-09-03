param(
  [Parameter(Mandatory = $true)]
  [string]$FinalOutputDirectory,

  [Parameter(Mandatory = $true)]
  [string]$WorkDirectory,

  [switch]$ResumeExisting
)

$ErrorActionPreference = "Stop"
$releaseRoot = Split-Path -Parent $PSScriptRoot
$localeRoot = Join-Path $releaseRoot "source\locale\ar"
$qaScript = Join-Path $PSScriptRoot "qa_dual_notation_pdfs.py"
$fontBuilder = Join-Path $PSScriptRoot "make_machrek_digit_font.py"
$repairScript = Join-Path $PSScriptRoot "repair_rtl_link_rects_letter_ar.py"
$assemblerScript = Join-Path $PSScriptRoot "assemble_complete_722_reader.py"

$profiles = @(
  [pscustomobject]@{
    Name = "international"
    ReaderDriver = "open-logic-complete-ar-readable-letter-international.tex"
    SupplementDriver = "open-logic-closure-supplement-ar-readable-letter-international.tex"
    ReaderAsset = "00_OPENLOGIC_ar_COMPLETE_LINKED_READER_INTERNATIONAL_NOTATION_OLP-0722.pdf"
    SupplementAsset = "01_OPENLOGIC_ar_CLOSURE_SUPPLEMENT_80_UNITS_INTERNATIONAL_NOTATION_OLP-0722.pdf"
    CompleteAsset = "00_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_INTERNATIONAL_NOTATION_OLP-0722.pdf"
  },
  [pscustomobject]@{
    Name = "machrek"
    ReaderDriver = "open-logic-complete-ar-readable-letter-machrek.tex"
    SupplementDriver = "open-logic-closure-supplement-ar-readable-letter-machrek.tex"
    ReaderAsset = "02_OPENLOGIC_ar_COMPLETE_LINKED_READER_MACHREK_NOTATION_OLP-0722.pdf"
    SupplementAsset = "03_OPENLOGIC_ar_CLOSURE_SUPPLEMENT_80_UNITS_MACHREK_NOTATION_OLP-0722.pdf"
    CompleteAsset = "01_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_MACHREK_NOTATION_OLP-0722.pdf"
  }
)

foreach ($commandName in @("lualatex", "bibtex", "python")) {
  if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
    throw "Required command is unavailable: $commandName"
  }
}
if (-not (Test-Path -LiteralPath $fontBuilder -PathType Leaf)) {
  throw "Machrek digit-font builder is missing: $fontBuilder"
}
if (-not (Test-Path -LiteralPath $repairScript -PathType Leaf)) {
  throw "US-Letter RTL link repair is missing: $repairScript"
}
if (-not (Test-Path -LiteralPath $assemblerScript -PathType Leaf)) {
  throw "Complete 722-unit PDF assembler is missing: $assemblerScript"
}
& python -c "import pdfplumber, pypdf"
if ($LASTEXITCODE -ne 0) {
  throw "Python dependencies pdfplumber and pypdf are required"
}
foreach ($profile in $profiles) {
  foreach ($driverName in @($profile.ReaderDriver, $profile.SupplementDriver)) {
    $driver = Join-Path $localeRoot $driverName
    if (-not (Test-Path -LiteralPath $driver -PathType Leaf)) {
      throw "Notation-profile driver is missing: $driver"
    }
  }
}

foreach ($directory in @($FinalOutputDirectory, $WorkDirectory)) {
  if (Test-Path -LiteralPath $directory) {
    $existing = Get-ChildItem -LiteralPath $directory -Force | Select-Object -First 1
    if ($null -ne $existing -and -not $ResumeExisting) {
      throw "Build directory must be empty: $directory"
    }
  } else {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
  }
}
$resolvedFinal = (Resolve-Path -LiteralPath $FinalOutputDirectory).Path
$resolvedWork = (Resolve-Path -LiteralPath $WorkDirectory).Path
$outputArgument = "-output-directory=$resolvedWork"
$latexArguments = @(
  "-interaction=nonstopmode",
  "-halt-on-error",
  "-file-line-error",
  "-recorder",
  $outputArgument
)

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
    return -join ($hasher.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") })
  } finally {
    $hasher.Dispose()
  }
}

function Write-Utf8NoBom {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$Content
  )
  [IO.File]::WriteAllText($Path, $Content, [Text.UTF8Encoding]::new($false))
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
    # LuaLaTeX writes the authoritative log itself.  Suppress its very large
    # console transcript so an output transport limit cannot interrupt a
    # correct multi-pass build.
    & lualatex @latexArguments $Driver | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "$Stage LuaLaTeX pass $pass failed" }
    $logPath = Join-Path $resolvedWork "$Job.log"
    $logText = [IO.File]::ReadAllText($logPath)
    $rerunRequested =
      $logText.Contains("Label(s) may have changed. Rerun to get cross-references right.") -or
      $logText.Contains("Rerun to get cross-references right.") -or
      $logText.Contains("Rerun to get citations correct")
    $fingerprint = Get-ConvergenceFingerprint -Job $Job -Extensions $StateExtensions
    if ($null -ne $previous -and $fingerprint -eq $previous -and -not $rerunRequested) {
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

$oldSourceDateEpoch = [Environment]::GetEnvironmentVariable("SOURCE_DATE_EPOCH", "Process")
$oldForceSourceDate = [Environment]::GetEnvironmentVariable("FORCE_SOURCE_DATE", "Process")
$oldTimeZone = [Environment]::GetEnvironmentVariable("TZ", "Process")
$oldTexInputs = [Environment]::GetEnvironmentVariable("TEXINPUTS", "Process")

try {
  [Environment]::SetEnvironmentVariable("SOURCE_DATE_EPOCH", "1783874174", "Process")
  [Environment]::SetEnvironmentVariable("FORCE_SOURCE_DATE", "1", "Process")
  [Environment]::SetEnvironmentVariable("TZ", "UTC", "Process")
  $texInputs = if ([string]::IsNullOrEmpty($oldTexInputs)) {
    "$resolvedWork;"
  } else {
    "$resolvedWork;$oldTexInputs"
  }
  [Environment]::SetEnvironmentVariable("TEXINPUTS", $texInputs, "Process")

  Push-Location $localeRoot
  try {
    & python $fontBuilder
    if ($LASTEXITCODE -ne 0) { throw "Machrek digit-font build or provenance verification failed" }

    $convergence = @()
    foreach ($profile in $profiles) {
      $readerJob = [IO.Path]::GetFileNameWithoutExtension($profile.ReaderDriver)
      $supplementJob = [IO.Path]::GetFileNameWithoutExtension($profile.SupplementDriver)

      $readerCheckpointFiles = @(
        (Join-Path $resolvedWork "$readerJob.aux"),
        (Join-Path $resolvedWork "$readerJob.bbl"),
        (Join-Path $resolvedWork "$readerJob.pdf")
      )
      $resumeReader = $ResumeExisting -and
        (($readerCheckpointFiles | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf }).Count -eq $readerCheckpointFiles.Count)
      if (-not $resumeReader) {
        & lualatex @latexArguments $profile.ReaderDriver | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "$($profile.Name) reader LuaLaTeX pass 1 failed" }
        & bibtex (Join-Path $resolvedWork $readerJob) | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "$($profile.Name) reader BibTeX failed" }
      }
      $convergence += Invoke-ConvergentLuaLaTeX `
        -Driver $profile.ReaderDriver `
        -Job $readerJob `
        -Stage $(if ($resumeReader) { "$($profile.Name) reader (resumed)" } else { "$($profile.Name) reader" }) `
        -FirstPass 2 `
        -LastPass 6 `
        -StateExtensions @("aux", "bbl", "out", "pcr", "prb", "thm", "toc")

      $readerPdf = Join-Path $resolvedWork "$readerJob.pdf"
      $readerRawPdf = Join-Path $resolvedWork "$readerJob.raw-before-link-repair.pdf"
      $readerRepairReceipt = Join-Path $resolvedWork "$readerJob.rtl-link-rect-repair.json"
      Move-Item -LiteralPath $readerPdf -Destination $readerRawPdf
      & python $repairScript `
        --input $readerRawPdf `
        --output $readerPdf `
        --receipt $readerRepairReceipt
      if ($LASTEXITCODE -ne 0) { throw "$($profile.Name) reader link repair failed" }

      # xr-hyper reads the job AUX but records this exact released filename in
      # every cross-document action.  Keep a work-directory copy so the repair
      # and link validator can prove that the companion target exists.
      $readerReleaseAlias = Join-Path $resolvedWork $profile.ReaderAsset
      Copy-Item -LiteralPath $readerPdf -Destination $readerReleaseAlias

      $convergence += Invoke-ConvergentLuaLaTeX `
        -Driver $profile.SupplementDriver `
        -Job $supplementJob `
        -Stage "$($profile.Name) supplement" `
        -FirstPass 1 `
        -LastPass 5 `
        -StateExtensions @("aux", "out", "prb", "thm")

      $supplementPdf = Join-Path $resolvedWork "$supplementJob.pdf"
      $supplementRawPdf = Join-Path $resolvedWork "$supplementJob.raw-before-link-repair.pdf"
      $supplementRepairReceipt = Join-Path $resolvedWork "$supplementJob.rtl-link-rect-repair.json"
      Move-Item -LiteralPath $supplementPdf -Destination $supplementRawPdf
      & python $repairScript `
        --input $supplementRawPdf `
        --output $supplementPdf `
        --receipt $supplementRepairReceipt
      if ($LASTEXITCODE -ne 0) { throw "$($profile.Name) supplement link repair failed" }

      $readerLog = Join-Path $resolvedWork "$readerJob.log"
      $supplementLog = Join-Path $resolvedWork "$supplementJob.log"
      foreach ($log in @($readerLog, $supplementLog)) {
        $logText = [IO.File]::ReadAllText($log)
        if ($logText.Contains("Missing character:")) {
          throw "Missing glyph diagnostic in $log"
        }
        if (-not $logText.Contains("OL-NOTATION-PROFILE=$($profile.Name)")) {
          throw "Notation-profile marker is missing from $log"
        }
        if (-not $logText.Contains("OL-NOTATION-FORMULA-DIRECTION=LTR")) {
          throw "Formula-direction marker is missing from $log"
        }
        if ($logText.Contains("Label(s) may have changed. Rerun to get cross-references right.") -or
            $logText.Contains("Rerun to get cross-references right.") -or
            $logText.Contains("Rerun to get citations correct")) {
          throw "Final TeX log still requests another pass: $log"
        }
        if ($profile.Name -eq "machrek") {
          if (-not $logText.Contains("OL-NOTATION-MATH-SOURCE-DIGITS=U+0030--U+0039")) {
            throw "Machrek semantic source-digit marker is missing from $log"
          }
          if (-not $logText.Contains("OL-NOTATION-MATH-VISUAL-DIGITS=U+0660--U+0669")) {
            throw "Machrek visual digit marker is missing from $log"
          }
          if (-not $logText.Contains("OL-NOTATION-MATH-DIGIT-FONT=OpenLogicMachrekDigits-Regular")) {
            throw "Machrek digit-font marker is missing from $log"
          }
        }
      }

      foreach ($pdf in @($readerPdf, $supplementPdf)) {
        if (-not (Test-Path -LiteralPath $pdf -PathType Leaf) -or (Get-Item -LiteralPath $pdf).Length -le 0) {
          throw "Expected nonempty PDF is missing: $pdf"
        }
      }
      Copy-Item -LiteralPath $readerPdf -Destination (Join-Path $resolvedFinal $profile.ReaderAsset)
      Copy-Item -LiteralPath $supplementPdf -Destination (Join-Path $resolvedFinal $profile.SupplementAsset)
      Copy-Item -LiteralPath $readerRepairReceipt -Destination (Join-Path $resolvedFinal "$($profile.ReaderAsset).rtl-link-rect-repair.json")
      Copy-Item -LiteralPath $supplementRepairReceipt -Destination (Join-Path $resolvedFinal "$($profile.SupplementAsset).rtl-link-rect-repair.json")
    }
    $convergenceJson = $convergence | ConvertTo-Json -Depth 4
    Write-Utf8NoBom -Path (Join-Path $resolvedFinal "BUILD_CONVERGENCE.json") -Content ($convergenceJson + "`n")
  } finally {
    Pop-Location
  }
} finally {
  [Environment]::SetEnvironmentVariable("SOURCE_DATE_EPOCH", $oldSourceDateEpoch, "Process")
  [Environment]::SetEnvironmentVariable("FORCE_SOURCE_DATE", $oldForceSourceDate, "Process")
  [Environment]::SetEnvironmentVariable("TZ", $oldTimeZone, "Process")
  [Environment]::SetEnvironmentVariable("TEXINPUTS", $oldTexInputs, "Process")
}

$qaOutput = Join-Path $resolvedFinal "OPENLOGIC_ar_DUAL_NOTATION_PDF_QA.json"
& python $qaScript `
  --international-reader (Join-Path $resolvedFinal $profiles[0].ReaderAsset) `
  --international-supplement (Join-Path $resolvedFinal $profiles[0].SupplementAsset) `
  --machrek-reader (Join-Path $resolvedFinal $profiles[1].ReaderAsset) `
  --machrek-supplement (Join-Path $resolvedFinal $profiles[1].SupplementAsset) `
  --output $qaOutput
if ($LASTEXITCODE -ne 0) {
  throw "Dual-notation PDF QA failed"
}

foreach ($profile in $profiles) {
  $completePdf = Join-Path $resolvedFinal $profile.CompleteAsset
  $assemblyReceipt = $completePdf.Replace(".pdf", ".assembly.json")
  if ($ResumeExisting -and
      (Test-Path -LiteralPath $completePdf -PathType Leaf) -and
      (Test-Path -LiteralPath $assemblyReceipt -PathType Leaf)) {
    $existingReceipt = Get-Content -LiteralPath $assemblyReceipt -Raw | ConvertFrom-Json
    if ($existingReceipt.status -ne "PASS") {
      throw "Existing complete-reader assembly receipt is not PASS: $assemblyReceipt"
    }
  } else {
    if ((Test-Path -LiteralPath $completePdf) -or
        (Test-Path -LiteralPath $assemblyReceipt)) {
      throw "Refusing to overwrite incomplete standalone assembly pair: $completePdf"
    }
    & python $assemblerScript `
      --reader (Join-Path $resolvedFinal $profile.ReaderAsset) `
      --closure (Join-Path $resolvedFinal $profile.SupplementAsset) `
      --output $completePdf `
      --receipt $assemblyReceipt `
      --profile $profile.Name
    if ($LASTEXITCODE -ne 0) {
      throw "$($profile.Name) complete 722-unit assembly failed"
    }
  }
}

$artifacts = @()
foreach ($profile in $profiles) {
  foreach ($asset in @($profile.ReaderAsset, $profile.SupplementAsset)) {
    $path = Join-Path $resolvedFinal $asset
    $artifacts += [pscustomobject]@{
      Profile = $profile.Name
      Role = "build-component"
      File = $asset
      Bytes = (Get-Item -LiteralPath $path).Length
      SHA256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    }
  }
  $completePath = Join-Path $resolvedFinal $profile.CompleteAsset
  $artifacts += [pscustomobject]@{
    Profile = $profile.Name
    Role = "standalone-release"
    File = $profile.CompleteAsset
    Bytes = (Get-Item -LiteralPath $completePath).Length
    SHA256 = (Get-FileHash -LiteralPath $completePath -Algorithm SHA256).Hash
  }
}
$artifactsJson = $artifacts | ConvertTo-Json -Depth 4
Write-Utf8NoBom -Path (Join-Path $resolvedFinal "BUILD_ARTIFACTS.json") -Content ($artifactsJson + "`n")
$artifacts
