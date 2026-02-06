#!/usr/bin/env python3

import contextlib
import importlib.metadata
import pathlib
from unittest.mock import MagicMock, patch

import pytest
import tomli

from mlr.__main__ import main


@patch("sys.argv", ["mlr", "--version"])
def test_version_matches_pyproject(capsys: pytest.CaptureFixture) -> None:
    """
    The printed version should match the version in pyproject.toml
    """
    pyproject_data = tomli.loads(pathlib.Path("pyproject.toml").read_text())
    expected_version = pyproject_data["project"]["version"]

    with contextlib.suppress(SystemExit):
        main()

    captured = capsys.readouterr()
    assert expected_version in captured.out


@patch(
    "importlib.metadata.version",
    side_effect=importlib.metadata.PackageNotFoundError,
)
@patch("sys.argv", ["mlr", "--version"])
def test_version_fallback(version: MagicMock, capsys: pytest.CaptureFixture) -> None:
    """
    The version should default to 0.0.0 if the package metadata cannot be found
    """
    with contextlib.suppress(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "0.0.0" in captured.out
