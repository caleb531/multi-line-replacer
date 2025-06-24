## pip (single python version)

```yml
- name: MATCH_ALL_BUT_NEWLINE
  uses: actions/setup-python@MATCH_ALL_BUT_NEWLINE
  with:
    python-version: "MATCH_ALL_BUT_NEWLINE_LAZY"

- name: MATCH_ALL_BUT_NEWLINE
  run: |
    MATCH_ALL_BUT_NEWLINE
    MATCH_ALL_BUT_NEWLINE
```

## uv

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
- name: MATCH_ALL_BUT_NEWLINE ${{ matrix.python-version }}
  uses: actions/setup-python@MATCH_ALL_BUT_NEWLINE
  with:
    python-version: ${{ matrix.python-version }}

- name: MATCH_ALL_BUT_NEWLINE
  run: |
    MATCH_ALL_BUT_NEWLINE
    MATCH_ALL_BUT_NEWLINE
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
