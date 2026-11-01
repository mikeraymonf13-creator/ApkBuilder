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

## 2026-11-01 - Avoid unrestricted recursive file search for library dex discovery
**Learning:** `Project.find_files(library_dir, ".dex")` performs an unpruned recursive tree traversal and stat checks per library across both Dexer and Packager tasks. Extracted AAR library directories contain extensive `res/` and `assets/` trees where DEX files are never located, creating unnecessary filesystem traversal overhead across dozens of dependency libraries.
**Action:** Use a dedicated `find_lib_dex_files(library_dir)` scan that prunes `res` and `assets` trees and avoids stat overhead when discovering library DEX files in Dexer and Packager tasks.
