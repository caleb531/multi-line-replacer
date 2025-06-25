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

    def test_match_all_but_newline(self):
        """should perform a replacement with MATCH_ALL_BUT_NEWLINE"""
        self.assert_file_replace(
            input_filenames=["lint.yml"],
            rule_filenames=["gha/ruff.md"],
            output_filenames=["lint-ruff.yml"],
        )

    def test_match_all_but_newline_lazy(self):
        """should perform a replacement with MATCH_ALL_BUT_NEWLINE_LAZY"""
        self.assert_file_replace(
            input_filenames=["lint.yml"],
            rule_filenames=["gha/python-version.md"],
            output_filenames=["lint-python-version.yml"],
        )
