#!/usr/bin/env python3

#!/usr/bin/env python3
# coding=utf-8

import contextlib
import os
import os.path
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mlr.__main__ import main

# The temporary working directory in which the tests can safely perform file
# modifications
temp_dir_path = os.path.join(tempfile.gettempdir(), "mlr-test-data")
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
            temp_subdir_path = os.path.join(temp_dir_path, subdir_name)
            with contextlib.suppress(OSError):
                os.makedirs(temp_subdir_path)
                shutil.copytree(subdir_path, temp_subdir_path, dirs_exist_ok=True)

    # After each test, remove the temporary test fixture directories
    def tearDown(self):
        with contextlib.suppress(OSError):
            shutil.rmtree(temp_dir_path)

    def get_input_path(self, input_filename):
        return os.path.join(temp_dir_path, "input", input_filename)

    def get_rule_path(self, input_filename):
        return os.path.join(temp_dir_path, "rules", input_filename)

    def get_output_path(self, input_filename):
        return os.path.join(temp_dir_path, "output", input_filename)

    def assert_file_replace(self, *operations):
        with patch(
            "sys.argv",
            [
                __file__,
                *(
                    self.get_input_path(operation["input_filename"])
                    for operation in operations
                ),
                "-r",
                *(
                    self.get_rule_path(operation["rule_filename"])
                    for operation in operations
                ),
            ],
        ):
            main()
            for operation in operations:
                self.assertEqual(
                    Path(
                        self.get_output_path(operation["output_filename"])
                    ).read_text(),
                    Path(self.get_input_path(operation["input_filename"])).read_text(),
                )
