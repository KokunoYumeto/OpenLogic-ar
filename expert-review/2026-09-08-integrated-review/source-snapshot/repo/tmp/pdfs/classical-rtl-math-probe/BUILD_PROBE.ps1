param([Parameter(Mandatory = $true)][string]$OutputDirectory)

$ErrorActionPreference = 'Stop'
$probeRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$repoRoot = [IO.Path]::GetFullPath((Join-Path $probeRoot '..\..\..'))
$workingDirectory = [IO.Path]::GetFullPath((Join-Path $repoRoot 'source\locale\ar'))
$manifest = $null
$manifestPath = $null

function Resolve-NewOutputDirectory {
  param([Parameter(Mandatory = $true)][string]$Value)
  if ([string]::IsNullOrWhiteSpace($Value)) {
    throw 'RTL-math probe output path must not be blank.'
  }
  $resolved = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Value)
  $resolved = [IO.Path]::GetFullPath($resolved)
  if (-not [IO.Path]::IsPathRooted($resolved) -or
      $resolved -ieq [IO.Path]::GetPathRoot($resolved)) {
    throw 'RTL-math probe output path must be a non-root absolute filesystem path.'
  }
  if (Test-Path -LiteralPath $resolved) {
    throw 'RTL-math probe output must not already exist.'
  }
  return $resolved
}

function Get-Identity {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$RecordedPath
  )
  $item = Get-Item -LiteralPath $Path -ErrorAction Stop
  if ($item.PSIsContainer) { throw "Expected a file: $Path" }
  return [ordered]@{
    Path = $RecordedPath
    Bytes = [int64]$item.Length
    SHA256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $item.FullName).Hash
  }
}

function Save-Manifest {
  if ($null -eq $manifest -or [string]::IsNullOrWhiteSpace($manifestPath)) { return }
  $temporary = "$manifestPath.tmp-$PID"
  [IO.File]::WriteAllText(
    $temporary,
    (($manifest | ConvertTo-Json -Depth 12) + "`n"),
    [Text.UTF8Encoding]::new($false)
  )
  Move-Item -LiteralPath $temporary -Destination $manifestPath -Force
}

function Find-Diagnostics {
  param([Parameter(Mandatory = $true)][string]$LogText)
  $patterns = [ordered]@{
    MissingGlyph = 'Missing character:'
    OverfullHBox = 'Overfull \\hbox'
    OverfullVBox = 'Overfull \\vbox'
    UndefinedReference = 'Reference .* undefined|There were undefined references'
    UndefinedCitation = 'Citation .* undefined|There were undefined citations'
    MultiplyDefined = 'multiply defined|destination with the same identifier'
    Rerun = 'Rerun to get|Label\(s\) may have changed|rerunfilecheck Warning'
    Fatal = 'Undefined control sequence|Emergency stop|Fatal error occurred'
  }
  $found = @()
  foreach ($entry in $patterns.GetEnumerator()) {
    if ($LogText -match $entry.Value) { $found += $entry.Key }
  }
  return @($found)
}

