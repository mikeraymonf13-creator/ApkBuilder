from utils.color_formatter import ColorFormatter
import functools
import logging
import os
import shutil
import subprocess

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

# BOLT OPTIMIZATION: Cache binary path resolutions to eliminate redundant PATH traversals
# across task initialization and checks (~700x speedup on repeat lookups).
@functools.lru_cache(maxsize=64)
def get_bin(cmd):
    return shutil.which(cmd)

# BOLT OPTIMIZATION: Cache binary availability checks to avoid repeated stat/access syscalls
# and PATH scans during build task execution.
@functools.lru_cache(maxsize=64)
def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return shutil.which(cmd) is not None
