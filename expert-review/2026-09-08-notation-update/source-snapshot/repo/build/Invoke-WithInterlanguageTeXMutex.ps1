<#
Windows 10+ is required for atomic create-in-job. No unfenced fallback is used.
Native stdout/stderr are inherited unchanged; redirect the hosting executable
for logs. PowerShell-only pipelines around this script do not capture native
writes. The job covers ordinary CreateProcess descendants, not work deliberately
delegated to external services (WMI, Task Scheduler, etc.).
#>
param(
  [Parameter(Mandatory = $true)]
  [string]$Command,

  [string[]]$CommandArguments = @(),

  [ValidateRange(1, 3600)]
  [int]$AcquisitionTimeoutSeconds = 600,

  [string]$ReceiptPath = ""
)

$ErrorActionPreference = "Stop"
$global:LASTEXITCODE = 1
if (-not ('Interlanguage.TeXTreeGuardV2' -as [type])) {
  Add-Type -Path (Join-Path $PSScriptRoot 'InterlanguageTeXCapturedTree.cs')
}
if ([Interlanguage.TeXTreeGuardV2]::HasUnverifiedContainment) {
  throw 'This host retains an unverified captured tree; refusing another command or recursive mutex acquisition.'
}
$mutexName = "Global\InterlanguageTeXSlotV1"
$mutex = [Threading.Mutex]::new($false, $mutexName)
$acquired = $false
$abandoned = $false
$tree = $null
$treeDrained = $false
$commandExitCode = $null
$startedAt = [DateTimeOffset]::UtcNow
$receipt = [ordered]@{
  Schema = "interlanguage-tex-mutex/v2"
  Mutex = $mutexName
  Acquired = $false
  AbandonedMutexRecovered = $false
  StartedAtUtc = $startedAt.ToString("o")
  Status = "ACQUIRING"
  Containment = "Windows Job Object; atomic job assignment; suspended start; kill-on-close; no breakaway"
  OutputTransport = "inherited native standard handles (outer-process redirection supported)"
}

function Save-MutexReceipt {
  if (-not [string]::IsNullOrWhiteSpace($ReceiptPath)) {
    $parent = Split-Path -Parent $ReceiptPath
    if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    [IO.File]::WriteAllText($ReceiptPath, (($receipt | ConvertTo-Json -Depth 5) + "`n"), [Text.UTF8Encoding]::new($false))
  }
}

