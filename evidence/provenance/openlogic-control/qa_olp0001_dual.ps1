[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Control = $PSScriptRoot
$Programme = Split-Path -Parent $Control
$ExpectedCommit = '9620cc73f9c8e0ad003c514a5d3748f29611c4c0'
$ExpectedSourceHash = 'E4F2E2EC5D9957FA71DF41E9ED100641FE08230F63AF6065EAAFCB3D37346F4A'
$ExpectedBranches = @{
  'ar' = 'codex/openlogic-ar'
  'fa-IR' = 'codex/openlogic-fa-ir'
}
$ExpectedUrls = @(
  'https://github.com/OpenLogicProject/OpenLogic/wiki/Contributing',
  'http://openlogicproject.org/'
)
$CaptionKeys = @(
  'photocredits','history','reading','appendix','appendices','theorem',
  'example','definition','lemma','proposition','corollary','problem',
  'problems','remark','axiom','note','case','convention','OLP','OLT',
  'OLTlink','license','instigator','editorialboard','contributors'
)
$CrefKeys = @(
  'page','thm','ex','defn','lem','prop','prob','rem','cor','axiom','note',
  'case','conv','figure','table'
)
$Boilerplate = @(
  'ollicensetext','olshortlicensetext','oluselicensetext',
  'olshortuselicensetext','olremixedby','olacknowledgements',
  'olillustrations','olcolophon','olbookrevision'
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

foreach ($Locale in @('ar','fa-IR')) {
  $Root = Join-Path $Programme $Locale
  $Head = (& git -C $Root rev-parse HEAD).Trim()
  Assert-True ($LASTEXITCODE -eq 0) "Cannot resolve HEAD: $Locale"
  $Branch = (& git -C $Root branch --show-current).Trim()
  Assert-True ($LASTEXITCODE -eq 0 -and $Branch -ceq $ExpectedBranches[$Locale]) "Wrong branch: $Locale $Branch"
  & git -C $Root merge-base --is-ancestor $ExpectedCommit $Head
  Assert-True ($LASTEXITCODE -eq 0) "Pinned source is not an ancestor: $Locale $Head"
  $SourcePath = Join-Path $Root 'content\open-logic-about.tex'
  $SourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $SourcePath).Hash
  Assert-True ($SourceHash -ceq $ExpectedSourceHash) "Wrong source hash: $Locale $SourceHash"

  $LocaleRoot = Join-Path $Root ("locale\$Locale")
  $TargetPath = Join-Path $LocaleRoot 'content\open-logic-about.tex'
  $LocalePath = Join-Path $LocaleRoot 'open-logic-locale.sty'
  $Target = Read-Nfc $TargetPath
  $LocaleText = Read-Nfc $LocalePath
  $RelativeTarget = "locale/$Locale/content/open-logic-about.tex"
  & git -C $Root cat-file -e "HEAD:$RelativeTarget"
  Assert-True ($LASTEXITCODE -eq 0) "Target is not committed at HEAD: $Locale"
  & git -C $Root diff --quiet HEAD -- $RelativeTarget
  Assert-True ($LASTEXITCODE -eq 0) "Target differs from committed HEAD: $Locale"

  Assert-True (([regex]::Matches($Target, '\\chapter\*')).Count -eq 1) "chapter* mismatch: $Locale"
  Assert-True (([regex]::Matches($Target, '\\addcontentsline\{toc\}\{chapter\}')).Count -eq 1) "TOC routing mismatch: $Locale"
  Assert-True (([regex]::Matches($Target, '\\textit\{')).Count -eq 1) "textit mismatch: $Locale"
  Assert-True (([regex]::Matches($Target, '\\href\{')).Count -eq 2) "href count mismatch: $Locale"
  $Urls = @([regex]::Matches($Target, '\\href\{(?<url>[^{}]+)\}') | ForEach-Object { $_.Groups['url'].Value })
  Assert-True (($Urls -join '|') -ceq ($ExpectedUrls -join '|')) "URL sequence mismatch: $Locale"

  $Chapter = [regex]::Match($Target, '\\chapter\*\{(?<title>[^{}]+)\}').Groups['title'].Value
  $Toc = [regex]::Match($Target, '\\addcontentsline\{toc\}\{chapter\}\{(?<title>[^{}]+)\}').Groups['title'].Value
  Assert-True ($Chapter -and $Chapter -ceq $Toc) "Heading/TOC mismatch: $Locale"

  foreach ($Sentinel in @(
    'About the Open Logic Project','is an open-source','formal meta-logic',
    'Coverage of some topics','We plan to','please let the project team know',
    'The project operates in the spirit','additional information',
    'Proyek Logika Terbuka','Teks Logika Terbuka','metalogika','metode formal'
  )) {
    Assert-True (-not $Target.Contains($Sentinel)) "Residual source/Indonesian prose '$Sentinel': $Locale"
  }

  Assert-True (-not [regex]::IsMatch($Target + $LocaleText, '[\uFB50-\uFDFF\uFE70-\uFEFF]')) "Presentation form found: $Locale"
  Assert-True (-not [regex]::IsMatch($Target + $LocaleText, '[\u202A-\u202E\u2066-\u2069]')) "Explicit bidi control found: $Locale"
  if ($Locale -eq 'ar') {
    Assert-True (-not [regex]::IsMatch($Target + $LocaleText, '[\u067E\u0686\u0698\u06A9\u06AF\u06CC]')) 'Persian code point in Arabic target'
  } else {
    Assert-True (-not [regex]::IsMatch($Target + $LocaleText, '[\u0643\u0649\u064A]')) 'Arabic Kaf/Yeh in Persian target'
  }

  $FoundCaption = @([regex]::Matches($LocaleText, '\\setlocalecaption\{[^{}]+\}\{(?<key>[^{}]+)\}') | ForEach-Object { $_.Groups['key'].Value })
  Assert-True (@($CaptionKeys | Where-Object { $_ -notin $FoundCaption }).Count -eq 0) "Missing caption keys: $Locale"
  $FoundCref = @([regex]::Matches($LocaleText, '\\Crefname\{(?<key>[^{}]+)\}') | ForEach-Object { $_.Groups['key'].Value } | Sort-Object -Unique)
  Assert-True (@($CrefKeys | Where-Object { $_ -notin $FoundCref }).Count -eq 0) "Missing Cref keys: $Locale"
  foreach ($Macro in $Boilerplate) {
    Assert-True ([regex]::IsMatch($LocaleText, "\\renewcommand\*?\{\\$Macro\}")) "Missing boilerplate ${Macro}: $Locale"
  }
  $DriverName = if ($Locale -eq 'ar') { 'about-ar.tex' } else { 'about-fa-ir.tex' }
  foreach ($Path in @($TargetPath,$LocalePath,(Join-Path $LocaleRoot 'open-logic-config.sty'),(Join-Path $LocaleRoot $DriverName))) {
    $Text = Read-Nfc $Path
    Assert-True (([regex]::Matches($Text, '(?<!\\)\{')).Count -eq ([regex]::Matches($Text, '(?<!\\)\}')).Count) "Brace-count mismatch: $Path"
  }

  $TargetHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $TargetPath).Hash
  $LocaleHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $LocalePath).Hash
  "OLP0001_STATIC_OK locale=$Locale target_sha256=$TargetHash locale_sha256=$LocaleHash"
}
