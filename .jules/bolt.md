# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-09-24 - Subshell execution in PATH executable lookup
**Learning:** Using `os.system("which <cmd> > /dev/null")` spawns an entire `/bin/sh` subshell process for every binary check, causing ~3.6ms per check due to process creation overhead. Python's `shutil.which` combined with `@functools.lru_cache` performs direct PATH resolution in pure Python in under ~0.001ms.
**Action:** Always prefer `shutil.which` and `functools.lru_cache` over `os.system` or `subprocess` calls when checking tool/binary availability in Python.
