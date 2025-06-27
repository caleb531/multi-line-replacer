#!/usr/bin/env python3

import contextlib
import os
import os.path
import shutil
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from mlr.__main__ import main

# The temporary working directory in which the tests can safely perform file
# modifications
temp_dir_path = Path(tempfile.gettempdir()) / "mlr-test-data"
# Subdirectories from anywhere in the project to copy to the temporary working
# directory
subdirs_to_copy = ("tests/input", "tests/output", "tests/rules")


class MLRTestCase(unittest.TestCase):
    # Do not limit size of diffs (makes for easier debugging of failing tests)
    maxDiff = None

    # Before each test, create a temporary directory and copy the relevant test
    # fixture files to it
    def setUp(self):
        for subdir_path in subdirs_to_copy:
            subdir_name = os.path.basename(subdir_path)
            temp_subdir_path = temp_dir_path / subdir_name
            with contextlib.suppress(OSError):
                os.makedirs(temp_subdir_path)
                shutil.copytree(subdir_path, temp_subdir_path, dirs_exist_ok=True)

    # After each test, remove the temporary test fixture directories
    def tearDown(self):
        with contextlib.suppress(OSError):
            shutil.rmtree(temp_dir_path)

    def get_fixture_path(self, subpath):
        return temp_dir_path / subpath

    def assert_file_replace(
        self,
        input_filenames,
        rule_filenames,
        output_filenames,
        expected_cli_message=None,
    ):
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
