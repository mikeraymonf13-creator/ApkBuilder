import functools
import os
import subprocess
import logging
import shutil
from utils.color_formatter import ColorFormatter

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

# BOLT OPTIMIZATION: Cache binary path lookups in system PATH to eliminate
# redundant disk/environment scans across multiple build steps and project init.
@functools.lru_cache(maxsize=64)
def get_bin(cmd):
    if not cmd:
        return None
    return shutil.which(cmd)

def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return get_bin(cmd) is not None
