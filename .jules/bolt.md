# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-05 - Avoid redundant stat syscalls during directory scans
**Learning:** `os.listdir()` returns string filenames, requiring explicit `os.path.isdir()`/`os.path.isfile()` stat syscalls for each entry. Replacing `os.listdir()` with `os.scandir()` leverages OS directory entry metadata (`d_type`), avoiding stat calls and string concatenations during file scans in build tasks.
**Action:** Use `os.scandir()` when scanning directories for files with specific extensions or filtering subdirectories.

## 2026-10-11 - Do not replace Python's built-in os.walk with custom recursion
**Learning:** `os.walk()` in Python 3.5+ (PEP 471) already uses `os.scandir()` internally. Writing custom recursive `os.scandir()` helpers does not provide performance gains over `os.walk()` and risks introducing infinite loops with directory symlink cycles or `RecursionError` on deep paths.
**Action:** Keep `os.walk()` for recursive directory tree traversals and use `os.scandir()` only for shallow single-directory scans.
