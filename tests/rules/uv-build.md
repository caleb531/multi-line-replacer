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
