param(
  [Parameter(Mandatory=$true)]
  [ValidatePattern('^[a-z0-9][a-z0-9-]{7,79}$')]
  [string]$RunId,
  [switch]$InsideMutex
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$taskOut = Join-Path $repoRoot ('tmp\pdfs\classical-math-token-fields-'+$RunId)
if (-not $InsideMutex) {
  $taskReceipt = Join-Path $taskOut 'TEX_MUTEX_RECEIPT.json'
  if (Test-Path -LiteralPath $taskReceipt) { throw 'Existing specimen run; inspect receipt, do not overwrite.' }
  & (Join-Path $PSScriptRoot 'Invoke-WithInterlanguageTeXMutex.ps1') `
    -Command (Get-Process -Id $PID).Path `
    -CommandArguments @('-NoProfile','-File',$PSCommandPath,'-RunId',$RunId,'-InsideMutex') `
    -AcquisitionTimeoutSeconds 60 -ReceiptPath $taskReceipt
  if ($LASTEXITCODE -ne 0) { throw 'Captured specimen build failed.' }
  exit 0
}
$taskProbeInputs = Get-Content -LiteralPath (Join-Path $taskOut 'SOURCE_SPECIMEN.json') -Raw | ConvertFrom-Json
foreach ($taskInput in $taskProbeInputs.inputs) {
  $taskSource = Join-Path $repoRoot $taskInput.path
  if ((Get-FileHash -LiteralPath $taskSource -Algorithm SHA256).Hash.ToLowerInvariant() -cne $taskInput.sha256) {
    throw 'Specimen bound input changed before build.'
  }
}
$taskEngine = (Get-Command lualatex -CommandType Application | Select-Object -First 1).Source
Push-Location (Join-Path $repoRoot 'source\locale\ar')
try {
  foreach ($taskName in @('control','rtl')) {
    & $taskEngine '-interaction=nonstopmode' '-halt-on-error' '-file-line-error' '-recorder' ('-output-directory='+$taskOut) (Join-Path $taskOut ($taskName+'.tex'))
    if ($LASTEXITCODE -ne 0) { throw ('Specimen engine failed: '+$taskName) }
    $taskLog = Get-Content -LiteralPath (Join-Path $taskOut ($taskName+'.log')) -Raw
    if ($taskLog -match 'Missing character:|Undefined control sequence|Fatal error occurred|Overfull \\[hv]box') {
      throw ('Specimen log failed: '+$taskName)
    }
    if ([regex]::Matches($taskLog,'OLC-FIELD-').Count -ne $taskProbeInputs.cases.Count) { throw 'Not all specimen cases reached typesetting.' }
  }
} finally { Pop-Location }
foreach ($taskInput in $taskProbeInputs.inputs) {
  if ((Get-FileHash -LiteralPath (Join-Path $repoRoot $taskInput.path) -Algorithm SHA256).Hash.ToLowerInvariant() -cne $taskInput.sha256) {
    throw 'Specimen bound input changed during build.'
  }
}
