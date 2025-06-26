#!/usr/bin/env python3

from tests import MLRTestCase


class TestMLR(MLRTestCase):
    def test_literal_replacement(self):
        """Should perform a literal textual replacement"""
        self.assert_file_replace(
            input_filenames=["test.editorconfig"],
            rule_filenames=["editorconfig.md"],
            output_filenames=["test.editorconfig"],
        )

    def test_literal_target_misindented(self):
        """
        Should perform a literal textual replacement even if target text is
        misindented
        """
        self.assert_file_replace(
            input_filenames=["test.editorconfig"],
            rule_filenames=["editorconfig-misindented.md"],
            output_filenames=["test.editorconfig"],
        )

    def test_match_until_end_of_line(self):
        """Should perform a replacement with MATCH_UNTIL_END_OF_LINE"""
        self.assert_file_replace(
            input_filenames=["lint.yml"],
            rule_filenames=["gha/ruff.md"],
            output_filenames=["lint-ruff.yml"],
        )

    def test_match_all_between(self):
        """Should perform a replacement with MATCH_ALL_BETWEEN"""
        self.assert_file_replace(
            input_filenames=["lint.yml"],
            rule_filenames=["gha/python-version.md"],
            output_filenames=["lint-python-version.yml"],
        )

    def test_normalize_indent_unit_in_replacement(self):
        """
        Should normalize indent unit in replacement to match indent unit of
        input text
        """
        self.assert_file_replace(
            input_filenames=["lint.yml"],
            rule_filenames=["gha/ruff-tab-indent.md"],
            output_filenames=["lint-ruff.yml"],
        )
