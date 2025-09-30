# Backreferences Example

This rule demonstrates capturing three semantically distinct values with
`MATCH_ALL_BETWEEN` and then reusing (and duplicating) them in the replacement
via backreferences.

## CI environment variables as code

```yml
run: |
  export PROJECT_NAME=MATCH_ALL_BETWEEN
  export PY_VERSION=MATCH_ALL_BETWEEN
  export CACHE_KEY=MATCH_ALL_BETWEEN
  echo "Using ${PROJECT_NAME} on Python ${PY_VERSION} (cache: ${CACHE_KEY})"
```

## CI environment variables as configuration

```yml
env:
  PROJECT_NAME: MATCH_REF_1
  PY_VERSION: MATCH_REF_2
  CACHE_KEY: MATCH_REF_3
run: |
  echo "Using ${PROJECT_NAME} on Python ${PY_VERSION} (cache: ${CACHE_KEY})"
```
