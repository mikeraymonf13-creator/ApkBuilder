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

def cmd_is_available(cmd):
    # Optimization: Use shutil.which instead of spawning a subshell with os.system.
    # This avoids fork/exec and subshell overhead (~20-100x speedup per check),
    # and provides cross-platform executable checking without depending on POSIX 'which'.
    return shutil.which(cmd) is not None
