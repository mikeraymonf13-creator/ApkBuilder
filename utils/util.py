from utils.color_formatter import ColorFormatter
import functools
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

def get_logger():
    return log

def get_bin(cmd):
    return shutil.which(cmd)

# BOLT OPTIMIZATION: Memoize binary availability checks with LRU cache.
# Each build task (Aapt2, Javac, Kotlinc, D8, Apksigner) repeatedly calls
# cmd_is_available during prepare() and start(). Caching avoids redundant
# shutil.which PATH iterations and filesystem stat/access syscalls.
@functools.lru_cache(maxsize=128)
def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return shutil.which(cmd) is not None