function Update-TreeReceipt {
  if ($null -ne $tree) {
    $receipt.Tree = [ordered]@{
      RootProcessId = $tree.RootProcessId
      AssignedBeforeResume = $tree.AssignedBeforeResume
      CreatedSuspendedAtUtc = $tree.CreatedSuspendedAtUtc
      ResumedAtUtc = $tree.ResumedAtUtc
      RootExitedAtUtc = $tree.RootExitedAtUtc
      RootExitCode = $tree.RootExitCode
      TreeEmptyAtUtc = $tree.TreeEmptyAtUtc
      FinalActiveProcesses = $tree.ActiveProcesses
      TotalProcesses = $tree.TotalProcesses
      PeakObservedActiveProcesses = $tree.PeakObservedActiveProcesses
      TerminationRequested = $tree.TerminationRequested
      TerminationRequestedAtUtc = $tree.TerminationRequestedAtUtc
      JobClosedAtUtc = $tree.JobClosedAtUtc
      DrainVerified = $treeDrained
    }
  }
}

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
  if ([Interlanguage.TeXTreeGuardV2]::HasUnverifiedContainment) {
    throw 'This host retains an unverified captured tree; refusing to launch.'
  }

  $receipt.Acquired = $true
  $receipt.AcquiredAtUtc = [DateTimeOffset]::UtcNow.ToString("o")
  $receipt.AbandonedMutexRecovered = $abandoned
  $receipt.Status = "RUNNING"
  Save-MutexReceipt # Persist abandoned recovery before any command launch.
  $resolved = Get-Command -Name $Command -CommandType Application, ExternalScript -ErrorAction Stop | Select-Object -First 1
  $executable = $resolved.Source
  $nativeArguments = @($CommandArguments)
  if ($resolved.CommandType -eq 'ExternalScript') {
    if ([IO.Path]::GetExtension($executable) -ne '.ps1') { throw "Use an explicit native interpreter for '$Command'." }
    $nativeArguments = @('-NoProfile', '-File', $executable) + $nativeArguments
    $executable = (Get-Process -Id $PID).Path
  } elseif ([IO.Path]::GetExtension($executable) -notin @('.exe', '.com')) {
    throw "Use an explicit native interpreter for '$Command'."
  }
  $location = Get-Location
  if ($location.Provider.Name -ne 'FileSystem') { throw 'The guarded command requires a filesystem working directory.' }
  $receipt.Command = $executable
  $receipt.WorkingDirectory = $location.ProviderPath
  $tree = [Interlanguage.TeXTreeGuardV2]::new()
  $tree.Start($executable, [string[]]$nativeArguments, $location.ProviderPath)
  Update-TreeReceipt
  Save-MutexReceipt
  do {
    $tree.Poll()
    if ($tree.RootExited) {
      $commandExitCode = [int]$tree.RootExitCode
      if ($commandExitCode -ne 0) { throw "TeX command failed with exit code ${commandExitCode}: $Command" }
    }
    if ($tree.ActiveProcesses -ne 0) { Start-Sleep -Milliseconds 100 }
  } while (-not $tree.RootExited -or $tree.ActiveProcesses -ne 0)
  $receipt.Status = "PASS"
} catch {
  $receipt.Status = "FAIL"
  $receipt.Failure = $_.Exception.Message
  throw
} finally {
  try {
    # Only this unnamed job is terminated. Never enumerate or kill foreign PIDs.
    if ($null -ne $tree) {
      $tree.Poll()
      if ($tree.ActiveProcesses -ne 0 -or ($tree.RootProcessId -ne 0 -and -not $tree.RootExited)) {
        $tree.RequestTermination()
        $receipt.Status = "FAIL"
        Update-TreeReceipt
        # Do not release on a timer while captured work might still be alive.
        do {
          $tree.Poll()
          if ($tree.ActiveProcesses -ne 0 -or -not $tree.RootExited) { Start-Sleep -Milliseconds 100 }
        } while ($tree.ActiveProcesses -ne 0 -or ($tree.RootProcessId -ne 0 -and -not $tree.RootExited))
      }
      if ($null -eq $commandExitCode -and $tree.RootExited) { $commandExitCode = [int]$tree.RootExitCode }
      $tree.CloseVerifiedEmptyJob()
    }
    $treeDrained = $true
    Update-TreeReceipt
  } catch {
    $receipt.Status = "FAIL"
    $receipt.CleanupFailure = $_.Exception.Message
    # A failed observation must not prevent an independent captured-tree kill.
    try { if ($null -ne $tree) { $tree.RequestTermination() } } catch {
      $receipt.CleanupTerminationFailure = $_.Exception.Message
    }
    $receipt.MutexIntentionallyRetained = $true
    # The process-level latch also rejects another runspace or recursive owner.
    [Interlanguage.TeXTreeGuardV2]::RetainUnverifiedContainment($mutex, $tree)
    throw
  } finally {
    $receipt.FinishedAtUtc = [DateTimeOffset]::UtcNow.ToString("o")
    $receipt.ExitCode = if ($null -eq $commandExitCode -or ($receipt.Status -ne 'PASS' -and $commandExitCode -eq 0)) { 1 } else { $commandExitCode }
    if ($null -ne $commandExitCode -and $commandExitCode -ne 0) { $global:LASTEXITCODE = $commandExitCode }
    try {
      Save-MutexReceipt
    } finally {
      if ($treeDrained) {
        if ($acquired) { $mutex.ReleaseMutex() }
        $mutex.Dispose()
      }
    }
  }
}

$global:LASTEXITCODE = 0 # Only after drain, receipt persistence and mutex release succeeded.
[pscustomobject]@{
  Mutex = $mutexName
  Acquired = $true
  AbandonedMutexRecovered = $abandoned
  Command = $Command
  StartedAtUtc = $startedAt.ToString("o")
  FinishedAtUtc = $receipt.FinishedAtUtc
  ExitCode = $commandExitCode
  Tree = $receipt.Tree
}
