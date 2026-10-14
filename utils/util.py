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

# BOLT OPTIMIZATION: Caches for binary location resolution and binary availability checks
# to avoid redundant $PATH environment traversals and stat/access syscalls across build tasks.
_bin_cache = {}
_cmd_availability_cache = {}

def get_logger():
    return log

def get_bin(cmd):
    if cmd not in _bin_cache:
        _bin_cache[cmd] = shutil.which(cmd)
    return _bin_cache[cmd]

def cmd_is_available(cmd):
    if not cmd:
        return False
    if cmd not in _cmd_availability_cache:
        if os.path.isabs(cmd) or os.sep in cmd:
            _cmd_availability_cache[cmd] = os.path.isfile(cmd) and os.access(cmd, os.X_OK)
        else:
            _cmd_availability_cache[cmd] = shutil.which(cmd) is not None
    return _cmd_availability_cache[cmd]
