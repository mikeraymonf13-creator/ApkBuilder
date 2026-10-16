# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-05 - Avoid redundant stat syscalls during directory scans
**Learning:** `os.listdir()` returns string filenames, requiring explicit `os.path.isdir()`/`os.path.isfile()` stat syscalls for each entry. Replacing `os.listdir()` with `os.scandir()` leverages OS directory entry metadata (`d_type`), avoiding stat calls and string concatenations during file scans in build tasks.
**Action:** Use `os.scandir()` when scanning directories for files with specific extensions or filtering subdirectories.

## 2026-10-16 - Deduplicate DEX files during APK packaging
**Learning:** When multiple library JAR files reside in the same directory, directory file scans return the same `.dex` file path multiple times. Packaging without path tracking leads to duplicate `.dex` entries written to the output APK, inflating file size and causing redundant zip compression I/O. Furthermore, short-circuiting file extension matching (`entry.name.endswith(suffix)`) before `entry.is_file()` during `os.scandir()` traversals avoids unnecessary file metadata queries for non-matching files.
**Action:** Maintain a `visited` set when packaging DEX files and evaluate string suffixes before checking file types in filesystem directory scans.
