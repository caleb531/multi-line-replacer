You can specify as many replacements as you want within the same file, as long
as there are an even number of code blocks altogether. The code blocks are read
in pairs, so the first code block represents the target text to match, the
second code block represents the text to replace, and so on.

As mentioned, only the code blocks are read by the tool; all headings and other
Markdown content is ignored.

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