function Initialize-PrivateFontCache {
  param([Parameter(Mandatory = $true)][string]$Directory)
  $seedRoot = Join-Path $probeRoot 'cache-seed'
  $seed = Get-Content -LiteralPath (Join-Path $seedRoot 'SEED_MANIFEST.json') -Raw | ConvertFrom-Json
  if ($seed.Schema -cne 'openlogic-rtl-private-cache-seed-v1' -or
      $seed.Inputs.Count -ne 21 -or $seed.MaximumTotalBytes -ne 8388608) {
    throw 'Private font-cache seed contract differs.'
  }
  $total = [int64]0
  $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
  foreach ($row in $seed.Inputs) {
    if ($row.Path -cnotmatch '^luatex-cache/generic/(fonts/(hb|otl)|names)/[a-z0-9.-]+$' -or
        -not $seen.Add($row.Path)) { throw 'Invalid or duplicate cache seed path.' }
    $source = [IO.Path]::GetFullPath((Join-Path $seedRoot $row.Path))
    $target = [IO.Path]::GetFullPath((Join-Path $Directory $row.Path))
    if (-not $source.StartsWith($seedRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase) -or
        -not $target.StartsWith($Directory + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
      throw 'Cache seed path escaped its bounded directory.'
    }
    $identity = Get-Identity -Path $source -RecordedPath $row.Path
    $total += $identity.Bytes
    if ($identity.Bytes -ne $row.Bytes -or $identity.SHA256 -cne $row.SHA256 -or
        $total -gt $seed.MaximumTotalBytes) { throw 'Cache seed byte identity or bound differs.' }
    New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
    if (Test-Path -LiteralPath $target) { throw 'Private cache target already exists.' }
    Copy-Item -LiteralPath $source -Destination $target -ErrorAction Stop
    if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash -cne $row.SHA256) {
      throw 'Private cache copy differs.'
    }
  }
}

$resolvedOutput = Resolve-NewOutputDirectory -Value $OutputDirectory
New-Item -ItemType Directory -Path $resolvedOutput -ErrorAction Stop | Out-Null
$manifestPath = Join-Path $resolvedOutput 'BUILD_MANIFEST.json'

