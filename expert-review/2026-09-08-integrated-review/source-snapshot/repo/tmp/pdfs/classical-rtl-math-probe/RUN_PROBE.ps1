param([Parameter(Mandatory = $true)][string]$OutputDirectory)

$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
  throw 'RTL-math probe output path must not be blank.'
}
$resolvedOutput = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDirectory)
$resolvedOutput = [IO.Path]::GetFullPath($resolvedOutput)
if (-not [IO.Path]::IsPathRooted($resolvedOutput) -or
    $resolvedOutput -ieq [IO.Path]::GetPathRoot($resolvedOutput)) {
  throw 'RTL-math probe output path must be a non-root absolute filesystem path.'
}
$receiptParent = Split-Path -Parent $resolvedOutput
$receiptLeaf = (Split-Path -Leaf $resolvedOutput) + '-TEX_MUTEX_RECEIPT.json'
$receiptPath = Join-Path $receiptParent $receiptLeaf
if (Test-Path -LiteralPath $resolvedOutput) {
  throw 'RTL-math probe output must not already exist.'
}
if (Test-Path -LiteralPath $receiptPath) {
  throw 'RTL-math probe guard receipt must not already exist.'
}

$taskShell = [IO.Path]::GetFullPath((Get-Process -Id $PID).Path)
& (Join-Path $repoRoot 'build\Invoke-WithInterlanguageTeXMutex.ps1') `
  -Command $taskShell `
  -CommandArguments @(
    '-NoProfile',
    '-File',
    (Join-Path $PSScriptRoot 'BUILD_PROBE.ps1'),
    '-OutputDirectory',
    $resolvedOutput
  ) `
  -AcquisitionTimeoutSeconds 60 `
  -ReceiptPath $receiptPath
$guardExitCode = $LASTEXITCODE
if ($guardExitCode -ne 0) { throw "Guarded RTL-math probe failed with exit code $guardExitCode" }
if (-not (Test-Path -LiteralPath $receiptPath -PathType Leaf)) {
  throw 'Guarded RTL-math probe returned without its receipt.'
}
