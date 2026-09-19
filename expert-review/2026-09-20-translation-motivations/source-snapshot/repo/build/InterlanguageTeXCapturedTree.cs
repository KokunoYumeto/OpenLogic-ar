// Windows 10+ only. No shell expansion, breakaway permission, or unfenced fallback.
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Text;

namespace Interlanguage {
  public sealed class TeXTreeGuardV2 {
    static readonly object retentionLock = new object();
    static readonly List<object> retainedContainments = new List<object>();
    public static bool HasUnverifiedContainment {
      get { lock (retentionLock) { return retainedContainments.Count != 0; } }
    }
    public static void RetainUnverifiedContainment(object mutex, TeXTreeGuardV2 tree) {
      lock (retentionLock) { retainedContainments.Add(mutex); retainedContainments.Add(tree); }
    }
    IntPtr job, process, thread;
    bool closed;
    public uint RootProcessId { get; private set; }
    public bool AssignedBeforeResume { get; private set; }
    public bool RootExited { get; private set; }
    public int? RootExitCode { get; private set; }
    public uint ActiveProcesses { get; private set; }
    public uint TotalProcesses { get; private set; }
    public uint PeakObservedActiveProcesses { get; private set; }
    public bool TerminationRequested { get; private set; }
    public string CreatedSuspendedAtUtc { get; private set; }
    public string ResumedAtUtc { get; private set; }
    public string RootExitedAtUtc { get; private set; }
    public string TreeEmptyAtUtc { get; private set; }
    public string TerminationRequestedAtUtc { get; private set; }
    public string JobClosedAtUtc { get; private set; }

