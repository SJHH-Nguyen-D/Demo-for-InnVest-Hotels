import logging
import os
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings


def clean_printer(name: str, ln: int, module: str, var):
    print("\n")
    print("+++++++++++++++++++++++++++")
    print("\n")
    print(
        f"This is the variable under inspection <{name}>",
        "On line ",
        ln,
        f"in module <{module}>",
        "with type:",
        type(var),
        "with value:",
        var,
    )
    print("\n")
    print("+++++++++++++++++++++++++++")
    print("\n")


def create_logger():
    """
    Creates a logging object and returns it
    """
    _logger = logging.getLogger("\n================= LOGGER =================\n")
    _logger.setLevel(settings.LOG_LEVEL)
    # create the logging file handler

    logpath = "/var/log/"
    logfile = "apogee.log"

    try:
        logdir = os.path.join(logpath, logfile)
        if not os.path.exists(logdir):
            Path(logdir).touch(exist_ok=True)
    except PermissionError:
        logpath = "../" + logpath
        logdir = os.path.join(logpath, logfile)
        if not os.path.exists(logpath):
            os.makedirs(logpath)
        if not os.path.exists(logdir):
            Path(logdir).touch(exist_ok=True)

    os.chmod(logdir, 0o644)
    fh = RotatingFileHandler(logdir, backupCount=5, maxBytes=2_560_000)
    sh = StreamHandler(sys.stderr)
    fmt = "\n%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    _logger.addHandler(fh)
    _logger.addHandler(sh)
    return _logger


logger = create_logger()
