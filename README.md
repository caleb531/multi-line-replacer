# Multi-Line Replacer (`mlr`)

*Copyright 2025 Caleb Evans*  
*Released under the MIT license*

[![tests](https://github.com/caleb531/multi-line-replacer/actions/workflows/tests.yml/badge.svg)](https://github.com/caleb531/multi-line-replacer/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/caleb531/multi-line-replacer/badge.svg?branch=main)](https://coveralls.io/r/caleb531/multi-line-replacer?branch=main)

Multi-Line Replacer is a CLI utility for replacing multi-line hunks of strings
across one or more files. Matc\hing is mostly textual, but wildcard matching is
supported, and replacements are indentation-aware.

## Usage

The workflow takes one or more files on which to run replacements, and then a
series of "replacement rule" files with the `-r` flag:

```sh
mlr .github/workflows/*.yml -r my-replacement-rule.md
```

Each replacement rule must be a Markdown file with one or more pairs of GFM
fenced code blocks ([see documentation][gfm-docs]). Every odd code block
represents the target text to replace, and every even code block represents the
textual replacement. Please see 

[gfm-docs]: https://github.github.com/gfm/#fenced-code-blocks

### Example

The following example makes a series of replacements to a series of GitHub Action workflows written in YAML.

```sh
mlr .github/workflows/*.yml -r 
```
