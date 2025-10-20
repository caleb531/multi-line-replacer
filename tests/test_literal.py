#!/usr/bin/env python3

from tests.utils import MLRTestCase


class TestMLR(MLRTestCase):
    """Test literal string replacements without any variables"""

    def test_literal_replacement(self) -> None:
        """Should perform a literal textual replacement"""
        self.assert_file_replace(
            input_filenames=["input/test.editorconfig"],
            rule_filenames=["rules/editorconfig.md"],
            output_filenames=["output/test.editorconfig"],
            expected_cli_message=(
                f"{self.get_fixture_path('input/test.editorconfig')}"
            ),
        )

    def test_literal_target_misindented(self) -> None:
        """
        Should perform a literal textual replacement even if target text is
        misindented
        """
        self.assert_file_replace(
            input_filenames=["input/test.editorconfig"],
            rule_filenames=["rules/editorconfig-misindented.md"],
            output_filenames=["output/test.editorconfig"],
            expected_cli_message=(
                f"{self.get_fixture_path('input/test.editorconfig')}"
            ),
        )

    def test_crlf_files(self) -> None:
        """
        Should perform replacements correctly for files with CRLF line endings
        """
        self.assert_file_replace(
            input_filenames=["input/test.crlf.editorconfig"],
            rule_filenames=["rules/editorconfig.md"],
            output_filenames=["output/test.crlf.editorconfig"],
            expected_cli_message=(
                f"{self.get_fixture_path('input/test.crlf.editorconfig')}"
            ),
        )

    def test_no_trailing(self) -> None:
        """
        Should perform replacements correctly for files without trailing
        newlines
        """
        self.assert_file_replace(
            input_filenames=["input/foo-bar.no-trailing.txt"],
            rule_filenames=["rules/foo-bar.md"],
            output_filenames=["output/foo-bar.no-trailing.txt"],
            expected_cli_message=(
                f"{self.get_fixture_path('input/foo-bar.no-trailing.txt')}"
            ),
        )

    def test_tilde_code_fences(self) -> None:
        """
        Should handle code blocks fenced by tildes (~) instead of backticks (`)
        """
        self.assert_file_replace(
            input_filenames=["input/test.editorconfig"],
            rule_filenames=["rules/editorconfig-tildes.md"],
            output_filenames=["output/test.editorconfig"],
            expected_cli_message=(
                f"{self.get_fixture_path('input/test.editorconfig')}"
            ),
        )

    def test_no_match(self) -> None:
        """
        Should leave the file untouched if no matches are found
        """
        self.assert_file_replace(
            input_filenames=["input/test.editorconfig"],
            rule_filenames=["rules/python-version.md"],
            output_filenames=["input/test.editorconfig"],
            expected_cli_message=(
                f"{self.get_fixture_path('input/test.editorconfig')} (unchanged)"
            ),
        )
