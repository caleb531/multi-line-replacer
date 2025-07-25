#!/usr/bin/env python3.13
import os
import sys
from pathlib import PosixPath, WindowsPath

# Detect proper Path subclass to inherit from based on the user's platform,
# since the top-level Path subclass is not designed to be subclassed directly
if sys.platform == "win32":
    BasePath = WindowsPath
else:
    BasePath = PosixPath


class ExpandedPath(BasePath):
    """
    Path subclass that automatically expands the user's home directory (i.e. ~)
    """

    def __new__(cls, path: str, **kwargs: object) -> "ExpandedPath":
        return super().__new__(cls, os.path.expanduser(path), **kwargs)
