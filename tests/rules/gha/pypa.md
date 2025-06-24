## pypa

```yml
- name: Publish distribution to Test PyPI
  uses: pypa/gh-action-pypi-publish@release/MATCH_ALL_BUT_NEWLINE
  with:
    MATCH_ALL_BUT_NEWLINE
    attestations: false

- name: Publish distribution to PyPI
  uses: pypa/gh-action-pypi-publish@release/MATCH_ALL_BUT_NEWLINE
  with:
    MATCH_ALL_BUT_NEWLINE
```

## uv publish

```yml
- name: Publish distribution to Test PyPI
  run: uv publish --publish-url https://test.pypi.org/legacy/

- name: Publish distribution to PyPI
  run: uv publish
```
