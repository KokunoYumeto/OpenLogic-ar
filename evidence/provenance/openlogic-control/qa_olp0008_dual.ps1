[CmdletBinding()]
param()

$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Programme=Split-Path -Parent $PSScriptRoot
$ExpectedCommit='9620cc73f9c8e0ad003c514a5d3748f29611c4c0'
$ExpectedSourceHash='2AD0EEC70308CEEFF2A4158B2DEE60E59A9B1CF9268FC95C4BB1DA05F65AD60D'
$ExpectedBranches=@{'ar'='codex/openlogic-ar';'fa-IR'='codex/openlogic-fa-ir'}

function Assert-True{param([bool]$Condition,[string]$Message)if(-not $Condition){throw $Message}}
function Read-Nfc{param([string]$Path)$t=[IO.File]::ReadAllText($Path);Assert-True ($t.IsNormalized([Text.NormalizationForm]::FormC)) "Not NFC: $Path";Assert-True (-not $t.Contains([char]0xFFFD)) "Replacement character: $Path";return $t}
function Command-Sequence{param([string]$Text)return @([regex]::Matches($Text,'\\(?<cmd>[A-Za-z@]+|.)')|ForEach-Object{$_.Groups['cmd'].Value})}
function Environment-Sequence{param([string]$Text)return @([regex]::Matches($Text,'\\(?<kind>begin|end)\{(?<env>[^{}]+)\}')|ForEach-Object{$_.Groups['kind'].Value+':'+$_.Groups['env'].Value})}
function Token-Sequence{param([string]$Text)return @([regex]::Matches($Text,'!!(?<article>a)?\{(?<term>[^{}]+)\}(?<plural>s)?')|ForEach-Object{($_.Groups['article'].Value+'{'+$_.Groups['term'].Value+'}'+$_.Groups['plural'].Value)})}
function Normalize-TextPayloads{
  param([string]$Text)
  $Builder=[Text.StringBuilder]::new();$Index=0
  while($Index -lt $Text.Length){
    if($Index+6 -le $Text.Length -and $Text.Substring($Index,6) -ceq '\text{'){
      [void]$Builder.Append('\text{#}');$Index+=6;$Depth=1
      while($Index -lt $Text.Length -and $Depth -gt 0){
        if($Text[$Index] -eq '{'){$Depth++}elseif($Text[$Index] -eq '}'){$Depth--}
        $Index++
      }
      Assert-True ($Depth -eq 0) 'Unbalanced text payload in math segment'
    }else{[void]$Builder.Append($Text[$Index]);$Index++}
  }
  return $Builder.ToString()
}
function Math-Segments{param([string]$Text)return @([regex]::Matches($Text,'(?s)\\begin\{align\*\}.*?\\end\{align\*\}|\\\[.*?\\\]|\$(?!\$).*?\$')|ForEach-Object{[regex]::Replace((Normalize-TextPayloads $_.Value),'\s+','')})}
function Capture-Arguments{param([string]$Text,[string]$Command)return @([regex]::Matches($Text,"\\$Command\{(?<v>[^{}]+)\}")|ForEach-Object{$_.Groups['v'].Value})}

