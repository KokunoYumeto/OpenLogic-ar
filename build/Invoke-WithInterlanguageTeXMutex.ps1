param(
  [Parameter(Mandatory = $true)]
  [string]$Command,

  [string[]]$CommandArguments = @(),

  [ValidateRange(1, 3600)]
  [int]$AcquisitionTimeoutSeconds = 600
)

$ErrorActionPreference = "Stop"
$mutexName = "Global\InterlanguageTeXSlotV1"
$mutex = [Threading.Mutex]::new($false, $mutexName)
$acquired = $false
$abandoned = $false
$startedAt = [DateTimeOffset]::UtcNow

try {
  try {
    $acquired = $mutex.WaitOne([TimeSpan]::FromSeconds($AcquisitionTimeoutSeconds))
  } catch [Threading.AbandonedMutexException] {
    $acquired = $true
    $abandoned = $true
  }

  if (-not $acquired) {
    throw "Timed out acquiring the machine-wide TeX mutex '$mutexName'."
  }

  & $Command @CommandArguments
  $commandExitCode = $LASTEXITCODE
  if ($null -ne $commandExitCode -and $commandExitCode -ne 0) {
    throw "TeX command failed with exit code ${commandExitCode}: $Command"
  }

  [pscustomobject]@{
    Mutex = $mutexName
    Acquired = $true
    AbandonedMutexRecovered = $abandoned
    Command = $Command
    StartedAtUtc = $startedAt.ToString("o")
    FinishedAtUtc = [DateTimeOffset]::UtcNow.ToString("o")
    ExitCode = if ($null -eq $commandExitCode) { 0 } else { $commandExitCode }
  }
} finally {
  if ($acquired) {
    $mutex.ReleaseMutex()
  }
  $mutex.Dispose()
}
