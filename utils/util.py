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

# BOLT OPTIMIZATION: Cache binary resolution with lru_cache to eliminate
# redundant $PATH directory iterations and stat syscalls across build tasks.
@functools.lru_cache(maxsize=128)
def get_bin(cmd):
    return shutil.which(cmd)

def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return get_bin(cmd) is not None
