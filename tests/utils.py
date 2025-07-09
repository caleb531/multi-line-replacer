#!/usr/bin/env python3

import contextlib
import inspect
import os
import os.path
import shutil
import tempfile
import unittest
from functools import wraps
from io import StringIO
from pathlib import Path
from typing import Any, Callable, Optional, Sequence, Union
from unittest.mock import patch

from mlr.__main__ import main

# The temporary working directory in which the tests can safely perform file
# modifications
temp_dir_path = Path(tempfile.gettempdir()) / "mlr-test-data"
# Subdirectories from anywhere in the project to copy to the temporary working
# directory
subdirs_to_copy = ("tests/input", "tests/output", "tests/rules")


class MLRTestCase(unittest.TestCase):
    """
    A subclass of unittest.TestCase that provides additional behavior and
    assertions specific to the multi-line-replacer package
    """

    # Do not limit size of diffs (makes for easier debugging of failing tests)
    maxDiff = None

    def setUp(self) -> None:
        """
        Before each test, create a temporary directory and copy the relevant
        test fixture files to it
        """
        for subdir_path in subdirs_to_copy:
            subdir_name = os.path.basename(subdir_path)
            temp_subdir_path = temp_dir_path / subdir_name
            with contextlib.suppress(OSError):
                os.makedirs(temp_subdir_path)
                shutil.copytree(subdir_path, temp_subdir_path, dirs_exist_ok=True)

    def tearDown(self) -> None:
        """After each test, remove the temporary test fixture directories"""
        with contextlib.suppress(OSError):
            shutil.rmtree(temp_dir_path)

    def get_fixture_path(self, file_path: Union[str, Path]) -> Path:
        """
        Return a Path object representing the given file path relative to the
        temporary test data directory
        """
        return temp_dir_path / file_path

    def assert_file_replace(
        self,
        input_filenames: Sequence[Union[str, Path]],
        rule_filenames: Sequence[Union[str, Path]],
        output_filenames: Sequence[Union[str, Path]],
        expected_cli_message: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        A custom assertion that runs the CLI program with the specified
        parameters, and optionally checks the summary message from stdout
        """
        out = StringIO()
        with (
            patch(
                "sys.argv",
                [
                    __file__,
                    *(str(self.get_fixture_path(f)) for f in input_filenames),
                    "-r",
                    *(str(self.get_fixture_path(f)) for f in rule_filenames),
                ],
            ),
            contextlib.redirect_stdout(out),
        ):
            main()
            for input_file, output_file in zip(input_filenames, output_filenames):
                self.assertEqual(
                    self.get_fixture_path(output_file).read_text(),
                    self.get_fixture_path(input_file).read_text(),
                )
            if expected_cli_message:
                self.assertEqual(expected_cli_message, out.getvalue().strip())


class use_env(object):
    """
    A decorator (can also be used as a context manager) which sets an
    environment variable for only the lifetime of the given code; this utility
    works seamlessly for both functions and generators
    """

    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value

    def __enter__(self) -> None:
        self.orig_value = os.environ.get(self.key, "")
        os.environ[self.key] = self.value

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        os.environ[self.key] = self.orig_value

    # Derived from: <https://gist.github.com/LeoHuckvale/8f50f8f2a6235512827b>
    # and
    # <https://stackoverflow.com/questions/64622473/can-you-write-a-python-decorator-that-works-for-generator-functions-and-normal-f>
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def function_wrapper(*args: Any, **kwargs: Any) -> Any:
            with self:
                return func(*args, **kwargs)

        @wraps(func)
        def generator_wrapper(*args: Any, **kwargs: Any) -> Any:
            with self:
                return (yield from func(*args, **kwargs))

        if inspect.isgeneratorfunction(func):
            return generator_wrapper
        else:
            return function_wrapper
