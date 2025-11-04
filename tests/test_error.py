#!/usr/bin/env python3

import pytest

from tests.utils import assert_file_replace


def test_empty_target_code_block() -> None:
    """
    Should print an error and exit program if the target text code block is
    empty
    """
    with pytest.raises(SystemExit):
        assert_file_replace(
            input_filenames=["input/publish.yml"],
            rule_filenames=["rules/empty-target-text.md"],
            output_filenames=["input/publish.yml"],
        )


def test_missing_code_blocks() -> None:
    """
    Should print an error exit program if there are an odd number of code
    blocks
    """
    with pytest.raises(SystemExit):
        assert_file_replace(
            input_filenames=["input/publish.yml"],
            rule_filenames=["rules/missing-code-blocks.md"],
            output_filenames=["input/publish.yml"],
        )
