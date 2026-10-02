# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-09-22 - Repeated binary PATH traversal and availability checks
**Learning:** `get_bin()` and `cmd_is_available()` in `utils/util.py` execute `shutil.which` and filesystem stat/access checks on every call. Build tasks check binary availability repeatedly, causing redundant PATH environment traversals and system calls.
**Action:** Apply `@lru_cache(maxsize=128)` to `get_bin` and `cmd_is_available` to eliminate redundant binary lookups.
