#!/usr/bin/env python3

import contextlib
import os
import os.path
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Ensure that assertions within the test utils module are also rewritten to
# provide useful debug information
pytest.register_assert_rewrite("tests.utils")


@pytest.fixture(scope="function", autouse=True)
def setup_test_fixtures() -> Generator[None, None, None]:
    """
    Before all tests, create a temporary directory and copy the relevant
    test fixture files to it. After all tests, remove the temporary directory.
    """
    # The temporary working directory in which the tests can safely perform file
    # modifications
    temp_dir_path = Path(tempfile.gettempdir()) / "mlr-test-data"
    # Subdirectories from anywhere in the project to copy to the temporary
    # working directory
    subdirs_to_copy = ("tests/input", "tests/output", "tests/rules")

    # Setup: copy directories
    for subdir_path in subdirs_to_copy:
        subdir_name = os.path.basename(subdir_path)
        temp_subdir_path = temp_dir_path / subdir_name
        with contextlib.suppress(OSError):
            os.makedirs(temp_subdir_path)
            shutil.copytree(subdir_path, temp_subdir_path, dirs_exist_ok=True)

    yield

    # Teardown: remove temporary directory
    with contextlib.suppress(OSError):
        shutil.rmtree(temp_dir_path)
