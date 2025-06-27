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

## uv

```yml
- name: Install uv
  uses: astral-sh/setup-uv@v5
  with:
    python-version: ${{ matrix.python-version }}

- name: Check lockfile
  run: uv lock --check
```
