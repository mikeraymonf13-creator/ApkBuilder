# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-09-28 - Redundant SDK build-tools directory listing during binary resolution
**Learning:** `Project.__resolve_bin()` listed and sorted the `build-tools` directory every time a tool (`aapt2`, `javac`, `kotlinc`, `d8`, `apksigner`) was resolved, resulting in up to 5 redundant disk directory listings per project initialization.
**Action:** Cache `_build_tools_versions` on the `Project` instance during `__resolve_bin()` to scan `build-tools` at most once per project instance.
