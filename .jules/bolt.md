# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-05 - Avoid redundant stat syscalls during directory scans
**Learning:** `os.listdir()` returns string filenames, requiring explicit `os.path.isdir()`/`os.path.isfile()` stat syscalls for each entry. Replacing `os.listdir()` with `os.scandir()` leverages OS directory entry metadata (`d_type`), avoiding stat calls and string concatenations during file scans in build tasks.
**Action:** Use `os.scandir()` when scanning directories for files with specific extensions or filtering subdirectories.

## 2026-10-21 - Eliminate redundant stat syscalls before os.scandir
**Learning:** Pre-checking directory existence or type with `os.path.isdir()` or `os.stat()` before calling `os.scandir()` issues redundant stat system calls (`stat` followed by `getdents`/`openat`). Directly invoking `os.scandir()` within a `try...except OSError` block safely handles missing or non-directory paths while eliminating extra stat system calls.
**Action:** Invoke `os.scandir()` directly inside `try...except OSError` (or `NotADirectoryError`) instead of guarding with `os.path.isdir()` or `os.stat()`.
