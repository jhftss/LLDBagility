#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import functools
import logging
import os
import struct

BOLD = "\033[1m"
RED = "\033[91m"
CLEAR = "\033[0m"
LLDBAGILITY = BOLD + RED + "LLDBagility" + CLEAR


def p32(i):
    return struct.pack("<I", i)


def p64(i):
    return struct.pack("<Q", i)


def u32(s):
    return struct.unpack("<I", s)[0]


def u64(s):
    return struct.unpack("<Q", s)[0]


def create_logger(name, filename):
    filehandler = logging.FileHandler(filename, mode="w")
    filehandler.setFormatter(
        logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    )
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.addHandler(filehandler)
    logger.setLevel(os.getenv("LOGLEVEL", default="WARNING").upper())
    return logger


def create_indented_logger(name, filename):
    filehandler = logging.FileHandler(filename, mode="w")
    filehandler.setFormatter(
        logging.Formatter("%(asctime)s %(name)s %(levelname)s %(prefix)s%(message)s")
    )
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.addHandler(filehandler)
    logger.setLevel(os.getenv("LOGLEVEL", default="WARNING").upper())
    return logging.LoggerAdapter(logger, {"prefix": ""})


# https://stackoverflow.com/questions/26853675/nested-prefixes-accross-loggers-in-python
def indented(logger, prefix=list()):
    def decorator(f):
        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            prefix.append("")
            logger.extra["prefix"] = "|  ".join(prefix)
            res = f(*args, **kwargs)
            prefix.pop()
            logger.extra["prefix"] = "|  ".join(prefix)
            return res

        return _wrapper

    return decorator


# https://github.com/GrahamDumpleton/wrapt/blob/4ee35415a4b0d570ee6a9b3a14a6931441aeab4b/blog/07-the-missing-synchronized-decorator.md
def synchronized(f):
    @functools.wraps(f)
    def _wrapper(self, *args, **kwargs):
        with self.lock:
            return f(self, *args, **kwargs)

    return _wrapper
