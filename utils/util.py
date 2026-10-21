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

_cmd_availability_cache = {}

def cmd_is_available(cmd):
    # BOLT OPTIMIZATION: Cache binary availability lookups to avoid repeated
    # shutil.which PATH scans and os.access stat syscalls during task execution.
    if not cmd:
        return False
    if cmd in _cmd_availability_cache:
        return _cmd_availability_cache[cmd]

    if os.path.isabs(cmd) or os.sep in cmd:
        res = os.path.isfile(cmd) and os.access(cmd, os.X_OK)
    else:
        res = shutil.which(cmd) is not None

    _cmd_availability_cache[cmd] = res
    return res
