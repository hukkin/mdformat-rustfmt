__version__ = "0.0.2"  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT

import subprocess
from typing import Callable


def format_rust(unformatted: str, _info_str: str) -> str:
    unformatted = _for_each_line(unformatted, _hide_sharp)
    unformatted_bytes = unformatted.encode("utf-8")
    result = subprocess.run(
        ["rustfmt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        input=unformatted_bytes,
    )
    if result.returncode:
        raise Exception("Failed to format Rust code")
    formatted = result.stdout.decode("utf-8")
    formatted = _for_each_line(formatted, _unhide_sharp)
    return formatted


def _for_each_line(string: str, action: Callable[[str], str]) -> str:
    lines = string.split("\n")
    lines = (action(line) for line in lines)
    return "\n".join(lines)


_RUSTFMT_CUSTOM_COMMENT_PREFIX = "//#### "


def _hide_sharp(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("# ") or stripped == "#":
        return _RUSTFMT_CUSTOM_COMMENT_PREFIX + line
    return line


def _unhide_sharp(line: str) -> str:
    lstripped = line.lstrip()
    if lstripped.startswith(_RUSTFMT_CUSTOM_COMMENT_PREFIX):
        return _removeprefix(lstripped, _RUSTFMT_CUSTOM_COMMENT_PREFIX)
    return line


def _removeprefix(string: str, prefix: str) -> str:
    if string.startswith(prefix):
        return string[len(prefix) :]
    return string
