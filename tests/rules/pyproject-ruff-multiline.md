## without annotation rules

```toml
[tool.ruff.lint]
select = [
  MATCH_ALL_BETWEEN,
  "PERF",
]
```

## with annotation rules

```toml
[tool.ruff.lint]
select = [
  MATCH_REF_1,
  "PERF",
  "ANN001",
]
```
