# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-03 - Repeated build-tools directory listing in binary resolution
**Learning:** `Project.__resolve_bin()` scanned and sorted `os.listdir(build_tools_dir)` for every binary fallback (aapt2, javac, kotlinc, d8, apksigner). Scoping the cached version list to the `Project` instance safely avoids 4 redundant disk listings per build initialization without introducing stale global state.
**Action:** Cache instance-specific SDK directory listings on `Project` rather than process-global `lru_cache`.
