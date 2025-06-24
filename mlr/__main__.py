#!/usr/bin/env python3.13
import argparse
import os
import re
from pathlib import Path


# Path subclass that automatically expands the user' home directory (i.e. ~)
class ExpandedPath(Path):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, os.path.expanduser(*args), **kwargs)


# Extract fenced code blocks from Markdown
def extract_fenced_code_blocks(md_text):
    code_blocks = re.findall(
        r"```(?:[\w\-]*)\n(.*?)\n```",
        md_text,
        flags=re.DOTALL,
    )
    if len(code_blocks) % 2 != 0:
        raise ValueError(
            "Replacement file must have an even number of fenced code blocks."
        )
    return code_blocks


# Find the string representing the base unit of indentation in a given string of
# text; this can be either two spaces, four spaces, or a tab character.
def get_indent_unit(text):
    for indent_level in ((" " * 2), (" " * 4), "\t"):
        if re.search(rf"^{indent_level}(?=\S)", text, flags=re.MULTILINE):
            return indent_level
    return " " * 4


# Evaluate textual placeholder variables in the given target text to
# achieve certain behaviors (like wildcard-matching through the end of a line,
# or a wildcard-match for only a single word)
def evaluate_placeholder_vars(text):
    placeholder_evaluations = {
        "MATCH_ALL_BUT_NEWLINE": r"[^\n]*",
        "MATCH_ALL_BUT_NEWLINE_LAZY": r"[^\n]*?"
    }
    for placeholder_var_name, replacement in placeholder_evaluations.items():
        text = re.sub(
            rf"\b{re.escape(placeholder_var_name)}\b",
            replacement,
            text,
        )
    return text


# Replace the given text in the input text with the replacement text, preserving
# indentation
def replace_text(input_text, target_text, replacement_text):
    replace_this_patt = "\n".join(
        (
            evaluate_placeholder_vars(rf"([ \t]*){re.escape(line.strip())}")
            if line
            else ""
        )
        for line in target_text.splitlines()
    )
    base_indent_matches = re.search(replace_this_patt, input_text)
    if not base_indent_matches:
        return input_text
    base_indent_level = base_indent_matches.group(1)
    replacement_text = re.sub(
        get_indent_unit(replacement_text),
        get_indent_unit(target_text),
        "\n".join(
            base_indent_level + line if line else ""
            for line in replacement_text.splitlines()
        ),
    )
    input_text = re.sub(replace_this_patt, replacement_text, input_text)
    return input_text


# Define and parse CLI arguments
def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_paths",
        nargs="+",
        type=ExpandedPath,
        help="One or more paths of files to apply replacements to.",
    )
    parser.add_argument(
        "-r",
        "--replacement",
        nargs="+",
        required=True,
        type=ExpandedPath,
        help="One or more paths of replacement rule Markdown files. Each file should contain pairs of triple-backtick (```) fenced code blocks, where the first fenced block is the text to be replaced and the second fenced block is the replacement text.",  # noqa: E501
    )
    return parser.parse_args()


def main():
    args = get_cli_args()
    for input_path in args.input_paths:
        input_text = input_path.read_text()
        for rule_path in args.replacement:
            rule_text = rule_path.read_text()
            code_blocks = extract_fenced_code_blocks(rule_text)
            for target_text, replacement_text in zip(
                code_blocks[0::2], code_blocks[1::2]
            ):
                input_text = replace_text(input_text, target_text, replacement_text)
        input_path.write_text(input_text)


if __name__ == "__main__":
    main()
