# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-02 - Redundant system PATH scans and SDK build-tools traversals
**Learning:** `shutil.which()` PATH scans and `os.listdir()` on Android SDK `build-tools` were executed repeatedly during tool binary resolution (`aapt2`, `javac`, `kotlinc`, `d8`, `apksigner`). Memoizing `get_bin()` with `@functools.lru_cache` reduced lookup latency from ~779ms to ~1.7ms.
**Action:** Memoize binary search lookups with `lru_cache` and cache `build-tools` version directory scans on the `Project` instance.
