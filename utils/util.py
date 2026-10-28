from utils.color_formatter import ColorFormatter
import os
import subprocess
import logging
import shutil
from functools import lru_cache

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

# BOLT OPTIMIZATION: Cache executable binary resolution in get_bin to avoid
# repeated PATH traversals and filesystem stats across build steps.
@lru_cache(maxsize=128)
def get_bin(cmd):
    return shutil.which(cmd)

# BOLT OPTIMIZATION: Cache binary availability checks to eliminate repeated
# os.path.isfile(), os.access(), and shutil.which() syscalls during build tasks.
@lru_cache(maxsize=128)
def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return shutil.which(cmd) is not None
