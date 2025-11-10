#!/usr/bin/env python3

from tests.utils import assert_file_replace, get_fixture_path, use_env


def test_match_until_end_of_line() -> None:
    """Should perform a replacement with MATCH_UNTIL_END_OF_LINE"""
    assert_file_replace(
        input_filenames=["input/lint.yml"],
        rule_filenames=["rules/ruff.md"],
        output_filenames=["output/lint-ruff.yml"],
        expected_cli_message=(f"{get_fixture_path('input/lint.yml')}"),
    )


def test_match_all_between() -> None:
    """Should perform a replacement with MATCH_ALL_BETWEEN"""
    assert_file_replace(
        input_filenames=["input/lint.yml"],
        rule_filenames=["rules/python-version.md"],
        output_filenames=["output/lint-python-version.yml"],
        expected_cli_message=(f"{get_fixture_path('input/lint.yml')}"),
    )


@use_env("PROJECT_PKG_NAME", "myproject")
@use_env("PROJECT_BUILD_SYSTEM", "setuptools")
@use_env("PROJECT_BUILD_BACKEND", "setuptools.build_meta")
def test_environment_variables() -> None:
    """
    Should evaluate environment variables in both the target text and
    replacement text
    """
    assert_file_replace(
        input_filenames=["input/pyproject.toml"],
        rule_filenames=["rules/upgrade-build-system.md"],
        output_filenames=["output/pyproject-uv-build.toml"],
    )


@use_env("EXAMPLE_VARIABLE", "example-value")
def test_variables_in_input_text() -> None:
    """Should not evaluate literal variable names within the input text"""
    assert_file_replace(
        input_filenames=["input/environment-variables.txt"],
        rule_filenames=["rules/example-environment-variable.md"],
        output_filenames=["output/environment-variables.txt"],
    )


def test_backreferences() -> None:
    """
    Should capture backreferences in the target text and evaluate them
    correctly in the replacement text
    """
    assert_file_replace(
        input_filenames=["input/pyproject.toml"],
        rule_filenames=["rules/coverage-include.md"],
        output_filenames=["output/pyproject-coverage-include.toml"],
    )
