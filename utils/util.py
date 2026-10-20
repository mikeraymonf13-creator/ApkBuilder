from utils.color_formatter import ColorFormatter
from functools import lru_cache
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

# BOLT OPTIMIZATION: Cache binary path lookups and executable status checks.
# Prevents repeated PATH environment traversals and stat/access syscalls
# when checking binary availability across multiple build tasks (AAPT2, Javac, Kotlinc, D8, Apksigner).
@lru_cache(maxsize=128)
def get_bin(cmd):
    return shutil.which(cmd)

@lru_cache(maxsize=128)
def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return shutil.which(cmd) is not None
