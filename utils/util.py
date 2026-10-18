from utils.color_formatter import ColorFormatter
import os
import subprocess
import logging
import shutil

handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter(
    "[%(asctime)s] [%(levelname)s] %(message)s"
))

log = logging.getLogger("builder")
log.setLevel(logging.INFO)
log.addHandler(handler)
log.propagate = False

def run(cmd):
    subprocess.check_call(
        cmd,
        stdout=subprocess.DEVNULL
    )

import functools

def get_logger():
    return log

# BOLT OPTIMIZATION: Memoize binary path resolutions and availability checks
# to avoid redundant PATH directory scans (shutil.which) and stat/access syscalls
# (os.path.isfile / os.access) across build pipeline tasks (Aapt2, Java, Kotlin, D8, Packager).
@functools.lru_cache(maxsize=64)
def get_bin(cmd):
    return shutil.which(cmd)

@functools.lru_cache(maxsize=64)
def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return shutil.which(cmd) is not None
