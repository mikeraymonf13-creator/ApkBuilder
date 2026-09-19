## 2025-05-18 - Avoid subshell invocation via os.system for command existence checks
**Learning:** Using `os.system("which <cmd>")` invokes a shell subprocess incurring ~4ms overhead per check, whereas `shutil.which("<cmd>")` uses Python native path lookup in ~0.17ms (~25x faster).
**Action:** Always prefer `shutil.which` over spawning `os.system("which ...")` or `subprocess` subshells when checking command availability in Python.
