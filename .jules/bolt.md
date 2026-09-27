# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-09-27 - Avoid os.system for binary detection
**Learning:** Using `os.system("which <cmd>")` forks a subshell process for every binary check, incurring significant OS process creation overhead (~4ms per check). Using Python's native `shutil.which(cmd) is not None` executes entirely in Python without subshells (~0.02ms per check, ~170x faster).
**Action:** Use `shutil.which(cmd) is not None` instead of `os.system("which ...")` for command availability checks.
