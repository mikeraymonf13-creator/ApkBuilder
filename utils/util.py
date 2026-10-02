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

@functools.lru_cache(maxsize=128)
def get_bin(cmd):
    # BOLT OPTIMIZATION: Cache binary resolution to avoid repeating expensive PATH scans via shutil.which.
    return shutil.which(cmd)

@functools.lru_cache(maxsize=128)
def cmd_is_available(cmd):
    # BOLT OPTIMIZATION: Cache binary availability checks to avoid redundant filesystem checks (os.access / shutil.which).
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return shutil.which(cmd) is not None
