[![Build Status](https://github.com/hukkinj1/mdformat-rustfmt/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-rustfmt/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)
[![PyPI version](<https://img.shields.io/pypi/v/mdformat-rustfmt>)](<https://pypi.org/project/mdformat-rustfmt>)

# mdformat-rustfmt
> Mdformat plugin to rustfmt Rust code blocks

## Description
mdformat-rustfmt is an [mdformat](https://github.com/executablebooks/mdformat) plugin
that makes mdformat format Rust code blocks with [rustfmt](https://github.com/rust-lang/rustfmt).
The plugin invokes rustfmt in a subprocess so having it installed is a requirement.

## Installing
1. [Install rustfmt](https://github.com/rust-lang/rustfmt#quick-start)
1. Install mdformat-rustfmt
   ```bash
   pip install mdformat-rustfmt
   ```

## Usage
```bash
mdformat YOUR_MARKDOWN_FILE.md
```
