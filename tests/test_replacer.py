#!/usr/bin/env python3

import importlib
from pathlib import WindowsPath
from unittest.mock import patch

from tests.utils import MLRTestCase


class TestMLR(MLRTestCase):
    """Test all multi-line-replacer (mlr) functionality"""

    def test_literal_replacement(self) -> None:
        """Should perform a literal textual replacement"""
        self.assert_file_replace(
            input_filenames=["input/test.editorconfig"],
            rule_filenames=["rules/editorconfig.md"],
            output_filenames=["output/test.editorconfig"],
            expected_cli_message="1 file changed, 0 files unchanged",
        )

    def test_literal_target_misindented(self) -> None:
        """
        Should perform a literal textual replacement even if target text is
        misindented
        """
        self.assert_file_replace(
            input_filenames=["input/test.editorconfig"],
            rule_filenames=["rules/editorconfig-misindented.md"],
            output_filenames=["output/test.editorconfig"],
            expected_cli_message="1 file changed, 0 files unchanged",
        )

    def test_match_until_end_of_line(self) -> None:
        """Should perform a replacement with MATCH_UNTIL_END_OF_LINE"""
        self.assert_file_replace(
            input_filenames=["input/lint.yml"],
            rule_filenames=["rules/ruff.md"],
            output_filenames=["output/lint-ruff.yml"],
            expected_cli_message="1 file changed, 0 files unchanged",
        )

    def test_match_all_between(self) -> None:
        """Should perform a replacement with MATCH_ALL_BETWEEN"""
        self.assert_file_replace(
            input_filenames=["input/lint.yml"],
            rule_filenames=["rules/python-version.md"],
            output_filenames=["output/lint-python-version.yml"],
            expected_cli_message="1 file changed, 0 files unchanged",
        )

    def test_normalize_indent_unit_in_replacement(self) -> None:
        """
        Should normalize indent unit in replacement to match indent unit of
        input text
        """
        self.assert_file_replace(
            input_filenames=["input/lint.yml"],
            rule_filenames=["rules/ruff-tab-indent.md"],
            output_filenames=["output/lint-ruff.yml"],
            expected_cli_message="1 file changed, 0 files unchanged",
        )

    def test_no_match(self) -> None:
        """
        Should leave the file untouched if no matches are found
        """
        self.assert_file_replace(
            input_filenames=["input/publish.yml"],
            rule_filenames=["rules/ruff.md"],
            output_filenames=["input/publish.yml"],
            expected_cli_message="1 file unchanged (no replacements made)",
        )

    def test_missing_code_blocks(self) -> None:
        """
        Should raise a RuntimeError if there are an odd number of code blocks
        """
        with self.assertRaises(RuntimeError):
            self.assert_file_replace(
                input_filenames=["input/publish.yml"],
                rule_filenames=["rules/missing-code-blocks.md"],
                output_filenames=["input/publish.yml"],
            )

    def test_multiple_input_files(self) -> None:
        """
        Should process multiple input files
        """
        self.assert_file_replace(
            input_filenames=["input/lint.yml", "input/tests.yml"],
            rule_filenames=["rules/python-version.md"],
            output_filenames=[
                "output/lint-python-version.yml",
                "output/tests-python-version.yml",
            ],
        )

    def test_multiple_rules(self) -> None:
        """
        Should process multiple rules on all specified input files
        """
        self.assert_file_replace(
            input_filenames=["input/publish.yml"],
            rule_filenames=[
                "rules/uv-build.md",
                "rules/setup-python-single.md",
                "rules/pypa.md",
            ],
            output_filenames=["output/publish.yml"],
        )

    def test_multiple_replacements_per_rule(self) -> None:
        """
        Should process multiple replacements per rule file
        """
        self.assert_file_replace(
            input_filenames=["input/publish.yml"],
            rule_filenames=[
                "rules/uv-all.md",
            ],
            output_filenames=["output/publish.yml"],
        )

    @patch("sys.platform", "win32")
    def test_windows_detection(self) -> None:
        """
        Should detect when the host system is Windows and therefore should use
        Windows-native paths (as opposed to POSIX paths)
        """
        core = importlib.import_module("mlr.core")
        importlib.reload(core)
        self.assertEqual(core.BasePath, WindowsPath)
