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

## uv

```yml
- name: Install uv
  uses: astral-sh/setup-uv@v5
  with:
    python-version: "3.13"

- name: Check lockfile
  run: uv lock --check
```
