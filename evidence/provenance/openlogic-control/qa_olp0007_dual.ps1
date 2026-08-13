[CmdletBinding()]
param()

$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Programme=Split-Path -Parent $PSScriptRoot
$ExpectedCommit='9620cc73f9c8e0ad003c514a5d3748f29611c4c0'
$ExpectedSourceHash='B1B998CAD3FA5AEF48670F755245F86EFE00B239D332A50E764147602405FB32'
$ExpectedBranches=@{'ar'='codex/openlogic-ar';'fa-IR'='codex/openlogic-fa-ir'}

function Assert-True{param([bool]$Condition,[string]$Message)if(-not $Condition){throw $Message}}
function Read-Nfc{param([string]$Path)$t=[IO.File]::ReadAllText($Path);Assert-True ($t.IsNormalized([Text.NormalizationForm]::FormC)) "Not NFC: $Path";Assert-True (-not $t.Contains([char]0xFFFD)) "Replacement character: $Path";return $t}
function Command-Sequence{param([string]$Text)return @([regex]::Matches($Text,'\\(?<cmd>[A-Za-z@]+|.)')|ForEach-Object{$_.Groups['cmd'].Value})}
function Environment-Sequence{param([string]$Text)return @([regex]::Matches($Text,'\\(?<kind>begin|end)\{(?<env>[^{}]+)\}')|ForEach-Object{$_.Groups['kind'].Value+':'+$_.Groups['env'].Value})}
function Token-Sequence{param([string]$Text)return @([regex]::Matches($Text,'!!(?<article>a)?\{(?<term>[^{}]+)\}(?<plural>s)?')|ForEach-Object{($_.Groups['article'].Value+'{'+$_.Groups['term'].Value+'}'+$_.Groups['plural'].Value)})}
function Math-Segments{param([string]$Text)return @([regex]::Matches($Text,'(?s)\\begin\{multline\*\}.*?\\end\{multline\*\}|\$(?!\$).*?\$')|ForEach-Object{$s=[regex]::Replace($_.Value,'\\text\{[^{}]*\}','\text{#}');[regex]::Replace($s,'\s+','')})}

