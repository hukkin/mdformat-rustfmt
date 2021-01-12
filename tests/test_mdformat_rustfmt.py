import mdformat


def test_mdformat_integration():
    unformatted_md = """~~~rust
fn main(){println!("Hello World!");}
~~~
"""
    formatted_md = """```rust
fn main() {
    println!("Hello World!");
}
```
"""
    assert mdformat.text(unformatted_md, codeformatters={"rust"}) == formatted_md


def test_rustfmt_error(capfd):
    """Test that any prints by rustfmt go to devnull."""
    unformatted_md = """~~~rust
blaalbal.ablaa
~~~
"""
    formatted_md = """```rust
blaalbal.ablaa
```
"""
    result = mdformat.text(unformatted_md, codeformatters={"rust"})
    captured = capfd.readouterr()
    assert not captured.err
    assert not captured.out
    assert result == formatted_md