    [StructLayout(LayoutKind.Sequential)] struct BasicLimits {
      public long PerProcessUserTimeLimit, PerJobUserTimeLimit;
      public uint LimitFlags;
      public UIntPtr MinimumWorkingSetSize, MaximumWorkingSetSize;
      public uint ActiveProcessLimit;
      public UIntPtr Affinity;
      public uint PriorityClass, SchedulingClass;
    }
    [StructLayout(LayoutKind.Sequential)] struct IoCounters {
      public ulong ReadOperationCount, WriteOperationCount, OtherOperationCount;
      public ulong ReadTransferCount, WriteTransferCount, OtherTransferCount;
    }
    [StructLayout(LayoutKind.Sequential)] struct ExtendedLimits {
      public BasicLimits BasicLimitInformation;
      public IoCounters IoInfo;
      public UIntPtr ProcessMemoryLimit, JobMemoryLimit, PeakProcessMemoryUsed, PeakJobMemoryUsed;
    }
    [StructLayout(LayoutKind.Sequential)] struct Accounting {
      public long TotalUserTime, TotalKernelTime, ThisPeriodTotalUserTime, ThisPeriodTotalKernelTime;
      public uint TotalPageFaultCount, TotalProcesses, ActiveProcesses, TotalTerminatedProcesses;
    }
    [StructLayout(LayoutKind.Sequential, CharSet=CharSet.Unicode)] struct StartupInfo {
      public uint cb;
      public string lpReserved, lpDesktop, lpTitle;
      public uint dwX, dwY, dwXSize, dwYSize, dwXCountChars, dwYCountChars, dwFillAttribute, dwFlags;
      public short wShowWindow, cbReserved2;
      public IntPtr lpReserved2, hStdInput, hStdOutput, hStdError;
    }
    [StructLayout(LayoutKind.Sequential)] struct StartupInfoEx {
      public StartupInfo StartupInfo;
      public IntPtr lpAttributeList;
    }
    [StructLayout(LayoutKind.Sequential)] struct ProcessInformation {
      public IntPtr hProcess, hThread;
      public uint dwProcessId, dwThreadId;
    }
    [StructLayout(LayoutKind.Sequential)] struct SecurityAttributes {
      public uint nLength;
      public IntPtr lpSecurityDescriptor;
      [MarshalAs(UnmanagedType.Bool)] public bool bInheritHandle;
    }
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    static extern IntPtr CreateJobObjectW(IntPtr attributes, string name);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool SetInformationJobObject(IntPtr job, int infoClass, ref ExtendedLimits info, uint size);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool QueryInformationJobObject(IntPtr job, int infoClass, out Accounting info, uint size, IntPtr returnLength);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool TerminateJobObject(IntPtr job, uint exitCode);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool IsProcessInJob(IntPtr process, IntPtr job, out bool result);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool InitializeProcThreadAttributeList(IntPtr list, int count, uint flags, ref IntPtr size);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool UpdateProcThreadAttribute(IntPtr list, uint flags, IntPtr attribute, IntPtr value, IntPtr size, IntPtr previous, IntPtr returnedSize);
    [DllImport("kernel32.dll")] static extern void DeleteProcThreadAttributeList(IntPtr list);
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    static extern bool CreateProcessW(string application, StringBuilder commandLine, IntPtr processAttributes,
      IntPtr threadAttributes, bool inheritHandles, uint flags, IntPtr environment, string directory,
      ref StartupInfoEx startupInfo, out ProcessInformation processInformation);
    [DllImport("kernel32.dll", SetLastError=true)] static extern uint ResumeThread(IntPtr thread);
    [DllImport("kernel32.dll", SetLastError=true)] static extern uint WaitForSingleObject(IntPtr handle, uint milliseconds);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool GetExitCodeProcess(IntPtr handle, out uint code);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool TerminateProcess(IntPtr handle, uint code);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool CloseHandle(IntPtr handle);
    [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
    [DllImport("kernel32.dll", SetLastError=true)] static extern IntPtr GetStdHandle(int which);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool DuplicateHandle(IntPtr sourceProcess, IntPtr sourceHandle, IntPtr targetProcess,
      out IntPtr targetHandle, uint access, bool inheritHandle, uint options);
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    static extern IntPtr CreateFileW(string name, uint access, uint share, ref SecurityAttributes attributes,
      uint creation, uint flags, IntPtr template);

    static string Now() { return DateTimeOffset.UtcNow.ToString("o"); }
    static Win32Exception Error(string operation) {
      return new Win32Exception(Marshal.GetLastWin32Error(), operation + " failed; no unfenced fallback is allowed.");
    }
    public static string QuoteArgument(string value) {
      if (value == null) value = "";
      if (value.IndexOf('\0') >= 0) throw new ArgumentException("NUL in native argument.");
      StringBuilder result = new StringBuilder("\"");
      int slashes = 0;
      foreach (char c in value) {
        if (c == '\\') { slashes++; continue; }
        result.Append('\\', c == '"' ? slashes * 2 + 1 : slashes).Append(c);
        slashes = 0;
      }
      return result.Append('\\', slashes * 2).Append('"').ToString();
    }
    static IntPtr DuplicateStandardHandle(int which, bool input) {
      IntPtr original = GetStdHandle(which), duplicate;
      if (original == IntPtr.Zero || original == new IntPtr(-1)) {
        SecurityAttributes attributes = new SecurityAttributes();
        attributes.nLength = (uint)Marshal.SizeOf(typeof(SecurityAttributes));
        attributes.bInheritHandle = true;
        duplicate = CreateFileW("NUL", input ? 0x80000000u : 0x40000000u, 3, ref attributes, 3, 0, IntPtr.Zero);
        if (duplicate == new IntPtr(-1)) throw Error("CreateFile(NUL)");
      } else if (!DuplicateHandle(GetCurrentProcess(), original, GetCurrentProcess(), out duplicate, 0, true, 2)) {
        throw Error("DuplicateHandle(standard stream)");
      }
      return duplicate;
    }
    public void Start(string executable, string[] arguments, string directory) {
      if (job != IntPtr.Zero || closed) throw new InvalidOperationException("A guard can start only once.");
      job = CreateJobObjectW(IntPtr.Zero, null); // Unnamed, non-inheritable; only our tree.
      if (job == IntPtr.Zero) throw Error("CreateJobObject");
      ExtendedLimits limits = new ExtendedLimits();
      limits.BasicLimitInformation.LimitFlags = 0x2000; // KILL_ON_JOB_CLOSE; no breakaway.
      if (!SetInformationJobObject(job, 9, ref limits, (uint)Marshal.SizeOf(typeof(ExtendedLimits))))
        throw Error("SetInformationJobObject(KILL_ON_JOB_CLOSE)");
      IntPtr attributes = IntPtr.Zero, jobs = IntPtr.Zero, handles = IntPtr.Zero;
      bool initialized = false;
      List<IntPtr> standardHandles = new List<IntPtr>();
      try {
        IntPtr size = IntPtr.Zero;
        InitializeProcThreadAttributeList(IntPtr.Zero, 2, 0, ref size);
        if (size == IntPtr.Zero) throw Error("Size process attribute list");
        attributes = Marshal.AllocHGlobal(size);
        if (!InitializeProcThreadAttributeList(attributes, 2, 0, ref size)) throw Error("InitializeProcThreadAttributeList");
        initialized = true;
        jobs = Marshal.AllocHGlobal(IntPtr.Size);
        Marshal.WriteIntPtr(jobs, job);
        // Atomic job assignment prevents an orphan if the supervisor dies between create and resume.
        if (!UpdateProcThreadAttribute(attributes, 0, new IntPtr(0x2000D), jobs, new IntPtr(IntPtr.Size), IntPtr.Zero, IntPtr.Zero))
          throw Error("Set atomic job-list attribute (Windows 10+ required)");
        standardHandles.Add(DuplicateStandardHandle(-10, true));
        standardHandles.Add(DuplicateStandardHandle(-11, false));
        standardHandles.Add(DuplicateStandardHandle(-12, false));
        handles = Marshal.AllocHGlobal(IntPtr.Size * 3);
        for (int i = 0; i < 3; i++) Marshal.WriteIntPtr(handles, i * IntPtr.Size, standardHandles[i]);
        if (!UpdateProcThreadAttribute(attributes, 0, new IntPtr(0x20002), handles, new IntPtr(IntPtr.Size * 3), IntPtr.Zero, IntPtr.Zero))
          throw Error("Set inherited standard-handle list");
        StartupInfoEx startup = new StartupInfoEx();
        startup.StartupInfo.cb = (uint)Marshal.SizeOf(typeof(StartupInfoEx));
        startup.StartupInfo.dwFlags = 0x101; // USESTDHANDLES | USESHOWWINDOW (hidden).
        startup.StartupInfo.hStdInput = standardHandles[0];
        startup.StartupInfo.hStdOutput = standardHandles[1];
        startup.StartupInfo.hStdError = standardHandles[2];
        startup.lpAttributeList = attributes;
        StringBuilder commandLine = new StringBuilder(QuoteArgument(executable));
        foreach (string argument in arguments) commandLine.Append(' ').Append(QuoteArgument(argument));
        if (commandLine.Length >= 32767) throw new ArgumentException("Native command line exceeds Windows limit.");
        ProcessInformation info;
        // NO_WINDOW avoids an extra console window; explicit native standard handles remain valid.
        if (!CreateProcessW(executable, commandLine, IntPtr.Zero, IntPtr.Zero, true, 0x8080004,
              IntPtr.Zero, directory, ref startup, out info))
          throw Error("CreateProcessW(suspended, atomic job assignment)");
        process = info.hProcess; thread = info.hThread; RootProcessId = info.dwProcessId;
        CreatedSuspendedAtUtc = Now();
        bool member;
        if (!IsProcessInJob(process, job, out member)) throw Error("IsProcessInJob");
        if (!member) throw new InvalidOperationException("Root is not a job member; it will not be resumed.");
        AssignedBeforeResume = true;
        Poll();
        if (ResumeThread(thread) != 1) throw new InvalidOperationException("ResumeThread did not report exactly one suspended level.");
        ResumedAtUtc = Now();
        CloseHandle(thread); thread = IntPtr.Zero;
      } finally {
        if (initialized) DeleteProcThreadAttributeList(attributes);
        if (attributes != IntPtr.Zero) Marshal.FreeHGlobal(attributes);
        if (jobs != IntPtr.Zero) Marshal.FreeHGlobal(jobs);
        if (handles != IntPtr.Zero) Marshal.FreeHGlobal(handles);
        foreach (IntPtr handle in standardHandles) CloseHandle(handle);
      }
    }
    public void Poll() {
      if (closed) throw new InvalidOperationException("Captured job already closed.");
      if (process != IntPtr.Zero && !RootExited) {
        uint result = WaitForSingleObject(process, 0);
        if (result == 0) {
          uint code;
          if (!GetExitCodeProcess(process, out code)) throw Error("GetExitCodeProcess");
          RootExited = true; RootExitCode = unchecked((int)code); RootExitedAtUtc = Now();
        } else if (result != 258) throw Error("WaitForSingleObject(root)");
      }
      if (job != IntPtr.Zero) {
        Accounting accounting;
        if (!QueryInformationJobObject(job, 1, out accounting, (uint)Marshal.SizeOf(typeof(Accounting)), IntPtr.Zero))
          throw Error("QueryInformationJobObject(active-process accounting)");
        ActiveProcesses = accounting.ActiveProcesses; TotalProcesses = accounting.TotalProcesses;
        PeakObservedActiveProcesses = Math.Max(PeakObservedActiveProcesses, ActiveProcesses);
        if (ActiveProcesses == 0 && TreeEmptyAtUtc == null) TreeEmptyAtUtc = Now();
      }
    }
    public void RequestTermination() {
      if (TerminationRequested) return;
      Exception failure = null;
      if (job != IntPtr.Zero && !TerminateJobObject(job, 1)) failure = Error("TerminateJobObject(captured tree only)");
      // Also covers a failed membership assertion: this exact suspended process
      // handle is ours even if the OS did not report the expected job membership.
      if (process != IntPtr.Zero && WaitForSingleObject(process, 0) != 0 &&
          !TerminateProcess(process, 1) && WaitForSingleObject(process, 0) != 0)
        failure = Error("TerminateProcess(captured root only)");
      if (failure != null) throw failure;
      TerminationRequested = true; TerminationRequestedAtUtc = Now();
    }
    public void CloseVerifiedEmptyJob() {
      Poll();
      if (ActiveProcesses != 0 || (process != IntPtr.Zero && !RootExited))
        throw new InvalidOperationException("Refusing to close a nonempty job or live captured root.");
      if (thread != IntPtr.Zero) { CloseHandle(thread); thread = IntPtr.Zero; }
      if (process != IntPtr.Zero) { CloseHandle(process); process = IntPtr.Zero; }
      if (job != IntPtr.Zero) {
        if (!CloseHandle(job)) throw Error("CloseHandle(empty job)");
        job = IntPtr.Zero;
      }
      closed = true; JobClosedAtUtc = Now();
    }
  }
}
