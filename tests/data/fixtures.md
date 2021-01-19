Simple test
.
~~~rust
fn main(){println!("Hello World!");}
~~~
.
```rust
fn main() {
    println!("Hello World!");
}
```
.


Ignore setup code
.
~~~rust
fn main() {
  # let x=a();b();c();
  let y=d();e();f();
}
~~~
.
```rust
fn main() {
    # let x=a();b();c();
    let y = d();
    e();
    f();
}
```
.
