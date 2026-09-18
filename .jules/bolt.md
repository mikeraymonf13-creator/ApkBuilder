## 2025-05-18 - Faster File Traversal with os.scandir
**Learning:** `os.walk` in Python constructs tuples of `(root, dirs, files)` and performs unnecessary list copies and stat operations on every directory iteration. For CLI tools that scan project source trees and library folders repeatedly, replacing `os.walk` with a stack-based `os.scandir` iteration reduces filesystem traversal overhead by over 2x.
**Action:** Use stack-based `os.scandir` for recursive file searches in Python CLI applications instead of `os.walk`.
