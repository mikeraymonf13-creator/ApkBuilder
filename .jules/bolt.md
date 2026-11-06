# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-05 - Avoid redundant stat syscalls during directory scans
**Learning:** `os.listdir()` returns string filenames, requiring explicit `os.path.isdir()`/`os.path.isfile()` stat syscalls for each entry. Replacing `os.listdir()` with `os.scandir()` leverages OS directory entry metadata (`d_type`), avoiding stat calls and string concatenations during file scans in build tasks.
**Action:** Use `os.scandir()` when scanning directories for files with specific extensions or filtering subdirectories.

## 2026-10-30 - Prune resource directories during library code traversals
**Learning:** In Android project dependencies (`.libs`), extracted AARs contain expansive `res/` and `assets/` subtrees with hundreds of localized directories. Searching for code assets (`.jar`) or manifests with unrestricted `os.walk` spends >80% of traversal time scanning non-code resource trees where JARs or manifests never exist.
**Action:** In dependency scanners, prune traversal branches matching `res` or `assets` when scanning for compiled code or manifest metadata.

## 2026-11-06 - Uncompressed DEX storage in APK packaging
**Learning:** Writing `.dex` files into APK archives with default `ZIP_DEFLATED` invokes heavy zlib Deflate compression across megabytes of bytecode, accounting for >90% of packaging time while offering minimal compression ratio. Android runtime also expects DEX entries to be uncompressed (page-aligned) so they can be memory-mapped directly from the APK at runtime without decompression.
**Action:** Always store `.dex` files uncompressed (`compress_type=zipfile.ZIP_STORED`) in APK packaging tasks.
