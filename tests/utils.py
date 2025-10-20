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


class MLRTestCase(unittest.TestCase):
    """
    A subclass of unittest.TestCase that provides additional behavior and
    assertions specific to the multi-line-replacer package
    """

    # The temporary working directory in which the tests can safely perform file
    # modifications
    temp_dir_path = Path(tempfile.gettempdir()) / "mlr-test-data"
    # Subdirectories from anywhere in the project to copy to the temporary
    # working directory
    subdirs_to_copy = ("tests/input", "tests/output", "tests/rules")

    # Do not limit size of diffs (makes for easier debugging of failing tests)
    maxDiff = None

    def setUp(self) -> None:
        """
        Before each test, create a temporary directory and copy the relevant
        test fixture files to it
        """
        for subdir_path in self.subdirs_to_copy:
            subdir_name = os.path.basename(subdir_path)
            temp_subdir_path = self.temp_dir_path / subdir_name
            with contextlib.suppress(OSError):
                os.makedirs(temp_subdir_path)
                shutil.copytree(subdir_path, temp_subdir_path, dirs_exist_ok=True)

    def tearDown(self) -> None:
        """After each test, remove the temporary test fixture directories"""
        with contextlib.suppress(OSError):
            shutil.rmtree(self.temp_dir_path)

    def get_project_path(self, file_path: Union[str, Path]) -> Path:
        """
        Return a Path object representing the given file path relative to the
        project directory
        """
        return Path("tests", file_path)

    def get_fixture_path(self, file_path: Union[str, Path]) -> Path:
        """
        Return a Path object representing the given file path relative to the
        temporary test data directory
        """
        return self.temp_dir_path / file_path

    def assert_file_replace(
        self,
        input_filenames: Sequence[Union[str, Path]],
        rule_filenames: Sequence[Union[str, Path]],
        output_filenames: Sequence[Union[str, Path]],
        expected_cli_message: Optional[Union[str, Path]] = None,
        dry_run: bool = False,
        quiet: bool = False,
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
                    *(["--dry-run"] if dry_run else []),
                    *(["--quiet"] if quiet else []),
                    *(str(self.get_fixture_path(f)) for f in input_filenames),
                    "-r",
                    *(str(self.get_fixture_path(f)) for f in rule_filenames),
                ],
            ),
            contextlib.redirect_stdout(out),
        ):
            main()
            for input_file, output_file in zip(input_filenames, output_filenames):
                input_path = self.get_fixture_path(input_file)
                # For some tests, the expectation is that no file modifications
                # are made, so the output path is set to be the same as the
                # input path; however, in order for this to work, the output
                # file must be sourced from the project directory rather than
                # the temporary fixture directory; otherwise, the input/output
                # paths could be equal and the assertion would always pass in
                # this circumstance
                output_path = self.get_project_path(output_file)
                self.assertNotEqual(output_path, input_path)
                self.assertEqual(
                    # Compare raw text (including line endings) to ensure there
                    # is an exact match between the modified input file and the
                    # expected output
                    output_path.read_text(newline=""),
                    input_path.read_text(newline=""),
                )
            if expected_cli_message is not None:
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
