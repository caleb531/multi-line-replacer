#!/usr/bin/env python3

from tests.utils import MLRTestCase


class TestMLR(MLRTestCase):
    """Test error cases when running the CLI"""

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
