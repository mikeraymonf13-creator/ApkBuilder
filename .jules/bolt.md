# Bolt's Journal

## 2026-09-21 - Repeated filesystem traversal in build tasks
**Learning:** `Project.find_lib_jars()` and `Project.get_lib_package_names()` perform full `os.walk` directory tree scans and XML parsing on every call. Multiple build tasks (Aapt2, Javac, Kotlinc, D8, Packager) call these methods repeatedly during a single build execution, causing redundant disk I/O.
**Action:** Cache the result of `find_lib_jars()` and `get_lib_package_names()` on the `Project` instance during build execution.

## 2026-10-02 - Recursive os.walk when searching for library dex files
**Learning:** `find_files(library_dir, ".dex")` ran `os.walk` recursively over library directories, scanning thousands of files in deep `res/` subtrees (layouts, drawables, values). Since D8 outputs `.dex` files at the top level of library output directories, `os.listdir` via `find_dex_files(library_dir)` is ~80x faster.
**Action:** Always use top-level `os.listdir` or `find_dex_files(target_dir)` when locating `.dex` files instead of generic `find_files` directory tree scans.
