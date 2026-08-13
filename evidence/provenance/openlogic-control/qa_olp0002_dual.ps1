[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Control = $PSScriptRoot
$Programme = Split-Path -Parent $Control
$ExpectedCommit = '9620cc73f9c8e0ad003c514a5d3748f29611c4c0'
$ExpectedSourceHash = 'B42CD7F4BFD4185CCDA7F834A706973A728B2126498C873671924A77B4D8F1D6'
$ExpectedBranches = @{
  'ar' = 'codex/openlogic-ar'
  'fa-IR' = 'codex/openlogic-fa-ir'
}
$ExpectedUrls = @(
  'http://builds.openlogicproject.org/',
  'https://github.com/OpenLogicProject/OpenLogic/tree/master/courses/sample'
)

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { throw $Message }
}

function Read-Nfc {
  param([string]$Path)
  $Text = [IO.File]::ReadAllText($Path)
  Assert-True ($Text.IsNormalized([Text.NormalizationForm]::FormC)) "Not NFC: $Path"
  Assert-True (-not $Text.Contains([char]0xFFFD)) "Replacement character: $Path"
  return $Text
}

function Import-Signatures {
  param([string]$Text)
  return @([regex]::Matches($Text, '\\olimport(?:\[(?<opt>[^\]]+)\])?\{(?<arg>[^{}]+)\}') |
    ForEach-Object { $_.Groups['opt'].Value + '::' + $_.Groups['arg'].Value })
}

foreach ($Locale in @('ar','fa-IR')) {
  $Root = Join-Path $Programme $Locale
  $Head = (& git -C $Root rev-parse HEAD).Trim()
  Assert-True ($LASTEXITCODE -eq 0) "Cannot resolve HEAD: $Locale"
  $Branch = (& git -C $Root branch --show-current).Trim()
  Assert-True ($LASTEXITCODE -eq 0 -and $Branch -ceq $ExpectedBranches[$Locale]) "Wrong branch: $Locale $Branch"
  & git -C $Root merge-base --is-ancestor $ExpectedCommit $Head
  Assert-True ($LASTEXITCODE -eq 0) "Pinned source is not an ancestor: $Locale $Head"

  $SourcePath = Join-Path $Root 'content\content.tex'
  $SourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $SourcePath).Hash
  Assert-True ($SourceHash -ceq $ExpectedSourceHash) "Wrong source hash: $Locale $SourceHash"
  $Source = Read-Nfc $SourcePath

  $LocaleRoot = Join-Path $Root ("locale\$Locale")
  $TargetPath = Join-Path $LocaleRoot 'content\content.tex'
  Assert-True (Test-Path -LiteralPath $TargetPath -PathType Leaf) "Missing target: $Locale"
  $Target = Read-Nfc $TargetPath
  $RelativeTarget = "locale/$Locale/content/content.tex"
  & git -C $Root cat-file -e "HEAD:$RelativeTarget"
  Assert-True ($LASTEXITCODE -eq 0) "Target is not committed at HEAD: $Locale"
  & git -C $Root diff --quiet HEAD -- $RelativeTarget
  Assert-True ($LASTEXITCODE -eq 0) "Target differs from committed HEAD: $Locale"

  Assert-True (([regex]::Matches($Target, '\\documentclass\[\.\./include/open-logic-part\]\{subfiles\}')).Count -eq 1) "documentclass mismatch: $Locale"
  $Environments = @([regex]::Matches($Target, '\\(?<kind>begin|end)\{(?<env>document|editorial)\}') |
    ForEach-Object { $_.Groups['kind'].Value + ':' + $_.Groups['env'].Value })
  Assert-True (($Environments -join '|') -ceq 'begin:document|begin:editorial|end:editorial|end:document') "environment sequence mismatch: $Locale"
  Assert-True (([regex]::Matches($Target, '\\clearpage')).Count -eq 1) "clearpage mismatch: $Locale"
  Assert-True (([regex]::Matches($Target, '\\emph\{')).Count -eq 1) "emph count mismatch: $Locale"

  $Urls = @([regex]::Matches($Target, '\\href\{(?<url>[^{}]+)\}') |
    ForEach-Object { $_.Groups['url'].Value })
  Assert-True (($Urls -join '|') -ceq ($ExpectedUrls -join '|')) "URL sequence mismatch: $Locale"

  $SourceImports = Import-Signatures $Source
  $TargetImports = Import-Signatures $Target
  Assert-True ($SourceImports.Count -eq 18 -and $TargetImports.Count -eq 18) "import count mismatch: $Locale"
  Assert-True (($TargetImports -join '|') -ceq ($SourceImports -join '|')) "import order/argument mismatch: $Locale"

  $Editorial = [regex]::Match($Target, '(?s)\\begin\{editorial\}(?<body>.*?)\\end\{editorial\}')
  Assert-True ($Editorial.Success) "editorial body missing: $Locale"
  $Paragraphs = @([regex]::Split($Editorial.Groups['body'].Value.Trim(), '\r?\n\s*\r?\n') |
    Where-Object { $_.Trim().Length -gt 0 })
  Assert-True ($Paragraphs.Count -eq 3) "editorial paragraph count mismatch: $Locale $($Paragraphs.Count)"

  foreach ($Sentinel in @(
    'This file loads all content','Editorial notes like this','If you can read this',
    'not advisable','provides many mechanisms','logical operators','work in progress',
    'To find PDFs more suitable','To make your own','Proyek Logika','Teks Logika'
  )) {
    Assert-True (-not $Target.Contains($Sentinel)) "Residual source/Indonesian prose '$Sentinel': $Locale"
  }

  Assert-True (-not [regex]::IsMatch($Target, '[\uFB50-\uFDFF\uFE70-\uFEFF]')) "Presentation form found: $Locale"
  Assert-True (-not [regex]::IsMatch($Target, '[\u202A-\u202E\u2066-\u2069]')) "Explicit bidi control found: $Locale"
  Assert-True (([regex]::Matches($Target, '(?<!\\)\{')).Count -eq ([regex]::Matches($Target, '(?<!\\)\}')).Count) "Brace-count mismatch: $Locale"
  if ($Locale -eq 'ar') {
    Assert-True (-not [regex]::IsMatch($Target, '[\u067E\u0686\u0698\u06A9\u06AF\u06CC]')) 'Persian code point in Arabic target'
  } else {
    Assert-True (-not [regex]::IsMatch($Target, '[\u0643\u0649\u064A]')) 'Arabic Kaf/Yeh in Persian target'
  }

  $TargetHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $TargetPath).Hash
  "OLP0002_STATIC_OK locale=$Locale target_sha256=$TargetHash imports=$($TargetImports.Count) paragraphs=$($Paragraphs.Count)"
}
