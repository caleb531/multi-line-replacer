#!/usr/bin/env python3

from unittest.mock import patch

from rich.text import Text

from tests.utils import MLRTestCase


class FakeConsole:
    """
    A fake Console class that simulates a rich.console.Console class in a
    terminal environment for testing purposes.
    """

    is_terminal = True

    def print(self, obj: Text) -> None:
        text = getattr(obj, "plain", str(obj))
        print(text)


class TestConsoleOutput(MLRTestCase):
    """Tests specific to console/terminal presentation logic."""

    def test_mixed_changed_and_unchanged_non_terminal(self) -> None:
        """
        Should output both changed and unchanged files (non-terminal screens).
        """
        changed_path = self.get_fixture_path("input/lint.yml")
        unchanged_path = self.get_fixture_path("input/publish.yml")
        self.assert_file_replace(
            input_filenames=["input/lint.yml", "input/publish.yml"],
            rule_filenames=["rules/ruff.md"],
            output_filenames=["output/lint-ruff.yml", "input/publish.yml"],
            expected_cli_message=f"{changed_path}\n{unchanged_path} (unchanged)",
        )

    @patch("mlr.__main__.Console", FakeConsole)
    def test_mixed_changed_and_unchanged_terminal(self) -> None:
        """Should output both changed and unchanged files within a terminal."""
        changed_path = self.get_fixture_path("input/lint.yml")
        unchanged_path = self.get_fixture_path("input/publish.yml")
        self.assert_file_replace(
            input_filenames=["input/lint.yml", "input/publish.yml"],
            rule_filenames=["rules/ruff.md"],
            output_filenames=["output/lint-ruff.yml", "input/publish.yml"],
            expected_cli_message=f"{changed_path}\n{unchanged_path} (unchanged)",
        )

    def test_dry_run(self) -> None:
        """
        Should not write changes to disk when --dry-run is specified
        """
        self.assert_file_replace(
            dry_run=True,
            input_filenames=["input/test.editorconfig"],
            rule_filenames=["rules/editorconfig.md"],
            output_filenames=["input/test.editorconfig"],
            expected_cli_message=(
                "Note: Dry run enabled; no files will be modified on disk.\n"
                + f"{self.get_fixture_path('input/test.editorconfig')}"
            ),
        )

    @patch("mlr.__main__.Console", FakeConsole)
    def test_quiet_mode(self) -> None:
        """Should output both changed and unchanged files within a terminal."""
        self.assert_file_replace(
            quiet=True,
            input_filenames=["input/lint.yml", "input/publish.yml"],
            rule_filenames=["rules/ruff.md"],
            output_filenames=["output/lint-ruff.yml", "input/publish.yml"],
            expected_cli_message="",
        )
