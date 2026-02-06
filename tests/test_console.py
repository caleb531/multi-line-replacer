#!/usr/bin/env python3
import contextlib
from typing import Iterator, Union
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

    @contextlib.contextmanager
    def pager(self, styles: bool = True) -> Iterator[None]:
        yield

    def print(self, obj: Union[Text, Syntax, str], **kwargs: object) -> None:
        end = str(kwargs.get("end", "\n"))
        if isinstance(obj, Syntax):
            print(obj.code, end=end)
        elif isinstance(obj, str):
            if kwargs.get("markup") is False:
                print(obj, end=end)
            else:
                print(Text.from_markup(obj).plain, end=end)
        else:
            text = getattr(obj, "plain", str(obj))
            print(text, end=end)


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


def test_show_diff_no_changes() -> None:
    """
    Should not show a diff if no changes were made, even if --show-diff is
    passed.
    """
    input_filename = "input/publish.yml"
    input_path = get_fixture_path(input_filename)

    with patch("mlr.__main__.Console", FakeConsole):
        assert_file_replace(
            show_diff=True,
            dry_run=True,
            input_filenames=[input_filename],
            rule_filenames=["rules/ruff.md"],
            output_filenames=[input_filename],
            expected_cli_message=(
                "Note: Dry run enabled; no files will be modified on disk.\n"
                f"{input_path} (unchanged)"
            ),
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

    # Warning is printed to stdout so it will appear in the captured stdout
    expected_message = (
        "Note: Dry run enabled; no files will be modified on disk.\n"
        f"{text_file} (unchanged)\n"
        f"{binary_file} (skipping binary file)"
    )

    # We expect 'binary.bin' to be skipped (not in results list), so we
    # don't include it in input_filenames (which verifies final content)
    assert_file_replace(
        cli_input_paths=[text_file, binary_file],
        input_filenames=[],
        output_filenames=[],
        rule_filenames=["rules/ruff.md"],
        dry_run=True,
        expected_cli_message=expected_message,
        exact_message_match=False,
    )


@patch("mlr.__main__.Console", FakeConsole)
def test_directory_skip_warning() -> None:
    """
    Should skip directories with a warning.
    """
    directory_path = get_fixture_path("some_dir")
    directory_path.mkdir(parents=True, exist_ok=True)

    assert_file_replace(
        cli_input_paths=[directory_path],
        input_filenames=[],
        output_filenames=[],
        rule_filenames=["rules/ruff.md"],
        dry_run=True,
        expected_cli_message=(
            "Note: Dry run enabled; no files will be modified on disk.\n"
            f"{directory_path} (skipping directory)"
        ),
    )


@patch("mlr.__main__.Console", FakeConsole)
def test_binary_file_skip_quiet() -> None:
    """
    Should skip binary files silently when quiet mode is enabled.
    """
    binary_file_path = get_fixture_path("binary_quiet.bin")
    binary_file_path.write_bytes(b"\x96\x00\x00")

    with patch("sys.stderr") as mock_stderr:
        assert_file_replace(
            cli_input_paths=[binary_file_path],
            input_filenames=[],
            output_filenames=[],
            rule_filenames=["rules/ruff.md"],
            dry_run=True,
            quiet=True,
            expected_cli_message="",
        )
        args_concatenated = "".join(
            call.args[0] for call in mock_stderr.write.call_args_list if call.args
        )
        assert args_concatenated == ""


@patch("mlr.__main__.Console", FakeConsole)
def test_directory_skip_quiet() -> None:
    """
    Should skip directories silently when quiet mode is enabled.
    """
    directory_path = get_fixture_path("some_dir_quiet")
    directory_path.mkdir(parents=True, exist_ok=True)

    with patch("sys.stderr") as mock_stderr:
        assert_file_replace(
            cli_input_paths=[directory_path],
            input_filenames=[],
            output_filenames=[],
            rule_filenames=["rules/ruff.md"],
            dry_run=True,
            quiet=True,
            expected_cli_message="",
        )
        args_concatenated = "".join(
            call.args[0] for call in mock_stderr.write.call_args_list if call.args
        )
        assert args_concatenated == ""
