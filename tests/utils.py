#!/usr/bin/env python3

import contextlib
import inspect
import os
import os.path
import tempfile
from functools import wraps
from io import StringIO
from pathlib import Path
from typing import Any, Callable, Optional, Sequence, Union
from unittest.mock import patch

from mlr.__main__ import main
from mlr.path import read_text

# The temporary working directory in which the tests can safely perform file
# modifications
temp_dir_path = Path(tempfile.gettempdir()) / "mlr-test-data"
# Subdirectories from anywhere in the project to copy to the temporary
# working directory
subdirs_to_copy = ("tests/input", "tests/output", "tests/rules")

# Do not limit size of diffs (makes for easier debugging of failing tests)
maxDiff: Optional[int] = None


def get_project_path(file_path: Union[str, Path]) -> Path:
    """
    Return a Path object representing the given file path relative to the
    project directory
    """
    return Path("tests", file_path)


def get_fixture_path(file_path: Union[str, Path]) -> Path:
    """
    Return a Path object representing the given file path relative to the
    temporary test data directory
    """
    return temp_dir_path / file_path


def assert_file_replace(
    input_filenames: Sequence[Union[str, Path]],
    rule_filenames: Sequence[Union[str, Path]],
    output_filenames: Sequence[Union[str, Path]],
    expected_cli_message: Optional[Union[str, Path]] = None,
    dry_run: bool = False,
    show_diff: bool = False,
    quiet: bool = False,
    cli_input_paths: Optional[Sequence[Union[str, Path]]] = None,
    exact_message_match: bool = True,
) -> None:
    """
    A custom assertion that runs the CLI program with the specified
    parameters, and optionally checks the summary message from stdout
    """
    out = StringIO()
    # If explicit CLI input paths are provided, use those for sys.argv;
    # otherwise, default to the input filenames used for verification
    if cli_input_paths is None:
        cli_input_paths = input_filenames

    with (
        patch(
            "sys.argv",
            [
                __file__,
                *(["--dry-run"] if dry_run else []),
                *(["--show-diff"] if show_diff else []),
                *(["--quiet"] if quiet else []),
                *(str(get_fixture_path(f)) for f in cli_input_paths),
                *[
                    arg
                    for rule_filename in rule_filenames
                    for arg in ("-r", str(get_fixture_path(rule_filename)))
                ],
            ],
        ),
        contextlib.redirect_stdout(out),
    ):
        main()
        for input_file, output_file in zip(input_filenames, output_filenames):
            input_path = get_fixture_path(input_file)
            # For some tests, the expectation is that no file modifications
            # are made, so the output path is set to be the same as the
            # input path; however, in order for this to work, the output
            # file must be sourced from the project directory rather than
            # the temporary fixture directory; otherwise, the input/output
            # paths would be equal and the assertion would always pass in
            # this circumstance
            output_path = get_project_path(output_file)
            assert output_path != input_path
            assert (
                # Compare raw text (including line endings) to ensure there
                # is an exact match between the modified input file and the
                # expected output
                read_text(output_path, newline="") == read_text(input_path, newline="")
            )
        if expected_cli_message is not None:
            if exact_message_match:
                assert str(expected_cli_message) == out.getvalue().strip()
            else:
                assert str(expected_cli_message) in out.getvalue().strip()


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
