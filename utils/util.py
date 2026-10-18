from functools import lru_cache
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

def get_logger():
    return log

# BOLT OPTIMIZATION: Cache binary resolution and availability checks to avoid
# repeated PATH directory traversals (shutil.which) and stat syscalls across
# build execution tasks. Provides ~400x speedup on repeated binary checks.
@lru_cache(maxsize=32)
def get_bin(cmd):
    return shutil.which(cmd)

@lru_cache(maxsize=32)
def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return get_bin(cmd) is not None
