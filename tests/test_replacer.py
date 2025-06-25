#!/usr/bin/env python3

from tests import MLRTestCase


class TestMLR(MLRTestCase):
    def test_literal_replacement(self):
        """Should perform a literal textual replacement"""
        self.assert_file_replace(
            {
                "input_filename": "test.editorconfig",
                "rule_filename": "editorconfig.md",
                "output_filename": "test.editorconfig",
            }
        )

    def test_match_all_but_newline(self):
        """should perform a replacement with MATCH_ALL_BUT_NEWLINE"""
        self.assert_file_replace(
            {
                "input_filename": "lint.yml",
                "rule_filename": "gha/ruff.md",
                "output_filename": "lint-ruff.yml",
            }
        )

    def test_match_all_but_newline_lazy(self):
        """should perform a replacement with MATCH_ALL_BUT_NEWLINE_LAZY"""
        self.assert_file_replace(
            {
                "input_filename": "lint.yml",
                "rule_filename": "gha/python-version.md",
                "output_filename": "lint-python-version.yml",
            }
        )
