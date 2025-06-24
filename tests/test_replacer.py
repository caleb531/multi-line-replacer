#!/usr/bin/env python3

from tests import MLRTestCase


class TestMLR(MLRTestCase):
    def test_literal_replacement(self):
        self.assert_file_replace(
            {
                "input_filename": "test.editorconfig",
                "rule_filename": "editorconfig.md",
                "output_filename": "test.editorconfig",
            }
        )
