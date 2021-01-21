__version__ = "0.0.3"  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT

from collections.abc import Iterable
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


_RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN = "//__MDFORMAT_RUSTFMT_COMMENT_BEGIN__"
_RUSTFMT_CUSTOM_COMMENT_BLOCK_END = "//__MDFORMAT_RUSTFMT_COMMENT_END__"
_RUSTFMT_CUSTOM_COMMENT_ESCAPE = "//__MDFORMAT_RUSTFMT_COMMENT_ESCAPE__"


def _hide_sharp(line: str):
    global in_commented
    stripped = line.strip()

    if stripped.startswith("#"):
        if not in_commented:
            in_commented = True

            if stripped.startswith("##"):
                return [
                    _RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN,
                    _RUSTFMT_CUSTOM_COMMENT_ESCAPE,
                    stripped[1:],
                ]
            else:
                return [_RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN, stripped[1:]]
        if stripped.startswith("##"):
            return [_RUSTFMT_CUSTOM_COMMENT_ESCAPE, stripped[1:]]
        else:
            return stripped[1:]

    if in_commented:
        in_commented = False
        return [_RUSTFMT_CUSTOM_COMMENT_BLOCK_END, stripped]

    return stripped


next_line_escape = False


def _unhide_sharp(line: str):
    global in_commented
    global next_line_escape

    if _RUSTFMT_CUSTOM_COMMENT_BLOCK_BEGIN in line:
        in_commented = True
        return None

    if _RUSTFMT_CUSTOM_COMMENT_BLOCK_END in line:
        in_commented = False
        return None

    if _RUSTFMT_CUSTOM_COMMENT_ESCAPE in line:
        next_line_escape = True
        return None

    if in_commented:
        if line.startswith("#") and next_line_escape:
            next_line_escape = False
            return "#" + line
        if line.startswith(" "):
            return "#" + line[1:]

        return "# " + line

    return line
