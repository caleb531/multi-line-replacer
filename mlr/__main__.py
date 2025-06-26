#!/usr/bin/env python3.13
import argparse
import os
import re
import sys
from pathlib import PosixPath, WindowsPath

BasePath = WindowsPath if sys.platform == "win32" else PosixPath


# Path subclass that automatically expands the user' home directory (i.e. ~)
class ExpandedPath(BasePath):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, os.path.expanduser(*args), **kwargs)


# Extract fenced code blocks from Markdown
def extract_fenced_code_blocks(md_text):
    code_blocks = re.findall(
        r"```(?:[\w\-]*)\n(.*?)\n```",
        md_text,
        flags=re.DOTALL,
    )
    # If number of code blocks is not even
    if len(code_blocks) % 2 != 0:
        raise ValueError(
            "Replacement file must have an even number of fenced code blocks."
        )
    return code_blocks


# Find the string representing the base unit of indentation in a given string of
# text; this can be either two spaces, four spaces, or a tab character.
def get_indent_unit(text):
    for indent_level in ((" " * 2), (" " * 4), "\t"):
        # The positive lookahead is because since 2-space indent is really a
        # subset of 4-space indent, we need to be able to distinguish between
        # the two, so we check to see if there
        if re.search(rf"^{indent_level}(?=\S)", text, flags=re.MULTILINE):
            return indent_level
    return None


# Evaluate textual placeholder variables in the given target text to
# achieve certain behaviors (like wildcard-matching through the end of a line,
# or a wildcard-match for only a single word)
def evaluate_placeholder_vars(text):
    placeholder_evaluations = {
        # Match all non-newline characters until the end of the line is reached
        "MATCH_UNTIL_END_OF_LINE": r"[^\n]*",
        # Match all non-newline characters between two delimiters (like quotes)
        "MATCH_ALL_BETWEEN": r"[^\n]*?",
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
            # Evaluate special placeholder variables like MATCH_UNTIL_END_OF_LINE
            evaluate_placeholder_vars(rf"([ \t]*){re.escape(line.strip())}")
            if line
            else ""
        )
        for line in target_text.splitlines()
    )
    # Retrieve the base indentation level in the target text to ensure that the
    # replacement text is indented the same amount
    base_indent_matches = re.search(replace_this_patt, input_text)
    if not base_indent_matches:
        return input_text
    base_indent_level = base_indent_matches.group(1)
    # Ensure that the replacement text's preferred indentation unit matches that
    # of the input text
    replacement_indent_unit = get_indent_unit(replacement_text)
    if replacement_indent_unit:
        replacement_text = re.sub(
            replacement_indent_unit,
            get_indent_unit(input_text),
            replacement_text,
        )
    # Ensure that the replacement text is indented to the same amount as the
    # target text it is replacing
    replacement_text = "\n".join(
        # The ternary syntax is to prevent trailing whitespace from being added
        # to blank lines
        base_indent_level + line if line else ""
        for line in replacement_text.splitlines()
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
        # Apply each replacement rule to each input file
        for rule_path in args.replacement:
            rule_text = rule_path.read_text()
            code_blocks = extract_fenced_code_blocks(rule_text)
            # Enumerate fenced code blocks in pairs to get each pair of
            # target/replacement rules
            for target_text, replacement_text in zip(
                code_blocks[0::2], code_blocks[1::2]
            ):
                input_text = replace_text(input_text, target_text, replacement_text)
        input_path.write_text(input_text)


if __name__ == "__main__":
    main()
