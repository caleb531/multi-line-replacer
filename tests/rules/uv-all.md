## pip (single python version)

```yml
- name: MATCH_UNTIL_END_OF_LINE
  uses: actions/setup-python@MATCH_UNTIL_END_OF_LINE
  with:
    python-version: "MATCH_ALL_BETWEEN"

- name: MATCH_UNTIL_END_OF_LINE
  run: |
    MATCH_UNTIL_END_OF_LINE
    MATCH_UNTIL_END_OF_LINE
```

# uv (single python version)

```yml
- name: Install uv
  uses: astral-sh/setup-uv@v5
  with:
    python-version: "3.13"

- name: Check lockfile
  run: uv lock --check
```

## pip (python version in a matrix)

```yml
- name: MATCH_UNTIL_END_OF_LINE ${{ matrix.python-version }}
  uses: actions/setup-python@MATCH_UNTIL_END_OF_LINE
  with:
    python-version: ${{ matrix.python-version }}

- name: MATCH_UNTIL_END_OF_LINE
  run: |
    MATCH_UNTIL_END_OF_LINE
    MATCH_UNTIL_END_OF_LINE
```

## uv (python version in a matrix)

```yml
- name: Install uv
  uses: astral-sh/setup-uv@v5
  with:
    python-version: ${{ matrix.python-version }}

- name: Check lockfile
  run: uv lock --check
```

## build

```yml
- name: Install pypa/build
  run: python -m pip MATCH_UNTIL_END_OF_LINE

- name: Build a binary wheel and a source tarball
  run: python -m build MATCH_UNTIL_END_OF_LINE
```

## uv build

```yml
- name: Build a binary wheel and a source tarball
  run: uv build --sdist --wheel --out-dir dist/
```

## pypa

```yml
- name: Publish distribution to Test PyPI
  uses: pypa/gh-action-pypi-publish@release/MATCH_UNTIL_END_OF_LINE
  with:
    MATCH_UNTIL_END_OF_LINE
    attestations: false

- name: Publish distribution to PyPI
  uses: pypa/gh-action-pypi-publish@release/MATCH_UNTIL_END_OF_LINE
  with:
    MATCH_UNTIL_END_OF_LINE
```

## uv publish

```yml
- name: Publish distribution to Test PyPI
  run: uv publish --publish-url https://test.pypi.org/legacy/

- name: Publish distribution to PyPI
  run: uv publish
```

## coverage

```yml
- name: MATCH_UNTIL_END_OF_LINE
  run: |
    coverage run MATCH_UNTIL_END_OF_LINE
    coverage lcov MATCH_UNTIL_END_OF_LINE
```

## uv run coverage

```yml
- name: Test with nose2
  run: |
    uv run coverage run -m nose2
    uv run coverage lcov -o cover/coverage.lcov
```

## mypy

```yml
- name: Run mypy
  run: mypy MATCH_UNTIL_END_OF_LINE
```

## uv run mypy

```yml
- name: Run mypy
  run: uv run mypy .
```
