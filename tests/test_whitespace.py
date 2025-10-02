#!/usr/bin/env python3

from tests.utils import MLRTestCase


class TestMLR(MLRTestCase):
    """Test all multi-line-replacer (mlr) functionality"""

    def test_normalize_indent_unit_in_replacement(self) -> None:
        """
        Should normalize indent unit in replacement to match indent unit of
        input text
        """
        self.assert_file_replace(
            input_filenames=["input/lint.yml"],
            rule_filenames=["rules/ruff-tab-indent.md"],
            output_filenames=["output/lint-ruff.yml"],
            expected_cli_message=(f"{self.get_fixture_path('input/lint.yml')}"),
        )

    def test_empty_code_block(self) -> None:
        """
        Should remove lines by specifying an empty string as the replacement
        text in the rule file
        """
        self.assert_file_replace(
            input_filenames=["input/tests.yml"],
            rule_filenames=["rules/remove-lines.md"],
            output_filenames=["output/tests-remove-lines.yml"],
        )

    def test_replace_blank_line(self) -> None:
        """
        Should replace lines with a blank line by specifying a blank line as the
        replacement text in the rule file
        """
        self.assert_file_replace(
            input_filenames=["input/tests.yml"],
            rule_filenames=["rules/replace-with-blank-line.md"],
            output_filenames=["output/tests-replace-with-blank-line.yml"],
        )
