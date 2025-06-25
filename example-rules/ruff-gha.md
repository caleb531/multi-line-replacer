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
