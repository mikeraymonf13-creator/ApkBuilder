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

## 2026-11-06 - Redundant PATH traversals in executable checks
**Learning:** `shutil.which` and `os.access` checks across separate compilation pipeline tasks repeatedly traverse every directory listed in `PATH` to locate the same compiler tools (`javac`, `d8`, `aapt2`, `apksigner`). Because system PATH and binaries remain static during process lifetime, executing uncached disk searches imposes significant syscall overhead.
**Action:** Cache binary availability queries with `@functools.lru_cache` in utility modules to eliminate repeated filesystem PATH scans.
