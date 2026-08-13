[CmdletBinding()]
param()

$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Programme=Split-Path -Parent $PSScriptRoot
$ExpectedCommit='9620cc73f9c8e0ad003c514a5d3748f29611c4c0'
$ExpectedSourceHash='8BC9151AF0985E6E20C374AA38CDDD1ADD7A8DFFBABCCC94B89F324F62C40F8C'
$ExpectedBranches=@{'ar'='codex/openlogic-ar';'fa-IR'='codex/openlogic-fa-ir'}

function Assert-True{param([bool]$Condition,[string]$Message)if(-not $Condition){throw $Message}}
function Read-Nfc{param([string]$Path)$t=[IO.File]::ReadAllText($Path);Assert-True ($t.IsNormalized([Text.NormalizationForm]::FormC)) "Not NFC: $Path";Assert-True (-not $t.Contains([char]0xFFFD)) "Replacement character: $Path";return $t}
function Command-Sequence{param([string]$Text)return @([regex]::Matches($Text,'\\(?<cmd>[A-Za-z@]+|.)')|ForEach-Object{$_.Groups['cmd'].Value})}
function Environment-Sequence{param([string]$Text)return @([regex]::Matches($Text,'\\(?<kind>begin|end)\{(?<env>[^{}]+)\}')|ForEach-Object{$_.Groups['kind'].Value+':'+$_.Groups['env'].Value})}
function Token-Sequence{param([string]$Text)return @([regex]::Matches($Text,'!!(?<article>a)?\{(?<term>[^{}]+)\}(?<plural>s)?')|ForEach-Object{($_.Groups['article'].Value+'{'+$_.Groups['term'].Value+'}'+$_.Groups['plural'].Value)})}
function Math-Skeletons{
  param([string]$Text)
  return @([regex]::Matches($Text,'(?s)\\\[.*?\\\]|\$(?!\$).*?\$')|ForEach-Object{
    $x=$_.Value
    $x=[regex]::Replace($x,'\\text(?:rm)?\{[^{}]*\}','\TEXT{}')
    [regex]::Replace($x,'\s+','')
  })
}

foreach($Locale in @('ar','fa-IR')){
  $Root=Join-Path $Programme $Locale
  $Head=(& git -C $Root rev-parse HEAD).Trim();Assert-True ($LASTEXITCODE -eq 0) "Cannot resolve HEAD: $Locale"
  $Branch=(& git -C $Root branch --show-current).Trim();Assert-True ($Branch -ceq $ExpectedBranches[$Locale]) "Wrong branch: $Locale $Branch"
  & git -C $Root merge-base --is-ancestor $ExpectedCommit $Head;Assert-True ($LASTEXITCODE -eq 0) "Pinned source not ancestor: $Locale"

  $SourcePath=Join-Path $Root 'content\sets-functions-relations\sets\basics.tex'
  Assert-True (((Get-FileHash -Algorithm SHA256 -LiteralPath $SourcePath).Hash) -ceq $ExpectedSourceHash) "Wrong source hash: $Locale"
  $Source=Read-Nfc $SourcePath
  $TargetPath=Join-Path $Root "locale\$Locale\content\sets-functions-relations\sets\basics.tex"
  Assert-True (Test-Path -LiteralPath $TargetPath -PathType Leaf) "Missing target: $Locale"
  $Target=Read-Nfc $TargetPath

  Assert-True (((Command-Sequence $Target) -join '|') -ceq ((Command-Sequence $Source) -join '|')) "TeX command sequence mismatch: $Locale"
  Assert-True (((Environment-Sequence $Target) -join '|') -ceq ((Environment-Sequence $Source) -join '|')) "Environment sequence mismatch: $Locale"
  Assert-True (((Token-Sequence $Target) -join '|') -ceq ((Token-Sequence $Source) -join '|')) "Text-token sequence mismatch: $Locale"
  $SourceMath=Math-Skeletons $Source;$TargetMath=Math-Skeletons $Target
  Assert-True ($SourceMath.Count -eq 52 -and $TargetMath.Count -eq 52) "Math count mismatch: $Locale source=$($SourceMath.Count) target=$($TargetMath.Count)"
  for($i=0;$i -lt $SourceMath.Count;$i++){Assert-True ($SourceMath[$i] -ceq $TargetMath[$i]) "Math skeleton mismatch: $Locale segment=$($i+1)"}

  $ExpectedOlFileId=if($Locale -eq 'ar'){'\\olfileid\[ar\]\{sfr\}\{set\}\{bas\}'}else{'\\olfileid\[fa-IR\]\{sfr\}\{set\}\{bas\}'}
  Assert-True (([regex]::Matches($Target,$ExpectedOlFileId)).Count -eq 1) "localized olfileid mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\olsection\{[^{}]+\}')).Count -eq 1) "section mismatch: $Locale"
  $Tagblocks=@([regex]::Matches($Target,'\\begin\{tagblock\}\{(?<tag>[^{}]+)\}')|ForEach-Object{$_.Groups['tag'].Value})
  Assert-True (($Tagblocks -join '|') -ceq 'novice|novice|math') "tagblock mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\text(?:rm)?\{[^{}]*\}')).Count -eq 3) "text-in-math count mismatch: $Locale"
  Assert-True (-not $Target.Contains('Extensionality')) "Untranslated section/definition title: $Locale"
  foreach($Sentinel in @('A set is a collection','objects making up the set','empty set','It does not matter how','Extensionality licenses','Richard''s siblings','positive integers less than','A number is called','proper divisors','at most one empty set','is a sibling of Richard','is perfect and','Proyek Logika')){Assert-True (-not $Target.Contains($Sentinel)) "Residual source/Indonesian prose '$Sentinel': $Locale"}
  Assert-True (-not [regex]::IsMatch($Target,'[\u202A-\u202E\u2066-\u2069\uFB50-\uFDFF\uFE70-\uFEFF]')) "bidi/presentation form: $Locale"
  Assert-True (([regex]::Matches($Target,'(?<!\\)\{')).Count -eq ([regex]::Matches($Target,'(?<!\\)\}')).Count) "brace mismatch: $Locale"
  if($Locale -eq 'ar'){Assert-True (-not [regex]::IsMatch($Target,'[\u067E\u0686\u0698\u06A9\u06AF\u06CC]')) 'Persian code point in Arabic'}else{Assert-True (-not [regex]::IsMatch($Target,'[\u0643\u0649\u064A]')) 'Arabic Kaf/Yeh in Persian'}

  $ConfigPath=Join-Path $Root "locale\$Locale\open-logic-config.sty";$Config=Read-Nfc $ConfigPath
  Assert-True ([regex]::IsMatch($Config,'\\settexttoken\{element\}')) "Missing element token binding: $Locale"
  Assert-True ([regex]::IsMatch($Config,'\\definetoken\{a\}\{element\}\{\}')) "Missing empty indefinite article: $Locale"
  Assert-True ([regex]::IsMatch($Config,'\\definetoken\{A\}\{element\}\{\}')) "Missing empty capitalized article: $Locale"

  $TargetHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $TargetPath).Hash
  $ConfigHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $ConfigPath).Hash
  "OLP0005_STATIC_OK locale=$Locale target_sha256=$TargetHash config_sha256=$ConfigHash math=52 tokens=$((Token-Sequence $Target).Count)"
}