try {
  $privateCache = Join-Path $resolvedOutput 'texmf-cache'
  Initialize-PrivateFontCache -Directory $privateCache
  $engine = (Get-Command -Name 'lualatex' -CommandType Application -ErrorAction Stop |
    Select-Object -First 1).Source
  $engine = [IO.Path]::GetFullPath($engine)
  $inputSpecs = [ordered]@{
    'tmp/pdfs/classical-rtl-math-probe/common.tex' = Join-Path $probeRoot 'common.tex'
    'tmp/pdfs/classical-rtl-math-probe/control.tex' = Join-Path $probeRoot 'control.tex'
    'tmp/pdfs/classical-rtl-math-probe/rtl.tex' = Join-Path $probeRoot 'rtl.tex'
    'tmp/pdfs/classical-rtl-math-probe/BUILD_PROBE.ps1' = Join-Path $probeRoot 'BUILD_PROBE.ps1'
    'tmp/pdfs/classical-rtl-math-probe/RUN_PROBE.ps1' = Join-Path $probeRoot 'RUN_PROBE.ps1'
    'tmp/pdfs/classical-rtl-math-probe/cache-seed/SEED_MANIFEST.json' = Join-Path $probeRoot 'cache-seed\SEED_MANIFEST.json'
    'source/locale/ar-classical/open-logic-rtl-math.tex' = Join-Path $repoRoot 'source\locale\ar-classical\open-logic-rtl-math.tex'
    'source/sty/open-logic.sty' = Join-Path $repoRoot 'source\sty\open-logic.sty'
    'source/sty/open-logic-defer.sty' = Join-Path $repoRoot 'source\sty\open-logic-defer.sty'
    'source/open-logic-envs.sty' = Join-Path $repoRoot 'source\open-logic-envs.sty'
    'source/locale/ar/open-logic-config.sty' = Join-Path $repoRoot 'source\locale\ar\open-logic-config.sty'
    'build/qa_classical_rtl_math_probe.py' = Join-Path $repoRoot 'build\qa_classical_rtl_math_probe.py'
    'build/Invoke-WithInterlanguageTeXMutex.ps1' = Join-Path $repoRoot 'build\Invoke-WithInterlanguageTeXMutex.ps1'
    'build/InterlanguageTeXCapturedTree.cs' = Join-Path $repoRoot 'build\InterlanguageTeXCapturedTree.cs'
    '00_control/fonts/scheherazade-2.100/Scheherazade-Regular.ttf' = Join-Path $repoRoot '00_control\fonts\scheherazade-2.100\Scheherazade-Regular.ttf'
    '00_control/fonts/scheherazade-2.100/Scheherazade-Bold.ttf' = Join-Path $repoRoot '00_control\fonts\scheherazade-2.100\Scheherazade-Bold.ttf'
  }
  $inputs = @()
  foreach ($entry in $inputSpecs.GetEnumerator()) {
    $inputs += Get-Identity -Path $entry.Value -RecordedPath $entry.Key
  }
  $jobs = [ordered]@{}
  foreach ($job in @('control', 'rtl')) {
    $jobSource = [IO.Path]::GetFullPath((Join-Path $probeRoot "$job.tex"))
    $arguments = @(
      '-interaction=nonstopmode',
      '-halt-on-error',
      '-file-line-error',
      '-recorder',
      "-output-directory=$resolvedOutput",
      $jobSource
    )
    $jobs[$job] = [ordered]@{
      Source = $jobSource
      Arguments = $arguments
      Passes = @()
      Converged = $false
      StablePass = $null
      Outputs = @()
    }
  }
  $manifest = [ordered]@{
    Schema = 'openlogic-classical-rtl-math-probe-build-v1'
    Status = 'PREPARED'
    StartedAtUtc = [DateTimeOffset]::UtcNow.ToString('o')
    OutputDirectory = $resolvedOutput
    WorkingDirectory = $workingDirectory
    Engine = Get-Identity -Path $engine -RecordedPath $engine
    GuardInvocation = [ordered]@{
      Command = [IO.Path]::GetFullPath((Get-Process -Id $PID).Path)
      Arguments = @('-NoProfile', '-File', (Join-Path $probeRoot 'BUILD_PROBE.ps1'),
        '-OutputDirectory', $resolvedOutput)
      WorkingDirectory = [IO.Path]::GetFullPath((Get-Location).ProviderPath)
    }
    Environment = [ordered]@{
      SOURCE_DATE_EPOCH = '1783874174'
      FORCE_SOURCE_DATE = '1'
      TZ = 'UTC'
      TEXINPUTS = "$resolvedOutput;"
      TEMP = $resolvedOutput
      TMP = $resolvedOutput
      TEXMFCACHE = $privateCache
    }
    MaximumPasses = 4
    RequiredProducts = @('aux', 'out', 'fls', 'log', 'pdf')
    ConvergenceState = @('aux', 'out', 'toc', 'lof', 'lot', 'loe')
    InputsCapturedAtUtc = [DateTimeOffset]::UtcNow.ToString('o')
    Inputs = $inputs
    Jobs = $jobs
  }
  Save-Manifest

  $env:SOURCE_DATE_EPOCH = $manifest.Environment.SOURCE_DATE_EPOCH
  $env:FORCE_SOURCE_DATE = $manifest.Environment.FORCE_SOURCE_DATE
  $env:TZ = $manifest.Environment.TZ
  $env:TEXINPUTS = $manifest.Environment.TEXINPUTS
  $env:TEMP = $manifest.Environment.TEMP
  $env:TMP = $manifest.Environment.TMP
  $env:TEXMFCACHE = $manifest.Environment.TEXMFCACHE

  Push-Location -LiteralPath $workingDirectory
  try {
    foreach ($job in @('control', 'rtl')) {
      $previous = $null
      foreach ($pass in 1..$manifest.MaximumPasses) {
        $terminalPath = Join-Path $resolvedOutput "$job-pass-$pass.terminal.txt"
        & $engine @($manifest.Jobs[$job].Arguments) 2>&1 |
          Set-Content -LiteralPath $terminalPath -Encoding utf8
        $nativeExitCode = $LASTEXITCODE
        $passRecord = [ordered]@{
          Pass = $pass
          ExitCode = [int]$nativeExitCode
          Terminal = Get-Identity -Path $terminalPath -RecordedPath ([IO.Path]::GetFileName($terminalPath))
        }
        $manifest.Jobs[$job].Passes += $passRecord
        if ($nativeExitCode -ne 0) {
          Save-Manifest
          throw "$job RTL-math probe pass $pass failed; see $terminalPath"
        }
        foreach ($suffix in $manifest.RequiredProducts) {
          $product = Join-Path $resolvedOutput "$job.$suffix"
          if (-not (Test-Path -LiteralPath $product -PathType Leaf)) {
            Save-Manifest
            throw "$job pass $pass did not produce required .$suffix output"
          }
        }
        $logPath = Join-Path $resolvedOutput "$job.log"
        $logText = Get-Content -LiteralPath $logPath -Raw -Encoding utf8
        $passLogPath = Join-Path $resolvedOutput "$job-pass-$pass.log"
        Copy-Item -LiteralPath $logPath -Destination $passLogPath -ErrorAction Stop
        $diagnostics = @(Find-Diagnostics -LogText $logText)
        $passRecord.Log = Get-Identity -Path $passLogPath -RecordedPath ([IO.Path]::GetFileName($passLogPath))
        $passRecord.Diagnostics = $diagnostics
        if ('MissingGlyph' -in $diagnostics -or 'OverfullHBox' -in $diagnostics -or
            'OverfullVBox' -in $diagnostics -or 'MultiplyDefined' -in $diagnostics -or
            'Fatal' -in $diagnostics -or -not $logText.Contains('Output written on')) {
          Save-Manifest
          throw "$job RTL-math probe pass $pass has a fatal glyph/box/label/log diagnostic"
        }
        $state = @()
        foreach ($suffix in $manifest.ConvergenceState) {
          $stateFile = Join-Path $resolvedOutput "$job.$suffix"
          if (Test-Path -LiteralPath $stateFile -PathType Leaf) {
            $identity = Get-Identity -Path $stateFile -RecordedPath "$job.$suffix"
            $state += "$suffix=$($identity.SHA256)"
          }
        }
        foreach ($requiredState in @('aux', 'out')) {
          if (-not ($state | Where-Object { $_.StartsWith("$requiredState=") })) {
            Save-Manifest
            throw "$job pass $pass lacks required convergence state .$requiredState"
          }
        }
        $fingerprint = $state -join ';'
        $passRecord.StateFingerprint = $fingerprint
        if ($null -ne $previous -and $previous -eq $fingerprint -and
            @($diagnostics | Where-Object { $_ -in @('UndefinedReference', 'UndefinedCitation', 'Rerun') }).Count -eq 0) {
          $manifest.Jobs[$job].Converged = $true
          $manifest.Jobs[$job].StablePass = $pass
          break
        }
        $previous = $fingerprint
        Save-Manifest
      }
      if (-not $manifest.Jobs[$job].Converged) {
        Save-Manifest
        throw "$job RTL-math probe did not converge cleanly within four passes"
      }
      $outputs = @()
      foreach ($suffix in $manifest.RequiredProducts) {
        $outputPath = Join-Path $resolvedOutput "$job.$suffix"
        $outputs += Get-Identity -Path $outputPath -RecordedPath "$job.$suffix"
      }
      foreach ($suffix in $manifest.ConvergenceState) {
        if ($suffix -in @('aux', 'out')) { continue }
        $outputPath = Join-Path $resolvedOutput "$job.$suffix"
        if (Test-Path -LiteralPath $outputPath -PathType Leaf) {
          $outputs += Get-Identity -Path $outputPath -RecordedPath "$job.$suffix"
        }
      }
      $manifest.Jobs[$job].Outputs = $outputs
      Save-Manifest
    }
  } finally {
    Pop-Location
  }
  $manifest.Status = 'PASS'
  $manifest.FinishedAtUtc = [DateTimeOffset]::UtcNow.ToString('o')
  Save-Manifest
} catch {
  if ($null -ne $manifest) {
    $manifest.Status = 'FAIL'
    $manifest.Failure = $_.Exception.Message
    $manifest.FinishedAtUtc = [DateTimeOffset]::UtcNow.ToString('o')
    Save-Manifest
  }
  throw
}
