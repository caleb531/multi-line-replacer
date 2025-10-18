#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

from rich.console import Console
from rich.text import Style, Text

from mlr.core import extract_code_blocks_from_md_text, replace_text
from mlr.exceptions import CodeBlocksMismatched
from mlr.path import ExpandedPath


def get_cli_args() -> argparse.Namespace:
    """Define and parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_paths",
        metavar="INPUT_FILE",
        nargs="+",
        type=ExpandedPath,
        help="One or more paths to files to apply replacements to.",
    )
    parser.add_argument(
        "-r",
        "--rules",
        metavar="RULE_FILE",
        dest="rule_paths",
        nargs="+",
        required=True,
        type=ExpandedPath,
        help="One or more paths to replacement rule Markdown files. Each file should contain pairs of triple-backtick (```) fenced code blocks, where the first fenced block is the text to be replaced and the second fenced block is the replacement text.",  # noqa: E501
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform all replacements in memory without writing changes to "
        "disk. Useful for testing which files would be changed.",
    )
    return parser.parse_args()


def extract_code_blocks_from_md_path(md_path: Path) -> list[str]:
    """Extract fenced code blocks from a Markdown file at the given path"""
    md_text = md_path.read_text()
    try:
        return extract_code_blocks_from_md_text(md_text)
    except CodeBlocksMismatched:
        print(
            f"{Path(sys.argv[0]).name}: "
            f"{md_path}: "
            f"replacement file must have an even number of fenced code blocks"
        )
        sys.exit(1)


def print_file_statuses(results: List[Tuple[ExpandedPath, bool]]) -> None:
    """Print each processed file path along with whether it changed.

    Output format (no color):
        /abs/path/to/file.yml
        /abs/path/to/other.yml (unchanged)

    Colors (when rich + TTY available):
        changed   -> default
        unchanged -> dim
    """
    # If rich is available and stdout is a terminal, use color; otherwise
    # fall back to plain print
    console = Console()
    for path_obj, changed in results:
        status_text = "changed" if changed else "unchanged"
        if console.is_terminal:
            # Build styled text
            color = Style(color=None) if changed else "dim"
            txt = Text(str(path_obj), style=color)
            if not changed:
                txt.append(f" ({status_text})", style=color)
            console.print(txt)
        elif changed:
            print(f"{path_obj}")
        else:
            print(f"{path_obj} ({status_text})")


def main() -> None:
    """The entry point for the `multi-line-replacer` / `mlr` CLI program"""
    args = get_cli_args()
    results: List[Tuple[ExpandedPath, bool]] = []
    for input_path in args.input_paths:
        orig_input_text = input_path.read_text()
        input_text = orig_input_text
        # Apply each replacement rule to each input file
        for rule_path in args.rule_paths:
            code_blocks = extract_code_blocks_from_md_path(rule_path)
            # Enumerate fenced code blocks in pairs to get each pair of
            # target/replacement rules
            for target_text, replacement_text in zip(
                code_blocks[0::2], code_blocks[1::2]
            ):
                input_text = replace_text(input_text, target_text, replacement_text)
        file_changed = orig_input_text != input_text
        if file_changed and not args.dry_run:
            input_path.write_text(input_text)
        results.append((input_path, file_changed))
    print_file_statuses(results)


if __name__ == "__main__":
    main()
