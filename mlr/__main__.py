#!/usr/bin/env python3

import argparse
import contextlib
import difflib
import importlib.metadata
import sys
from pathlib import Path

from rich.console import Console
from rich.syntax import Syntax
from rich.text import Style, Text

from mlr.core import extract_code_blocks_from_md_text, replace_text
from mlr.exceptions import CodeBlocksMismatched, TargetCodeBlockEmpty
from mlr.path import ExpandedPath, read_text, write_text


class CLIArgs(object):
    """
    A subclass of argparse.Namespace that exposes type information for all CLI
    arguments supported by the program
    """

    input_paths: list[ExpandedPath]
    rule_paths: list[ExpandedPath]
    dry_run: bool
    show_diff: bool
    quiet: bool


def get_package_version() -> str:
    """
    Retrieve the current package version from the project metadata
    """
    try:
        return importlib.metadata.version("multi-line-replacer")
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0"


def get_cli_args() -> CLIArgs:
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
        "--rule",
        metavar="RULE_FILE",
        dest="rule_paths",
        action="append",
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
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="Show a unified diff of changes for each file.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppresses all output except for errors.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_package_version()}",
    )
    return parser.parse_args(namespace=CLIArgs())


def extract_code_blocks_from_md_path(md_path: Path) -> list[str]:
    """Extract fenced code blocks from a Markdown file at the given path"""
    md_text = md_path.read_text()
    try:
        return extract_code_blocks_from_md_text(md_text)
    except TargetCodeBlockEmpty:
        print(
            f"{Path(sys.argv[0]).name}: "
            f"{md_path}: "
            f"target text code block cannot be empty"
        )
        sys.exit(1)
    except CodeBlocksMismatched:
        print(
            f"{Path(sys.argv[0]).name}: "
            f"{md_path}: "
            f"replacement file must have an even number of fenced code blocks"
        )
        sys.exit(1)


def apply_replacement_rules(input_text: str, *, rule_paths: list[ExpandedPath]) -> str:
    """
    Apply all replacement rules from the given rule files to the input text,
    returning the final modified text
    """
    # Apply each replacement rule to each input file
    for rule_path in rule_paths:
        code_blocks = extract_code_blocks_from_md_path(rule_path)
        # Enumerate fenced code blocks in pairs to get each pair of
        # target/replacement rules
        for target_text, replacement_text in zip(code_blocks[0::2], code_blocks[1::2]):
            input_text = replace_text(input_text, target_text, replacement_text)
    return input_text


def print_file_statuses(
    console: Console, results: list[tuple[ExpandedPath, bool]]
) -> None:
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
    for path_obj, changed in results:
        status_text = "changed" if changed else "unchanged"
        # Build styled text whether we are in a terminal or not;
        # Console will handle stripping styles if necessary
        color = Style(color=None) if changed else "dim"
        txt = Text(str(path_obj), style=color)
        if not changed:
            txt.append(f" ({status_text})", style=color)
        console.print(txt, soft_wrap=True)


def print_diff(
    console: Console, input_path: ExpandedPath, original_text: str, new_text: str
) -> None:
    """
    Print a syntax-highlighted unified diff of the changes to the console.
    """
    diff_lines = list(
        difflib.unified_diff(
            original_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=str(input_path),
            tofile=str(input_path),
        )
    )
    diff_text = "".join(diff_lines)
    syntax = Syntax(
        diff_text,
        "diff",
        theme="monokai",
        word_wrap=True,
        background_color="default",
    )
    console.print(syntax)


def print_dry_run_message(console: Console) -> None:
    """
    Print a dry run notice to the console to inform the user that modifications
    will not be written to disk.
    """
    console.print(
        "[yellow]Note: Dry run enabled; no files will be modified on disk.[/yellow]"
    )


line_endings = ("\r\n", "\n", "\r")


def get_line_ending_from_text(text: str) -> str:
    """
    Choose a single EOL to preserve by inspecting the raw text.
    Prefer CRLF if present, else LF, else CR.
    Fallback to LF if no newline is found.
    """
    for line_ending in line_endings:
        if line_ending in text:
            return line_ending
    return "\n"


def main() -> None:
    """The entry point for the `multi-line-replacer` / `mlr` CLI program"""
    args = get_cli_args()
    results: list[tuple[ExpandedPath, bool]] = []
    warnings: list[str] = []

    console = Console()
    pager = console.pager(styles=True) if args.show_diff else contextlib.nullcontext()

    with pager:
        for input_path in args.input_paths:
            # Check for directories, since the tool is only intended for files
            # or glob patterns
            if input_path.is_dir():
                warnings.append(
                    f"Warning: Skipping {input_path}: directories are "
                    "not supported (use a glob pattern like 'dir/*.txt')",
                )
                continue
            try:
                # Read once without translation to detect original line endings
                orig_line_ending = get_line_ending_from_text(
                    read_text(input_path, newline="")
                )
                # Read again with universal newlines for normalized processing
                orig_input_text = read_text(input_path)
            except UnicodeDecodeError:
                warnings.append(
                    f"Warning: Skipping {input_path}: not a valid text file",
                )
                continue

            input_text = apply_replacement_rules(
                orig_input_text, rule_paths=args.rule_paths
            )
            file_changed = orig_input_text != input_text
            if file_changed:
                if args.show_diff:
                    print_diff(console, input_path, orig_input_text, input_text)
                if not args.dry_run:
                    write_text(input_path, input_text, newline=orig_line_ending)
            results.append((input_path, file_changed))

    if not args.quiet:
        for warning in warnings:
            print(warning, file=sys.stderr)
        if args.dry_run:
            print_dry_run_message(console)
        print_file_statuses(console, results)


if __name__ == "__main__":
    main()