foreach($Locale in @('ar','fa-IR')){
  $Root=Join-Path $Programme $Locale
  $Head=(& git -C $Root rev-parse HEAD).Trim();Assert-True ($LASTEXITCODE -eq 0) "Cannot resolve HEAD: $Locale"
  $Branch=(& git -C $Root branch --show-current).Trim();Assert-True ($Branch -ceq $ExpectedBranches[$Locale]) "Wrong branch: $Locale"
  & git -C $Root merge-base --is-ancestor $ExpectedCommit $Head;Assert-True ($LASTEXITCODE -eq 0) "Pinned source not ancestor: $Locale"

  $SourcePath=Join-Path $Root 'content\sets-functions-relations\sets\unions-and-intersections.tex'
  Assert-True (((Get-FileHash -Algorithm SHA256 -LiteralPath $SourcePath).Hash) -ceq $ExpectedSourceHash) "Wrong source hash: $Locale"
  $Source=Read-Nfc $SourcePath
  $TargetPath=Join-Path $Root "locale\$Locale\content\sets-functions-relations\sets\unions-and-intersections.tex"
  Assert-True (Test-Path -LiteralPath $TargetPath -PathType Leaf) "Missing target: $Locale"
  $Target=Read-Nfc $TargetPath

  $SourceCommands=Command-Sequence $Source;$TargetCommands=Command-Sequence $Target
  Assert-True ($SourceCommands.Count -eq 213 -and $TargetCommands.Count -eq 213) "TeX command count mismatch: $Locale source=$($SourceCommands.Count) target=$($TargetCommands.Count)"
  Assert-True (($TargetCommands -join '|') -ceq ($SourceCommands -join '|')) "TeX command sequence mismatch: $Locale"
  $SourceEnvs=Environment-Sequence $Source;$TargetEnvs=Environment-Sequence $Target
  Assert-True ($SourceEnvs.Count -eq 46 -and $TargetEnvs.Count -eq 46) "Environment count mismatch: $Locale"
  Assert-True (($TargetEnvs -join '|') -ceq ($SourceEnvs -join '|')) "Environment sequence mismatch: $Locale"
  $SourceTokens=Token-Sequence $Source;$TargetTokens=Token-Sequence $Target
  Assert-True ($SourceTokens.Count -eq 27 -and $TargetTokens.Count -eq 27) "Token count mismatch: $Locale"
  Assert-True (($TargetTokens -join '|') -ceq ($SourceTokens -join '|')) "Text-token sequence mismatch: $Locale"
  $SourceMath=Math-Segments $Source;$TargetMath=Math-Segments $Target
  Assert-True ($SourceMath.Count -eq 72 -and $TargetMath.Count -eq 72) "Math count mismatch: $Locale source=$($SourceMath.Count) target=$($TargetMath.Count)"
  for($i=0;$i -lt $SourceMath.Count;$i++){Assert-True ($SourceMath[$i] -ceq $TargetMath[$i]) "Math mismatch: $Locale segment=$($i+1)"}

  $ExpectedOlFileId=if($Locale -eq 'ar'){'\\olfileid\[ar\]\{sfr\}\{set\}\{uni\}'}else{'\\olfileid\[fa-IR\]\{sfr\}\{set\}\{uni\}'}
  Assert-True (([regex]::Matches($Target,$ExpectedOlFileId)).Count -eq 1) "localized olfileid mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\olsection\{[^{}]+\}')).Count -eq 1) "section mismatch: $Locale"
  $Labels=Capture-Arguments $Target 'ollabel';Assert-True (($Labels -join '|') -ceq 'fig:union|fig:intersection|difference') "labels mismatch: $Locale"
  $Assets=Capture-Arguments $Target 'olasset';Assert-True (($Assets -join '|') -ceq 'assets/diagrams/union.tikz|assets/diagrams/intersection.tikz|assets/diagrams/difference.tikz') "assets mismatch: $Locale"
  $Refs=@([regex]::Matches($Target,'\\olref(?:\[[^\]]+\]){0,3}\{[^{}]+\}')|ForEach-Object{$_.Value})
  Assert-True (($Refs -join '|') -ceq '\olref[sfr][set][bas]{sec}|\olref{fig:union}|\olref{fig:intersection}|\olref{difference}') "references mismatch: $Locale"
  Assert-True (-not $Target.Contains('Unions and Intersections')) "Untranslated section title: $Locale"
  foreach($Sentinel in @('We already encountered','The union of','The intersection of','are disjoint','union of all the sets','intersection of all the sets','indexed family','set difference','symmetric difference','Proyek Logika')){Assert-True (-not $Target.Contains($Sentinel)) "Residual source/Indonesian prose '$Sentinel': $Locale"}
  Assert-True (-not [regex]::IsMatch($Target,'[\u202A-\u202E\u2066-\u2069\uFB50-\uFDFF\uFE70-\uFEFF]')) "bidi/presentation form: $Locale"
  Assert-True (([regex]::Matches($Target,'(?<!\\)\{')).Count -eq ([regex]::Matches($Target,'(?<!\\)\}')).Count) "brace mismatch: $Locale"
  if($Locale -eq 'ar'){Assert-True (-not [regex]::IsMatch($Target,'[\u067E\u0686\u0698\u06A9\u06AF\u06CC]')) 'Persian code point in Arabic'}else{Assert-True (-not [regex]::IsMatch($Target,'[\u0643\u0649\u064A]')) 'Arabic Kaf/Yeh in Persian'}

  $TargetHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $TargetPath).Hash
  "OLP0008_STATIC_OK locale=$Locale target_sha256=$TargetHash commands=213 envs=46 math=72 tokens=27"
}
