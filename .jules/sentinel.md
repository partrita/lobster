## 2024-05-24 - Avoid Command Injection via subprocess shell=True

**Vulnerability:** Command injection vulnerability (B602: subprocess_popen_with_shell_equals_true) discovered when `subprocess.check_output(..., shell=True)` was used with unsanitized file paths containing command-line pipelines (using `cat`, `grep`, `awk`, `cut`). This allows potential arbitrary command execution if an attacker controls `self.root` or `self.data_file` paths.

**Learning:** Shell pipelines cannot simply be safely passed using string concatenation with `shell=True`, and even if input is believed to be safe, `shell=True` exposes the application to significant risks if future assumptions change. We need a way to construct bash-like pipelines explicitly without relying on a shell interpreter.

**Prevention:** Always avoid using `shell=True` in `subprocess` calls. To achieve piping behavior natively in python, launch each command using `subprocess.Popen` with an array of arguments, chaining them by passing the `stdout` of the previous process to the `stdin` of the next process (e.g., `stdin=p1.stdout, stdout=subprocess.PIPE`). Ensure file streams are explicitly closed on parent objects where appropriate (e.g., `p1.stdout.close()`) to prevent deadlock.
## 2024-11-06 - Replacing os.system with Secure Subprocess Run

**Vulnerability:** Command injection vulnerability (B605: start_process_with_a_shell) discovered when using `os.system` with file paths constructed via string concatenation. An attacker could potentially embed command control characters into a file path, compromising the system.

**Learning:** `os.system` runs commands via the shell, which means any user-controlled input or filename with spaces/special characters can lead to command injection.

**Prevention:** Always use `subprocess.run` (or similar functions from `subprocess`) with a list of arguments (`shell=False`) instead of `os.system` when executing external commands. Use `check=True` to ensure the command succeeds.
