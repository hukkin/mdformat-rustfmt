__version__ = "0.0.3"  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT

import subprocess
from typing import Callable
from collections.abc import Iterable


in_commented = False


def flatten(deep_list):
    for el in deep_list:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def format_rust(unformatted: str, _info_str: str) -> str:
    global in_commented

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
    return _for_each_line(formatted, _unhide_sharp).replace("\r", "") + "\n"


def _for_each_line(string: str, action: Callable[[str], str]) -> str:
    lines = string.split("\n")

    lines = [action(line) for line in lines]

    lines = list(flatten(lines))

    lines = list(filter(None, lines))
    return "\n".join(lines)


_RUSTFMT_CUSTOM_COMMENT_PREFIX = "//__MDFORMAT_RUSTFMT__"
_RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN = "//__MDFORMAT_RUSTFMT_COMMENT_BEGIN__"
_RUSTFMT_CUSTOM_COMMENT_BLOCK_END = "//__MDFORMAT_RUSTFMT_COMMENT_END__"


def _hide_sharp(line: str):
    global in_commented
    stripped = line.strip()

    if stripped.startswith("#") and not line.startswith("##"):
        if not in_commented:
            in_commented = True
            return [_RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN, stripped[1:]]

        return stripped[1:]

    if in_commented:
        in_commented = False
        return [_RUSTFMT_CUSTOM_COMMENT_BLOCK_END, stripped]

    return stripped


def _unhide_sharp(line: str):
    global in_commented

    if _RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN in line:
        in_commented = True
        return None

    if _RUSTFMT_CUSTOM_COMMENT_BLOCK_END in line:
        in_commented = False
        return None

    if in_commented:
        if line.startswith("#"):
            return "#" + line
        if line.startswith(" "):
            return "#" + line[1:]

        return "# " + line

    return line
