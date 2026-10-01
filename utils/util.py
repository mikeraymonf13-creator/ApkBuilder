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

def get_bin(cmd):
    return shutil.which(cmd)

# BOLT OPTIMIZATION: Cache binary path lookup results using lru_cache.
# During build execution, tasks (Aapt2Task, JavaTask, KotlinTask, Task/D8, Task/ApkSigner)
# check executable availability repeatedly. Caching avoids redundant shutil.which and os.access filesystem calls.
@functools.lru_cache(maxsize=128)
def cmd_is_available(cmd):
    if not cmd:
        return False
    if os.path.isabs(cmd) or os.sep in cmd:
        return os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    return shutil.which(cmd) is not None
