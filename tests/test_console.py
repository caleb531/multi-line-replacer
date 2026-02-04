#!/usr/bin/env python3
from typing import Union
from unittest.mock import patch

from rich.syntax import Syntax
from rich.text import Text

from tests.utils import assert_file_replace, get_fixture_path


class FakeConsole:
    """
    A fake Console class that simulates a rich.console.Console class in a
    terminal environment for testing purposes.
    """

    is_terminal = True

    def print(self, obj: Union[Text, Syntax, str]) -> None:
        if isinstance(obj, Syntax):
            print(obj.code)
        elif isinstance(obj, str):
            print(Text.from_markup(obj).plain)
        else:
            text = getattr(obj, "plain", str(obj))
            print(text)


def test_mixed_changed_and_unchanged_non_terminal() -> None:
    """
    Should output both changed and unchanged files (non-terminal screens).
    """
    changed_path = get_fixture_path("input/lint.yml")
    unchanged_path = get_fixture_path("input/publish.yml")
    assert_file_replace(
        input_filenames=["input/lint.yml", "input/publish.yml"],
        rule_filenames=["rules/ruff.md"],
        output_filenames=["output/lint-ruff.yml", "input/publish.yml"],
        expected_cli_message=f"{changed_path}\n{unchanged_path} (unchanged)",
    )


@patch("mlr.__main__.Console", FakeConsole)
def test_mixed_changed_and_unchanged_terminal() -> None:
    """Should output both changed and unchanged files within a terminal."""
    changed_path = get_fixture_path("input/lint.yml")
    unchanged_path = get_fixture_path("input/publish.yml")
    assert_file_replace(
        input_filenames=["input/lint.yml", "input/publish.yml"],
        rule_filenames=["rules/ruff.md"],
        output_filenames=["output/lint-ruff.yml", "input/publish.yml"],
        expected_cli_message=f"{changed_path}\n{unchanged_path} (unchanged)",
    )


def test_dry_run() -> None:
    """
    Should not write changes to disk when --dry-run is specified
    """
    assert_file_replace(
        dry_run=True,
        input_filenames=["input/test.editorconfig"],
        rule_filenames=["rules/editorconfig.md"],
        output_filenames=["input/test.editorconfig"],
        expected_cli_message=(
            "Note: Dry run enabled; no files will be modified on disk.\n"
            + f"{get_fixture_path('input/test.editorconfig')}"
        ),
    )


def test_quiet_mode() -> None:
    """Should not output anything when --quiet/-q is passed."""
    assert_file_replace(
        quiet=True,
        input_filenames=["input/lint.yml", "input/publish.yml"],
        rule_filenames=["rules/ruff.md"],
        output_filenames=["output/lint-ruff.yml", "input/publish.yml"],
        expected_cli_message="",
    )


def test_quiet_mode_dry_run() -> None:
    """
    Should still not output anything when dry run mode and quiet mode are
    enabled.
    """
    assert_file_replace(
        quiet=True,
        dry_run=True,
        input_filenames=["input/lint.yml", "input/publish.yml"],
        rule_filenames=["rules/ruff.md"],
        output_filenames=["input/lint.yml", "input/publish.yml"],
        expected_cli_message="",
    )


def test_show_diff() -> None:
    """
    Should show a unified diff of changes when --show-diff is passed.
    """
    input_filename = "input/lint.yml"
    input_path = get_fixture_path(input_filename)

    # Just check that the output contains the diff header
    with patch("mlr.__main__.Console", FakeConsole):
        assert_file_replace(
            show_diff=True,
            dry_run=True,
            input_filenames=[input_filename],
            rule_filenames=["rules/ruff.md"],
            output_filenames=[input_filename],
            expected_cli_message=f"--- {input_path}",
            exact_message_match=False,
        )


@patch("mlr.__main__.Console", FakeConsole)
def test_binary_file_skip() -> None:
    """
    Should gracefully skip binary files with a warning.
    """
    # Create a binary file
    binary_file = get_fixture_path("binary.bin")
    binary_file.write_bytes(b"\x96\x00\x00")

    # Create a valid text file to ensure others are still processed
    text_file = get_fixture_path("text.txt")
    text_file.write_text("some text")

    # Warning is printed to stderr, so it won't appear in the captured stdout
    # checked by expected_cli_message unless we captured stderr too.
    # checking assert_file_replace implementation: contextlib.redirect_stdout(out).
    # It does NOT redirect stderr.
    # However, print_file_statuses prints to stdout.

    expected_message = (
        "Note: Dry run enabled; no files will be modified on disk.\n"
        f"{text_file} (unchanged)"
    )

    with patch("sys.stderr") as mock_stderr:
        # We expect 'binary.bin' to be skipped (not in results list), so we
        # don't include it in input_filenames (which verifies final content)
        # properly speaking, if we passed it in input_filenames, the
        # assert_file_replace loop would try to read it.
        assert_file_replace(
            cli_input_paths=[text_file, binary_file],
            input_filenames=[],
            output_filenames=[],
            rule_filenames=["rules/ruff.md"],
            dry_run=True,
            expected_cli_message=expected_message,
        )
        # Parse out stderr calls to verify binary file warning
        args_concatenated = "".join(
            call.args[0] for call in mock_stderr.write.call_args_list if call.args
        )
        assert "Skipping" in args_concatenated
        assert str(binary_file) in args_concatenated