foreach($Locale in @('ar','fa-IR')){
  $Root=Join-Path $Programme $Locale
  $Head=(& git -C $Root rev-parse HEAD).Trim();Assert-True ($LASTEXITCODE -eq 0) "Cannot resolve HEAD: $Locale"
  $Branch=(& git -C $Root branch --show-current).Trim();Assert-True ($Branch -ceq $ExpectedBranches[$Locale]) "Wrong branch: $Locale $Branch"
  & git -C $Root merge-base --is-ancestor $ExpectedCommit $Head;Assert-True ($LASTEXITCODE -eq 0) "Pinned source not ancestor: $Locale"

  $SourcePath=Join-Path $Root 'content\sets-functions-relations\sets\important-sets.tex'
  Assert-True (((Get-FileHash -Algorithm SHA256 -LiteralPath $SourcePath).Hash) -ceq $ExpectedSourceHash) "Wrong source hash: $Locale"
  $Source=Read-Nfc $SourcePath
  $TargetPath=Join-Path $Root "locale\$Locale\content\sets-functions-relations\sets\important-sets.tex"
  Assert-True (Test-Path -LiteralPath $TargetPath -PathType Leaf) "Missing target: $Locale"
  $Target=Read-Nfc $TargetPath

  $SourceCommands=Command-Sequence $Source;$TargetCommands=Command-Sequence $Target
  Assert-True ($SourceCommands.Count -eq 95 -and $TargetCommands.Count -eq 95) "TeX command count mismatch: $Locale source=$($SourceCommands.Count) target=$($TargetCommands.Count)"
  Assert-True (($TargetCommands -join '|') -ceq ($SourceCommands -join '|')) "TeX command sequence mismatch: $Locale"
  $SourceEnvs=Environment-Sequence $Source;$TargetEnvs=Environment-Sequence $Target
  Assert-True ($SourceEnvs.Count -eq 14 -and $TargetEnvs.Count -eq 14) "Environment count mismatch: $Locale"
  Assert-True (($TargetEnvs -join '|') -ceq ($SourceEnvs -join '|')) "Environment sequence mismatch: $Locale"
  $SourceTokens=Token-Sequence $Source;$TargetTokens=Token-Sequence $Target
  Assert-True (($SourceTokens -join '|') -ceq '{element}s|{element}s|{element}s|a{element}') "Unexpected source token oracle"
  Assert-True (($TargetTokens -join '|') -ceq ($SourceTokens -join '|')) "Text-token sequence mismatch: $Locale"
  $SourceMath=Math-Segments $Source;$TargetMath=Math-Segments $Target
  Assert-True ($SourceMath.Count -eq 26 -and $TargetMath.Count -eq 26) "Math count mismatch: $Locale source=$($SourceMath.Count) target=$($TargetMath.Count)"
  for($i=0;$i -lt $SourceMath.Count;$i++){Assert-True ($SourceMath[$i] -ceq $TargetMath[$i]) "Math mismatch: $Locale segment=$($i+1)"}

  $ExpectedOlFileId=if($Locale -eq 'ar'){'\\olfileid\[ar\]\{sfr\}\{set\}\{imp\}'}else{'\\olfileid\[fa-IR\]\{sfr\}\{set\}\{imp\}'}
  Assert-True (([regex]::Matches($Target,$ExpectedOlFileId)).Count -eq 1) "localized olfileid mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\olsection\{[^{}]+\}')).Count -eq 1) "section mismatch: $Locale"
  Assert-True ($Target.Contains('\oliflabeldef{sfr:arith:real:realline}')) "Conditional label mismatch: $Locale"
  Assert-True ($Target.Contains('\olref[arith][real]{realline}')) "Conditional reference mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\begin\{tagblock\}\{compsci\}')).Count -eq 1) "tagblock mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\ollabel')).Count -eq 0) "unexpected ordinary label: $Locale"
  Assert-True (([regex]::Matches($Target,'\\emph')).Count -eq 5) "emphasis count mismatch: $Locale"
  Assert-True (-not $Target.Contains('Some Important Sets')) "Untranslated section title: $Locale"
  foreach($Sentinel in @('The following four sets','are all infinite','set of natural numbers','set of integers','set of rational numbers','set of real numbers','The inclusions are all proper','Positive integers','binary numbers','finite strings','empty string','length of the string','one-way infinite sequences','Proyek Logika')){Assert-True (-not $Target.Contains($Sentinel)) "Residual source/Indonesian prose '$Sentinel': $Locale"}
  Assert-True (-not [regex]::IsMatch($Target,'[\u202A-\u202E\u2066-\u2069\uFB50-\uFDFF\uFE70-\uFEFF]')) "bidi/presentation form: $Locale"
  Assert-True (([regex]::Matches($Target,'(?<!\\)\{')).Count -eq ([regex]::Matches($Target,'(?<!\\)\}')).Count) "brace mismatch: $Locale"
  if($Locale -eq 'ar'){Assert-True (-not [regex]::IsMatch($Target,'[\u067E\u0686\u0698\u06A9\u06AF\u06CC]')) 'Persian code point in Arabic'}else{Assert-True (-not [regex]::IsMatch($Target,'[\u0643\u0649\u064A]')) 'Arabic Kaf/Yeh in Persian'}

  $ConfigPath=Join-Path $Root "locale\$Locale\open-logic-config.sty";$Config=Read-Nfc $ConfigPath
  Assert-True ([regex]::IsMatch($Config,'\\settexttoken\{element\}')) "Missing element token binding: $Locale"
  Assert-True ([regex]::IsMatch($Config,'\\definetoken\{a\}\{element\}\{\}')) "Missing empty indefinite article: $Locale"

  $TargetHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $TargetPath).Hash
  "OLP0007_STATIC_OK locale=$Locale target_sha256=$TargetHash math=26 tokens=$($TargetTokens.Count)"
}
