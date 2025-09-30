#!/usr/bin/env python3


import importlib
import os
import os.path
from pathlib import Path, WindowsPath
from unittest.mock import patch

from tests.utils import MLRTestCase


class TestMLRPathExpansion(MLRTestCase):
    """
    Test expanding ~ to the user's home directory within paths supplied to MLR
    """

    temp_dir_path = Path(os.path.expanduser("~")) / ".cache" / "mlr-test-data"

    @patch("sys.platform", "win32")
    def test_windows_detection(self) -> None:
        """
        Should detect when the host system is Windows and therefore should use
        Windows-native paths (as opposed to POSIX paths)
        """
        path = importlib.import_module("mlr.path")
        importlib.reload(path)
        self.assertEqual(path.BasePath, WindowsPath)

    def test_literal_replacement_expansion(self) -> None:
        """Should perform a literal textual replacement (with ~ expansion)"""
        self.assert_file_replace(
            input_filenames=["input/test.editorconfig"],
            rule_filenames=["rules/editorconfig.md"],
            output_filenames=["output/test.editorconfig"],
            expected_cli_message=(
                f"{self.get_fixture_path('input/test.editorconfig')}"
            ),
        )
