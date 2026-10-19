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

def get_bin(cmd):
    return shutil.which(cmd)

# BOLT OPTIMIZATION: Cache binary availability checks in-memory to avoid repeated
# filesystem stat syscalls (os.path.isfile/os.access) and PATH directory scans (shutil.which)
# across multiple build tasks (aapt2, javac, kotlinc, d8, apksigner, java).
_cmd_availability_cache = {}

def cmd_is_available(cmd):
    if not cmd:
        return False
    if cmd not in _cmd_availability_cache:
        if os.path.isabs(cmd) or os.sep in cmd:
            _cmd_availability_cache[cmd] = os.path.isfile(cmd) and os.access(cmd, os.X_OK)
        else:
            _cmd_availability_cache[cmd] = shutil.which(cmd) is not None
    return _cmd_availability_cache[cmd]
