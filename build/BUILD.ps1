param(
  [string]$OutputDirectory = ""
)

$releaseRoot = Split-Path -Parent $PSScriptRoot
$localeRoot = Join-Path $releaseRoot "source\locale\ar"
$driver = Join-Path $localeRoot "open-logic-through-olp0010-ar.tex"
if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
  $OutputDirectory = Join-Path $PSScriptRoot "output-ar"
}
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$resolvedOutput = (Resolve-Path -LiteralPath $OutputDirectory).Path

$env:SOURCE_DATE_EPOCH = "1783874174"
$env:FORCE_SOURCE_DATE = "1"
$env:TZ = "UTC"
$outputArgument = "-output-directory=$resolvedOutput"

Push-Location $localeRoot
try {
  for ($pass = 1; $pass -le 5; $pass++) {
    & lualatex -interaction=nonstopmode -halt-on-error -file-line-error -recorder $outputArgument $driver
    if ($LASTEXITCODE -ne 0) { throw "LuaLaTeX failed on pass $pass" }
  }
} finally {
  Pop-Location
}

$pdf = Join-Path $resolvedOutput "open-logic-through-olp0010-ar.pdf"
Get-FileHash -Algorithm SHA256 -LiteralPath $pdf
