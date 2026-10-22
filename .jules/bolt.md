# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-05 - Avoid redundant stat syscalls during directory scans
**Learning:** `os.listdir()` returns string filenames, requiring explicit `os.path.isdir()`/`os.path.isfile()` stat syscalls for each entry. Replacing `os.listdir()` with `os.scandir()` leverages OS directory entry metadata (`d_type`), avoiding stat calls and string concatenations during file scans in build tasks.
**Action:** Use `os.scandir()` when scanning directories for files with specific extensions or filtering subdirectories.

## 2026-10-22 - Avoid redundant os.stat before os.scandir and duplicate library DEX packaging
**Learning:** `os.scandir()` directly raises `NotADirectoryError` for file targets and `FileNotFoundError` for missing paths, rendering a preliminary `os.stat()` check redundant and wasteful. Additionally, when multiple library JAR files reside in the same folder, searching each library's folder for `.dex` files without tracking processed DEX paths causes duplicate DEX writes to the APK archive.
**Action:** Call `os.scandir()` directly and catch `NotADirectoryError` instead of checking `os.stat()`. Maintain a `seen_dex_files` set in packaging tasks to avoid duplicate ZIP write operations.
