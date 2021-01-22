__version__ = "0.0.3"  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT

from collections.abc import Iterable
import re
import subprocess
from typing import Callable

in_commented = False


def flatten(deep_list):
    for el in deep_list:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def format_rust(unformatted: str, _info_str: str) -> str:
    global in_commented
    global remove_newlines

    unformatted = _for_each_line(unformatted, _hide_sharp)

    unformatted_bytes = unformatted.encode("utf-8")
    result = subprocess.run(
        ["rustfmt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        input=unformatted_bytes,
    )

    formatted = result.stdout.decode("utf-8")

    if result.returncode:
        raise Exception("Failed to format Rust code\n" + formatted)

    in_commented = False
    remove_newlines = False

    return _for_each_line(formatted, _unhide_sharp).replace("\r", "")


def _for_each_line(string: str, action: Callable[[str], str]) -> str:
    lines = string.split("\n")

    lines = [action(line) for line in lines]

    lines = list(flatten(lines))

    lines = [x for x in lines if x is not None]
    return "\n".join(lines)


_RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN = "//__MDFORMAT_RUSTFMT_COMMENT_BEGIN__"
_RUSTFMT_CUSTOM_COMMENT_BLOCK_END = "//__MDFORMAT_RUSTFMT_COMMENT_END__"
_RUSTFMT_CUSTOM_COMMENT_ESCAPE = "//__MDFORMAT_RUSTFMT_COMMENT_ESCAPE__"
_RUSTFMT_CUSTOM_COMMENT_BLANK_LINE = "//__MDFORMAT_RUSTFMT_COMMENT_BLANK_LINE__"


def _hide_sharp(line: str):
    global in_commented
    stripped = line.strip()

    if stripped.startswith("# ") or stripped.startswith("##") or stripped == "#":
        tokens = []

        if not in_commented:
            in_commented = True
            tokens.append(_RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN)

        if stripped.startswith("##"):
            tokens.append(_RUSTFMT_CUSTOM_COMMENT_ESCAPE)

        # if stripped == "#":
        #     tokens.append(_RUSTFMT_CUSTOM_COMMENT_BLANK_LINE)

        tokens.append(stripped[1:])

        return tokens

    if in_commented:
        in_commented = False
        return [_RUSTFMT_CUSTOM_COMMENT_BLOCK_END, stripped]

    return stripped


next_line_escape = False
remove_newlines = False


def _unhide_sharp(line: str):
    global in_commented
    global next_line_escape
    global remove_newlines

    if _RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN in line:
        remove_newlines = True
        in_commented = True
        line = re.sub(
            re.escape(_RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN), "", line, 1
        ).rstrip()
        return line or None

    if _RUSTFMT_CUSTOM_COMMENT_BLOCK_END in line:
        in_commented = False
        line = re.sub(
            re.escape(_RUSTFMT_CUSTOM_COMMENT_BLOCK_END), "", line, 1
        ).rstrip()
        return line or None

    if _RUSTFMT_CUSTOM_COMMENT_ESCAPE in line:
        next_line_escape = True
        line = re.sub(re.escape(_RUSTFMT_CUSTOM_COMMENT_ESCAPE), "", line, 1).rstrip()
        return line or None

    if _RUSTFMT_CUSTOM_COMMENT_BLANK_LINE in line:
        return "#"

    if in_commented:
        if line == "" and remove_newlines:
            return None

        remove_newlines = False

        if line.startswith("#") and next_line_escape:
            next_line_escape = False
            return "#" + line

        if line.startswith(" "):
            return "#" + line[1:]

        return "# " + line

    return line
