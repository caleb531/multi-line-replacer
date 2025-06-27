## pypa

```yml
- name: Publish distribution to Test PyPI
  uses: pypa/gh-action-pypi-publish@release/MATCH_UNTIL_END_OF_LINE
  with:
    MATCH_UNTIL_END_OF_LINE
    attestations: false

- name: Publish distribution to PyPI
  uses: pypa/gh-action-pypi-publish@release/MATCH_UNTIL_END_OF_LINE
  with:
    MATCH_UNTIL_END_OF_LINE
```

## uv publish

```yml
- name: Publish distribution to Test PyPI
  run: uv publish --publish-url https://test.pypi.org/legacy/

- name: Publish distribution to PyPI
  run: uv publish
```
