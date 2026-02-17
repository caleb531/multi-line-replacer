#!/usr/bin/env python3

import contextlib
import importlib.metadata
import pathlib

import pytest
import tomli
from pytest_mock import MockerFixture

from mlr.__main__ import main


def test_version_matches_pyproject(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
) -> None:
    """
    The printed version should match the version in pyproject.toml
    """
    mocker.patch("sys.argv", ["mlr", "--version"])
    pyproject_data = tomli.loads(pathlib.Path("pyproject.toml").read_text())
    expected_version = pyproject_data["project"]["version"]

    with contextlib.suppress(SystemExit):
        main()

    captured = capsys.readouterr()
    assert expected_version in captured.out


def test_version_fallback(capsys: pytest.CaptureFixture, mocker: MockerFixture) -> None:
    """
    The version should default to 0.0.0 if the package metadata cannot be found
    """
    mocker.patch(
        "importlib.metadata.version",
        side_effect=importlib.metadata.PackageNotFoundError,
    )
    mocker.patch("sys.argv", ["mlr", "--version"])

    with contextlib.suppress(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "0.0.0" in captured.out
