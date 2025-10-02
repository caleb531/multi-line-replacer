#!/usr/bin/env python3

from tests.utils import MLRTestCase


class TestMLR(MLRTestCase):
    """Test handling of multiple arguments to the CLI"""

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
