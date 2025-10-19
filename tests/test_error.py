#!/usr/bin/env python3

from tests.utils import MLRTestCase


class TestMLR(MLRTestCase):
    """Test error cases when running the CLI"""

    def test_empty_target_code_block(self) -> None:
        """
        Should print an error and exit program if the target text code block is
        empty
        """
        with self.assertRaises(SystemExit):
            self.assert_file_replace(
                input_filenames=["input/publish.yml"],
                rule_filenames=["rules/empty-target-text.md"],
                output_filenames=["input/publish.yml"],
            )

    def test_missing_code_blocks(self) -> None:
        """
        Should print an error exit program if there are an odd number of code
        blocks
        """
        with self.assertRaises(SystemExit):
            self.assert_file_replace(
                input_filenames=["input/publish.yml"],
                rule_filenames=["rules/missing-code-blocks.md"],
                output_filenames=["input/publish.yml"],
            )
