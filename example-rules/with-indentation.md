A major benefit of MLR is that it automatically indents the replacement text
according to the auto-detected starting indentation of the matched text in the
input file. This has two main implications:

1. No indentation is required for the starting line of the target text (unless
   subsequent lines need to decrease in indentation)
2. When running MLR, the indentation style of your target/replacement text will
   be normalized to match the indentation style of the input file (e.g.
   converting tabs to 2-space indent)

## flake8

```yml
- name: Run flake8
  run: flake8 MATCH_UNTIL_END_OF_LINE
```

## ruff

```yml
- name: Run ruff
  run: |
    uv run ruff check .
    uv run ruff format --check .
```
