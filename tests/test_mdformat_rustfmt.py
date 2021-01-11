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
