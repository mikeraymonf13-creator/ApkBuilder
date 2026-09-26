# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-09-26 - Shell process execution in availability checks
**Learning:** Using `os.system("which <cmd>")` forks shell sub-processes every time binary availability is checked, introducing measurable process creation overhead and potential subshell escaping edge cases.
**Action:** Use Python's built-in `shutil.which(cmd) is not None` for in-process PATH lookup without subshell overhead.
