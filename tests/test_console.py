#!/usr/bin/env python3

from unittest.mock import patch

from rich.text import Text

from tests.utils import assert_file_replace, get_fixture_path


class FakeConsole:
    """
    A fake Console class that simulates a rich.console.Console class in a
    terminal environment for testing purposes.
    """

    is_terminal = True

    def print(self, obj: Text) -> None:
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
