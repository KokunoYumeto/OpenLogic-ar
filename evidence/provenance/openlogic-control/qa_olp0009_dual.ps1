[CmdletBinding()]
param(
  [switch]$SourceOracleOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Programme = Split-Path -Parent $PSScriptRoot
$ExpectedCommit = '9620cc73f9c8e0ad003c514a5d3748f29611c4c0'
$ExpectedSourceHash = '3DB7F0241D387B49488F70E78062C24192B813873618F761565D97BD7249431C'
$ExpectedBranches = @{
  'ar' = 'codex/openlogic-ar'
  'fa-IR' = 'codex/openlogic-fa-ir'
}
$RelativeSource = 'content\sets-functions-relations\sets\pairs-and-products.tex'
$RelativeTarget = 'content\sets-functions-relations\sets\pairs-and-products.tex'

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

function Get-StringHash {
  param([string]$Text)
  $Hasher = [Security.Cryptography.SHA256]::Create()
  try {
    $Bytes = [Text.Encoding]::UTF8.GetBytes($Text)
    return ([BitConverter]::ToString($Hasher.ComputeHash($Bytes))).Replace('-', '')
  }
  finally { $Hasher.Dispose() }
}

function Test-EscapedAt {
  param([string]$Text, [int]$Index)
  $SlashCount = 0
  for ($i = $Index - 1; $i -ge 0 -and $Text[$i] -eq '\'; $i--) { $SlashCount++ }
  return (($SlashCount % 2) -eq 1)
}

function Read-BalancedGroup {
  param(
    [string]$Text,
    [int]$StartIndex,
    [char]$Open,
    [char]$Close
  )
  Assert-True ($StartIndex -lt $Text.Length -and $Text[$StartIndex] -eq $Open) "Expected '$Open' at index $StartIndex"
  $Depth = 0
  $Builder = [Text.StringBuilder]::new()
  for ($i = $StartIndex; $i -lt $Text.Length; $i++) {
    $Character = $Text[$i]
    if (($Character -eq $Open -or $Character -eq $Close) -and (Test-EscapedAt $Text $i)) {
      if ($Depth -gt 0) { [void]$Builder.Append($Character) }
      continue
    }
    if ($Character -eq $Open) {
      $Depth++
      if ($Depth -gt 1) { [void]$Builder.Append($Character) }
      continue
    }
    if ($Character -eq $Close) {
      $Depth--
      Assert-True ($Depth -ge 0) "Unexpected '$Close' at index $i"
      if ($Depth -eq 0) {
        return [pscustomobject]@{ Value = $Builder.ToString(); NextIndex = $i + 1 }
      }
      [void]$Builder.Append($Character)
      continue
    }
    if ($Depth -gt 0) { [void]$Builder.Append($Character) }
  }
  throw "Unclosed '$Open' group beginning at index $StartIndex"
}

function Get-CommandCalls {
  param([string]$Text, [string]$Command)
  $Pattern = '\\' + [regex]::Escape($Command) + '(?![A-Za-z@])'
  $Calls = [Collections.Generic.List[object]]::new()
  foreach ($Match in [regex]::Matches($Text, $Pattern)) {
    $Cursor = $Match.Index + $Match.Length
    while ($Cursor -lt $Text.Length -and [char]::IsWhiteSpace($Text[$Cursor])) { $Cursor++ }
    $Options = [Collections.Generic.List[string]]::new()
    while ($Cursor -lt $Text.Length -and $Text[$Cursor] -eq '[') {
      $Group = Read-BalancedGroup $Text $Cursor '[' ']'
      $Options.Add($Group.Value)
      $Cursor = $Group.NextIndex
      while ($Cursor -lt $Text.Length -and [char]::IsWhiteSpace($Text[$Cursor])) { $Cursor++ }
    }
    $Arguments = [Collections.Generic.List[string]]::new()
    while ($Cursor -lt $Text.Length -and $Text[$Cursor] -eq '{') {
      $Group = Read-BalancedGroup $Text $Cursor '{' '}'
      $Arguments.Add($Group.Value)
      $Cursor = $Group.NextIndex
      while ($Cursor -lt $Text.Length -and [char]::IsWhiteSpace($Text[$Cursor])) { $Cursor++ }
    }
    $Calls.Add([pscustomobject]@{
      Options = @($Options)
      Arguments = @($Arguments)
      StartIndex = $Match.Index
      NextIndex = $Cursor
    })
  }
  return @($Calls)
}

function Get-CommandSequence {
  param([string]$Text)
  return @([regex]::Matches($Text, '\\(?<cmd>[A-Za-z@]+|.)') | ForEach-Object { $_.Groups['cmd'].Value })
}

function Get-EnvironmentSequence {
  param([string]$Text)
  return @([regex]::Matches($Text, '\\(?<kind>begin|end)\{(?<env>[^{}]+)\}') | ForEach-Object {
    $_.Groups['kind'].Value + ':' + $_.Groups['env'].Value
  })
}

function Get-TokenSequence {
  param([string]$Text)
  return @([regex]::Matches($Text, '!!(?<article>a)?\{(?<term>[^{}]+)\}(?<plural>s)?') | ForEach-Object {
    $_.Groups['article'].Value + '{' + $_.Groups['term'].Value + '}' + $_.Groups['plural'].Value
  })
}

function Get-MathSegments {
  param([string]$Text)
  $Segments = [Collections.Generic.List[string]]::new()
  $Index = 0
  while ($Index -lt $Text.Length) {
    if ($Text[$Index] -eq '%' -and -not (Test-EscapedAt $Text $Index)) {
      $Newline = $Text.IndexOf("`n", $Index)
      if ($Newline -lt 0) { break }
      $Index = $Newline + 1
      continue
    }
    $AlignStart = '\begin{align*}'
    $AlignEnd = '\end{align*}'
    if ($Index + $AlignStart.Length -le $Text.Length -and $Text.Substring($Index, $AlignStart.Length) -ceq $AlignStart) {
      $EndIndex = $Text.IndexOf($AlignEnd, $Index + $AlignStart.Length, [StringComparison]::Ordinal)
      Assert-True ($EndIndex -ge 0) "Unclosed align* segment at index $Index"
      $Length = $EndIndex + $AlignEnd.Length - $Index
      $Segments.Add($Text.Substring($Index, $Length))
      $Index += $Length
      continue
    }
    if ($Index + 2 -le $Text.Length -and $Text.Substring($Index, 2) -ceq '\[') {
      $EndIndex = $Text.IndexOf('\]', $Index + 2, [StringComparison]::Ordinal)
      Assert-True ($EndIndex -ge 0) "Unclosed display-math segment at index $Index"
      $Length = $EndIndex + 2 - $Index
      $Segments.Add($Text.Substring($Index, $Length))
      $Index += $Length
      continue
    }
    if ($Text[$Index] -eq '$' -and -not (Test-EscapedAt $Text $Index) -and ($Index + 1 -ge $Text.Length -or $Text[$Index + 1] -ne '$')) {
      $EndIndex = $Index + 1
      while ($EndIndex -lt $Text.Length -and ($Text[$EndIndex] -ne '$' -or (Test-EscapedAt $Text $EndIndex))) { $EndIndex++ }
      Assert-True ($EndIndex -lt $Text.Length) "Unclosed inline-math segment at index $Index"
      $Segments.Add($Text.Substring($Index, $EndIndex + 1 - $Index))
      $Index = $EndIndex + 1
      continue
    }
    $Index++
  }
  return @($Segments)
}

function Normalize-LocalizedTextInMath {
  param([string]$Text)
  $Builder = [Text.StringBuilder]::new()
  $Index = 0
  while ($Index -lt $Text.Length) {
    if ($Index + 6 -le $Text.Length -and $Text.Substring($Index, 6) -ceq '\text{') {
      [void]$Builder.Append('\text{#}')
      $Group = Read-BalancedGroup $Text ($Index + 5) '{' '}'
      $Index = $Group.NextIndex
      continue
    }
    [void]$Builder.Append($Text[$Index])
    $Index++
  }
  return [regex]::Replace($Builder.ToString(), '\s+', '')
}

function Get-NormalizedMathSequence {
  param([string]$Text)
  return @(Get-MathSegments $Text | ForEach-Object { Normalize-LocalizedTextInMath $_ })
}

function Assert-TeXBraceBalance {
  param([string]$Text, [string]$Context)
  $Depth = 0
  $InComment = $false
  for ($i = 0; $i -lt $Text.Length; $i++) {
    $Character = $Text[$i]
    if ($InComment) {
      if ($Character -eq "`n") { $InComment = $false }
      continue
    }
    if ($Character -eq '%' -and -not (Test-EscapedAt $Text $i)) { $InComment = $true; continue }
    if (($Character -eq '{' -or $Character -eq '}') -and (Test-EscapedAt $Text $i)) { continue }
    if ($Character -eq '{') { $Depth++ }
    elseif ($Character -eq '}') {
      $Depth--
      Assert-True ($Depth -ge 0) "Closing brace without opener: $Context index=$i"
    }
  }
  Assert-True ($Depth -eq 0) "Unbalanced braces: $Context depth=$Depth"
}

function Get-CallSignature {
  param([string]$Command, [object]$Call)
  $OptionText = (@($Call.Options) | ForEach-Object { '[' + $_ + ']' }) -join ''
  $ArgumentText = (@($Call.Arguments) | ForEach-Object { '{' + $_ + '}' }) -join ''
  return '\' + $Command + $OptionText + $ArgumentText
}

function Get-ProseLatinRuns {
  param([string]$Text)
  $Work = [regex]::Replace($Text, '(?m)(?<!\\)%.*$', ' ')
  foreach ($Segment in @(Get-MathSegments $Work)) { $Work = $Work.Replace($Segment, ' ') }
  $Work = [regex]::Replace($Work, '!!(?<article>a)?\{[^{}]+\}(?<plural>s)?', ' ')
  $Work = [regex]::Replace($Work, '\\documentclass(?:\[[^\]]*\])?\{[^{}]*\}', ' ')
  $Work = [regex]::Replace($Work, '\\olfileid(?:\[[^\]]*\])?(?:\{[^{}]*\}){3}', ' ')
  $Work = [regex]::Replace($Work, '\\ollabel\{[^{}]*\}', ' ')
  $Work = [regex]::Replace($Work, '\\olref(?:\[[^\]]*\]){0,3}\{[^{}]*\}', ' ')
  $Work = [regex]::Replace($Work, '\\(?:begin|end)\{[^{}]*\}', ' ')
  $Work = [regex]::Replace($Work, '\\[A-Za-z@]+|\\.', ' ')
  return @([regex]::Matches($Work, '[A-Za-z]{3,}') | ForEach-Object { $_.Value } | Sort-Object -Unique)
}

function Assert-SourceOracle {
  param([string]$Source)
  Assert-TeXBraceBalance $Source 'source'
  $Commands = @(Get-CommandSequence $Source)
  $Environments = @(Get-EnvironmentSequence $Source)
  $Tokens = @(Get-TokenSequence $Source)
  $Math = @(Get-NormalizedMathSequence $Source)
  Assert-True ($Commands.Count -eq 177) "Source command oracle drift: $($Commands.Count)"
  Assert-True ($Environments.Count -eq 30) "Source environment oracle drift: $($Environments.Count)"
  Assert-True ($Tokens.Count -eq 12) "Source token oracle drift: $($Tokens.Count)"
  Assert-True ($Math.Count -eq 78) "Source math oracle drift: $($Math.Count)"
  Assert-True (@(Get-MathSegments $Source | Where-Object { $_.StartsWith('$', [StringComparison]::Ordinal) }).Count -eq 72) 'Source inline-math oracle drift'
  Assert-True (@(Get-MathSegments $Source | Where-Object { $_.StartsWith('\[', [StringComparison]::Ordinal) }).Count -eq 5) 'Source display-math oracle drift'
  Assert-True (@(Get-MathSegments $Source | Where-Object { $_.StartsWith('\begin{align*}', [StringComparison]::Ordinal) }).Count -eq 1) 'Source align* oracle drift'

  $ExpectedEnvironmentSequence = 'begin:document|begin:explain|end:explain|begin:defn|end:defn|begin:prob|end:prob|begin:explain|end:explain|begin:defn|end:defn|begin:ex|end:ex|begin:ex|begin:align*|end:align*|end:ex|begin:prob|end:prob|begin:prop|end:prop|begin:proof|begin:array|end:array|end:proof|begin:prob|end:prob|begin:ex|end:ex|end:document'
  Assert-True (($Environments -join '|') -ceq $ExpectedEnvironmentSequence) 'Source environment role/ordering oracle drift'
  $ExpectedTokenSequence = '{element}s|{element}s|{element}s|{element}|{element}s|{element}s|{element}s|{element}s|{element}s|{element}s|{element}s|{element}s'
  Assert-True (($Tokens -join '|') -ceq $ExpectedTokenSequence) 'Source Open Logic token oracle drift'

  $FileIds = @(Get-CommandCalls $Source 'olfileid')
  Assert-True ($FileIds.Count -eq 1 -and $FileIds[0].Options.Count -eq 0 -and (($FileIds[0].Arguments -join '|') -ceq 'sfr|set|pai')) 'Source olfileid oracle drift'
  $Sections = @(Get-CommandCalls $Source 'olsection')
  Assert-True ($Sections.Count -eq 1 -and $Sections[0].Arguments.Count -eq 1 -and $Sections[0].Arguments[0] -ceq 'Pairs, Tuples, Cartesian Products') 'Source section oracle drift'
  $Labels = @(Get-CommandCalls $Source 'ollabel')
  Assert-True ($Labels.Count -eq 2 -and (($Labels | ForEach-Object { $_.Arguments[0] }) -join '|') -ceq 'wienerkuratowski|cardnmprod') 'Source label oracle drift'
  $Refs = @(Get-CommandCalls $Source 'olref')
  Assert-True ($Refs.Count -eq 1 -and (Get-CallSignature 'olref' $Refs[0]) -ceq '\olref[sfr][set][pai]{wienerkuratowski}') 'Source reference oracle drift'
  Assert-True (@(Get-CommandCalls $Source 'olasset').Count -eq 0) 'Unexpected source asset'
  Assert-True ((@(Get-CommandCalls $Source 'cite').Count + @(Get-CommandCalls $Source 'parencite').Count + @(Get-CommandCalls $Source 'textcite').Count) -eq 0) 'Unexpected source citation'
  Assert-True (([regex]::Matches($Source, '\\begin\{defn\}\s*\[[^\]\r\n]+\]')).Count -eq 2) 'Source definition-title oracle drift'
  Assert-True (([regex]::Matches($Source, '\\begin\{array\}\{rcccc\}')).Count -eq 1) 'Source array-column oracle drift'

  return [pscustomobject]@{
    Commands = $Commands
    Environments = $Environments
    Tokens = $Tokens
    Math = $Math
  }
}

$Source = $null
$Oracle = $null
foreach ($Locale in @('ar', 'fa-IR')) {
  $Root = Join-Path $Programme $Locale
  $Head = (& git -C $Root rev-parse HEAD).Trim()
  Assert-True ($LASTEXITCODE -eq 0) "Cannot resolve HEAD: $Locale"
  $Branch = (& git -C $Root branch --show-current).Trim()
  Assert-True ($LASTEXITCODE -eq 0 -and $Branch -ceq $ExpectedBranches[$Locale]) "Wrong branch: $Locale"
  & git -C $Root merge-base --is-ancestor $ExpectedCommit $Head
  Assert-True ($LASTEXITCODE -eq 0) "Pinned source commit is not an ancestor: $Locale"

  $SourcePath = Join-Path $Root $RelativeSource
  Assert-True (Test-Path -LiteralPath $SourcePath -PathType Leaf) "Missing source: $Locale"
  $SourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $SourcePath).Hash
  Assert-True ($SourceHash -ceq $ExpectedSourceHash) "Wrong source hash: $Locale got=$SourceHash"
  $LocaleSource = Read-Nfc $SourcePath
  if ($null -eq $Source) {
    $Source = $LocaleSource
    $Oracle = Assert-SourceOracle $Source
  }
  else { Assert-True ($LocaleSource -ceq $Source) "Source bytes/text disagree across worktrees: $Locale" }
}

$CommandSequenceHash = Get-StringHash ($Oracle.Commands -join "`n")
$EnvironmentSequenceHash = Get-StringHash ($Oracle.Environments -join "`n")
$TokenSequenceHash = Get-StringHash ($Oracle.Tokens -join "`n")
$MathSequenceHash = Get-StringHash ($Oracle.Math -join "`n")
"OLP0009_SOURCE_ORACLE_OK source_sha256=$ExpectedSourceHash commands=177 command_sequence_sha256=$CommandSequenceHash envs=30 environment_sequence_sha256=$EnvironmentSequenceHash tokens=12 token_sequence_sha256=$TokenSequenceHash math=78 inline=72 display=5 align=1 math_sequence_sha256=$MathSequenceHash"

if ($SourceOracleOnly) { return }

foreach ($Locale in @('ar', 'fa-IR')) {
  $Root = Join-Path $Programme $Locale
  $TargetPath = Join-Path (Join-Path $Root "locale\$Locale") $RelativeTarget
  Assert-True (Test-Path -LiteralPath $TargetPath -PathType Leaf) "Missing target: $Locale"
  $Target = Read-Nfc $TargetPath
  Assert-TeXBraceBalance $Target "target $Locale"

  $TargetCommands = @(Get-CommandSequence $Target)
  $TargetEnvironments = @(Get-EnvironmentSequence $Target)
  $TargetTokens = @(Get-TokenSequence $Target)
  $TargetMath = @(Get-NormalizedMathSequence $Target)
  Assert-True ($TargetCommands.Count -eq 177) "TeX command count mismatch: $Locale source=177 target=$($TargetCommands.Count)"
  Assert-True (($TargetCommands -join '|') -ceq ($Oracle.Commands -join '|')) "TeX command sequence mismatch: $Locale"
  Assert-True ($TargetEnvironments.Count -eq 30 -and (($TargetEnvironments -join '|') -ceq ($Oracle.Environments -join '|'))) "Environment sequence mismatch: $Locale"
  Assert-True ($TargetTokens.Count -eq 12 -and (($TargetTokens -join '|') -ceq ($Oracle.Tokens -join '|'))) "Open Logic token sequence mismatch: $Locale"
  Assert-True ($TargetMath.Count -eq 78) "Math segment count mismatch: $Locale source=78 target=$($TargetMath.Count)"
  for ($i = 0; $i -lt $Oracle.Math.Count; $i++) {
    Assert-True ($TargetMath[$i] -ceq $Oracle.Math[$i]) "Math mismatch after localized-text normalization: $Locale segment=$($i + 1)"
  }

  $DocumentClasses = @(Get-CommandCalls $Target 'documentclass')
  Assert-True ($DocumentClasses.Count -eq 1 -and $DocumentClasses[0].Options.Count -eq 1 -and $DocumentClasses[0].Options[0] -ceq '../../../include/open-logic-section' -and $DocumentClasses[0].Arguments.Count -eq 1 -and $DocumentClasses[0].Arguments[0] -ceq 'subfiles') "documentclass mismatch: $Locale"
  $FileIds = @(Get-CommandCalls $Target 'olfileid')
  Assert-True ($FileIds.Count -eq 1 -and $FileIds[0].Options.Count -eq 1 -and $FileIds[0].Options[0] -ceq $Locale -and (($FileIds[0].Arguments -join '|') -ceq 'sfr|set|pai')) "Localized olfileid mismatch: $Locale"
  $Sections = @(Get-CommandCalls $Target 'olsection')
  Assert-True ($Sections.Count -eq 1 -and $Sections[0].Arguments.Count -eq 1 -and $Sections[0].Arguments[0] -cne 'Pairs, Tuples, Cartesian Products') "Section localization mismatch: $Locale"
  $Labels = @(Get-CommandCalls $Target 'ollabel')
  Assert-True ($Labels.Count -eq 2 -and (($Labels | ForEach-Object { $_.Arguments[0] }) -join '|') -ceq 'wienerkuratowski|cardnmprod') "Label mismatch: $Locale"
  $Refs = @(Get-CommandCalls $Target 'olref')
  Assert-True ($Refs.Count -eq 1 -and (Get-CallSignature 'olref' $Refs[0]) -ceq '\olref[sfr][set][pai]{wienerkuratowski}') "Reference mismatch: $Locale"
  Assert-True (@(Get-CommandCalls $Target 'olasset').Count -eq 0) "Unexpected asset: $Locale"
  Assert-True ((@(Get-CommandCalls $Target 'cite').Count + @(Get-CommandCalls $Target 'parencite').Count + @(Get-CommandCalls $Target 'textcite').Count) -eq 0) "Unexpected citation: $Locale"
  Assert-True (([regex]::Matches($Target, '\\begin\{defn\}\s*\[[^\]\r\n]+\]')).Count -eq 2) "Definition headings missing: $Locale"
  Assert-True (([regex]::Matches($Target, '\\begin\{array\}\{rcccc\}')).Count -eq 1) "Array column specification mismatch: $Locale"
  foreach ($RoleValue in @('sets-functions-relations', 'sets', 'pairs-and-products')) {
    $RolePattern = '(?m)^%[^\r\n:]*:\s*' + [regex]::Escape($RoleValue) + '\s*$'
    Assert-True (([regex]::Matches($Target, $RolePattern)).Count -eq 1) "Missing or duplicated source-role value '$RoleValue': $Locale"
  }

  $LowerTarget = $Target.ToLowerInvariant()
  foreach ($Sentinel in @(
    'pairs, tuples, cartesian products',
    'it follows from extensionality',
    'unordered pair',
    'how should we think about ordered pairs',
    'wiener--kuratowski definition',
    'having fixed a definition',
    'given sets',
    'cartesian product',
    'list all',
    'for every',
    'to visualize this',
    'show, by induction',
    'words, i.e.',
    'computer science',
    'by convention',
    'proyek logika'
  )) {
    Assert-True (-not $LowerTarget.Contains($Sentinel)) "Residual source/Indonesian prose '$Sentinel': $Locale"
  }
  $LatinRuns = @(Get-ProseLatinRuns $Target)
  Assert-True ($LatinRuns.Count -eq 0) "Residual Latin prose: $Locale runs=$($LatinRuns -join ',')"
  Assert-True (([regex]::Matches($Target, '[\u0600-\u06FF]')).Count -ge 100) "Insufficient target-script prose: $Locale"
  Assert-True (-not [regex]::IsMatch($Target, '[\u202A-\u202E\u2066-\u2069\uFB50-\uFDFF\uFE70-\uFEFF]')) "Bidi control or presentation-form code point: $Locale"
  if ($Locale -eq 'ar') {
    Assert-True (-not [regex]::IsMatch($Target, '[\u067E\u0686\u0698\u06A9\u06AF\u06CC]')) 'Persian code point in Arabic target'
  }
  else {
    Assert-True (-not [regex]::IsMatch($Target, '[\u0643\u0649\u064A]')) 'Arabic Kaf/Yeh code point in Persian target'
  }

  $TargetHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $TargetPath).Hash
  "OLP0009_STATIC_OK locale=$Locale target_sha256=$TargetHash commands=177 envs=30 tokens=12 math=78 labels=2 refs=1 assets=0 citations=0"
}
