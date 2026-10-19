from utils.color_formatter import ColorFormatter
import os
import subprocess
import logging
import shutil
import functools

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

# BOLT OPTIMIZATION: Cache binary path resolution to avoid scanning system PATH
# directories repeatedly across tasks during project initialization and pre-checks.
@functools.lru_cache(maxsize=32)
def get_bin(cmd):
    return shutil.which(cmd)

# BOLT OPTIMIZATION: Cache binary availability check to avoid stat/access syscalls
# and shutil.which PATH scans on repeated binary checks across build steps.
@functools.lru_cache(maxsize=32)
def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return shutil.which(cmd) is not None
