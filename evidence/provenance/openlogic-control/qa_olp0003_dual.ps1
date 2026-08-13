[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Programme = Split-Path -Parent $PSScriptRoot
$ExpectedCommit = '9620cc73f9c8e0ad003c514a5d3748f29611c4c0'
$ExpectedSourceHash = '03E55D8EE2EC4586A5DC8B64E6FA59950C46DA3CDEE54267946015E7BBD989ED'
$ExpectedBranches = @{'ar'='codex/openlogic-ar';'fa-IR'='codex/openlogic-fa-ir'}

function Assert-True {
  param([bool]$Condition,[string]$Message)
  if(-not $Condition){throw $Message}
}

function Read-Nfc {
  param([string]$Path)
  $Text=[IO.File]::ReadAllText($Path)
  Assert-True ($Text.IsNormalized([Text.NormalizationForm]::FormC)) "Not NFC: $Path"
  Assert-True (-not $Text.Contains([char]0xFFFD)) "Replacement character: $Path"
  return $Text
}

function Import-Signatures {
  param([string]$Text)
  return @([regex]::Matches($Text,'\\olimport\[(?<opt>[^\]]+)\]\{(?<arg>[^{}]+)\}') |
    ForEach-Object {$_.Groups['opt'].Value+'::'+$_.Groups['arg'].Value})
}

foreach($Locale in @('ar','fa-IR')){
  $Root=Join-Path $Programme $Locale
  $Head=(& git -C $Root rev-parse HEAD).Trim()
  Assert-True ($LASTEXITCODE -eq 0) "Cannot resolve HEAD: $Locale"
  $Branch=(& git -C $Root branch --show-current).Trim()
  Assert-True ($Branch -ceq $ExpectedBranches[$Locale]) "Wrong branch: $Locale $Branch"
  & git -C $Root merge-base --is-ancestor $ExpectedCommit $Head
  Assert-True ($LASTEXITCODE -eq 0) "Pinned source is not an ancestor: $Locale $Head"

  $SourcePath=Join-Path $Root 'content\sets-functions-relations\sets-functions-relations-complete.tex'
  Assert-True (((Get-FileHash -Algorithm SHA256 -LiteralPath $SourcePath).Hash) -ceq $ExpectedSourceHash) "Wrong source hash: $Locale"
  $Source=Read-Nfc $SourcePath
  $TargetPath=Join-Path $Root "locale\$Locale\content\sets-functions-relations\sets-functions-relations-complete.tex"
  Assert-True (Test-Path -LiteralPath $TargetPath -PathType Leaf) "Missing target: $Locale"
  $Target=Read-Nfc $TargetPath
  $RelativeTarget="locale/$Locale/content/sets-functions-relations/sets-functions-relations-complete.tex"
  & git -C $Root cat-file -e "HEAD:$RelativeTarget"
  Assert-True ($LASTEXITCODE -eq 0) "Target is not committed at HEAD: $Locale"
  & git -C $Root diff --quiet HEAD -- $RelativeTarget
  Assert-True ($LASTEXITCODE -eq 0) "Target differs from committed HEAD: $Locale"

  Assert-True (([regex]::Matches($Target,'\\documentclass\[\.\./\.\./include/open-logic-part\]\{subfiles\}')).Count -eq 1) "documentclass mismatch: $Locale"
  $Envs=@([regex]::Matches($Target,'\\(?<kind>begin|end)\{(?<env>document|editorial)\}')|ForEach-Object{$_.Groups['kind'].Value+':'+$_.Groups['env'].Value})
  Assert-True (($Envs -join '|') -ceq 'begin:document|begin:editorial|end:editorial|end:document') "environment mismatch: $Locale"
  $Part=[regex]::Match($Target,'\\olpart\{(?<id>[^{}]+)\}\{(?<title>[^{}]+)\}')
  Assert-True ($Part.Success -and $Part.Groups['id'].Value -ceq 'sfr' -and $Part.Groups['title'].Value.Length -gt 0) "olpart mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\OLEndPartHook')).Count -eq 1) "OLEndPartHook mismatch: $Locale"
  $SourceImports=Import-Signatures $Source
  $TargetImports=Import-Signatures $Target
  Assert-True ($TargetImports.Count -eq 6 -and ($TargetImports -join '|') -ceq ($SourceImports -join '|')) "import mismatch: $Locale"
  Assert-True (([regex]::Matches($Target,'\\href\{')).Count -eq 0) "unexpected href: $Locale"
  foreach($Sentinel in @('The material in this part','basic naive set','Tim Button','Open Set Theory','construction of number systems','discussion of infinity','not required for the logical parts','Proyek Logika','teori himpunan')){
    Assert-True (-not $Target.Contains($Sentinel)) "Residual source/Indonesian prose '$Sentinel': $Locale"
  }
  Assert-True (-not [regex]::IsMatch($Target,'[\uFB50-\uFDFF\uFE70-\uFEFF]')) "Presentation form: $Locale"
  Assert-True (-not [regex]::IsMatch($Target,'[\u202A-\u202E\u2066-\u2069]')) "Explicit bidi control: $Locale"
  Assert-True (([regex]::Matches($Target,'(?<!\\)\{')).Count -eq ([regex]::Matches($Target,'(?<!\\)\}')).Count) "Brace mismatch: $Locale"
  if($Locale -eq 'ar'){
    Assert-True (-not [regex]::IsMatch($Target,'[\u067E\u0686\u0698\u06A9\u06AF\u06CC]')) 'Persian code point in Arabic target'
  }else{
    Assert-True (-not [regex]::IsMatch($Target,'[\u0643\u0649\u064A]')) 'Arabic Kaf/Yeh in Persian target'
  }
  $TargetHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $TargetPath).Hash
  "OLP0003_STATIC_OK locale=$Locale target_sha256=$TargetHash part_title=$($Part.Groups['title'].Value) imports=$($TargetImports.Count)"
}
