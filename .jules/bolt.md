# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-05 - Avoid redundant stat syscalls during directory scans
**Learning:** `os.listdir()` returns string filenames, requiring explicit `os.path.isdir()`/`os.path.isfile()` stat syscalls for each entry. Replacing `os.listdir()` with `os.scandir()` leverages OS directory entry metadata (`d_type`), avoiding stat calls and string concatenations during file scans in build tasks.
**Action:** Use `os.scandir()` when scanning directories for files with specific extensions or filtering subdirectories.

## 2026-10-23 - Deduplicate library directory scans across build tasks
**Learning:** Multiple build tasks (`Aapt2Task`, `DexerTask`, and `PackagerTask`) iterate over `Project.find_lib_jars()` and process `os.path.dirname(library)`. When a library directory contains multiple `.jar` files, these tasks ran redundant filesystem searches (`find_files`), duplicate `.dex` packaging, and duplicate subprocess invocations (`aapt2 compile`).
**Action:** Track visited library directories using a `set()` when iterating over `find_lib_jars()` in build tasks to ensure directory scans and compilation commands execute at most once per library directory.
