[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Programme=Split-Path -Parent $PSScriptRoot
$ExpectedCommit='9620cc73f9c8e0ad003c514a5d3748f29611c4c0'
$ExpectedSourceHash='EEA34D38BB52811468A0025D348457A0F4D3F44AAE4B7CABB28551D6328E2785'
$ExpectedBranches=@{'ar'='codex/openlogic-ar';'fa-IR'='codex/openlogic-fa-ir'}
function Assert-True{param([bool]$Condition,[string]$Message)if(-not $Condition){throw $Message}}
function Read-Nfc{param([string]$Path)$t=[IO.File]::ReadAllText($Path);Assert-True ($t.IsNormalized([Text.NormalizationForm]::FormC)) "Not NFC: $Path";Assert-True (-not $t.Contains([char]0xFFFD)) "Replacement character: $Path";return $t}
function Imports{param([string]$Text)return @([regex]::Matches($Text,'\\olimport\{(?<arg>[^{}]+)\}')|ForEach-Object{$_.Groups['arg'].Value})}
foreach($Locale in @('ar','fa-IR')){
  $Root=Join-Path $Programme $Locale
  $Head=(& git -C $Root rev-parse HEAD).Trim();Assert-True ($LASTEXITCODE -eq 0) "Cannot resolve HEAD: $Locale"
  $Branch=(& git -C $Root branch --show-current).Trim();Assert-True ($Branch -ceq $ExpectedBranches[$Locale]) "Wrong branch: $Locale $Branch"
  & git -C $Root merge-base --is-ancestor $ExpectedCommit $Head;Assert-True ($LASTEXITCODE -eq 0) "Pinned source not ancestor: $Locale"
  $SourcePath=Join-Path $Root 'content\sets-functions-relations\sets\sets.tex';Assert-True (((Get-FileHash -Algorithm SHA256 -LiteralPath $SourcePath).Hash) -ceq $ExpectedSourceHash) "Wrong source hash: $Locale"
  $Source=Read-Nfc $SourcePath
  $TargetPath=Join-Path $Root "locale\$Locale\content\sets-functions-relations\sets\sets.tex";Assert-True (Test-Path -LiteralPath $TargetPath -PathType Leaf) "Missing target: $Locale"
  $Target=Read-Nfc $TargetPath
  $RelativeTarget="locale/$Locale/content/sets-functions-relations/sets/sets.tex"
  & git -C $Root cat-file -e "HEAD:$RelativeTarget";Assert-True ($LASTEXITCODE -eq 0) "Target is not committed at HEAD: $Locale"
  & git -C $Root diff --quiet HEAD -- $RelativeTarget;Assert-True ($LASTEXITCODE -eq 0) "Target differs from committed HEAD: $Locale"
  Assert-True (([regex]::Matches($Target,'\\documentclass\[\.\./\.\./\.\./include/open-logic-chapter\]\{subfiles\}')).Count -eq 1) "documentclass mismatch: $Locale"
  $Envs=@([regex]::Matches($Target,'\\(?<kind>begin|end)\{document\}')|ForEach-Object{$_.Groups['kind'].Value});Assert-True (($Envs -join '|') -ceq 'begin|end') "document environment mismatch: $Locale"
  $Chapter=[regex]::Match($Target,'\\olchapter\{(?<part>[^{}]+)\}\{(?<id>[^{}]+)\}\{(?<title>[^{}]+)\}')
  Assert-True ($Chapter.Success -and $Chapter.Groups['part'].Value -ceq 'sfr' -and $Chapter.Groups['id'].Value -ceq 'set' -and $Chapter.Groups['title'].Value.Length -gt 0) "chapter mismatch: $Locale"
  $si=Imports $Source;$ti=Imports $Target;Assert-True ($ti.Count -eq 6 -and ($ti -join '|') -ceq ($si -join '|')) "import mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\OLEndChapterHook')).Count -eq 1) "hook mismatch: $Locale"
  Assert-True (-not [regex]::IsMatch($Target,'[\u202A-\u202E\u2066-\u2069\uFB50-\uFDFF\uFE70-\uFEFF]')) "bidi/presentation form: $Locale"
  Assert-True (([regex]::Matches($Target,'(?<!\\)\{')).Count -eq ([regex]::Matches($Target,'(?<!\\)\}')).Count) "brace mismatch: $Locale"
  if($Locale -eq 'ar'){Assert-True (-not [regex]::IsMatch($Target,'[\u067E\u0686\u0698\u06A9\u06AF\u06CC]')) 'Persian code point in Arabic'}else{Assert-True (-not [regex]::IsMatch($Target,'[\u0643\u0649\u064A]')) 'Arabic Kaf/Yeh in Persian'}
  $Hash=(Get-FileHash -Algorithm SHA256 -LiteralPath $TargetPath).Hash
  "OLP0004_STATIC_OK locale=$Locale target_sha256=$Hash chapter_title=$($Chapter.Groups['title'].Value) imports=$($ti.Count)"
}
