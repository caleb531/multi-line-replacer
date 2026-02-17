#!/usr/bin/env python3

import importlib
from pathlib import WindowsPath

from pytest_mock import MockerFixture

from tests.utils import assert_file_replace, get_fixture_path


def test_windows_detection(mocker: MockerFixture) -> None:
    """
    Should detect when the host system is Windows and therefore should use
    Windows-native paths (as opposed to POSIX paths)
    """
    mocker.patch("sys.platform", "win32")
    path = importlib.import_module("mlr.path")
    importlib.reload(path)
    assert path.BasePath == WindowsPath


def test_literal_replacement_expansion() -> None:
    """Should perform a literal textual replacement (with ~ expansion)"""
    assert_file_replace(
        input_filenames=["input/test.editorconfig"],
        rule_filenames=["rules/editorconfig.md"],
        output_filenames=["output/test.editorconfig"],
        expected_cli_message=(f"{get_fixture_path('input/test.editorconfig')}"),
    )
