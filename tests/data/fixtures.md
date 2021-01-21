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
#   let x = a();
#   b();
#   c();
    let y = d();
    e();
    f();
}
```
.

Format hidden lines
.
~~~rust
fn main() {
  #       let x=a();b();c();
}
~~~
.
```rust
fn main() {
#   let x = a();
#   b();
#   c();
}
```
.

Handle empty comment lines
.
~~~rust
fn main() {
  #
#
    # // comment
let s = "asdf
## literal hash";
}
~~~
.
```rust
fn main() {
#   // comment
    let s = "asdf
## literal hash";
}
```
.

Handle hidden derive and attr statements
.
~~~rust
#   #[derive(Debug)]
struct MyStruct {}
~~~
.
```rust
# #[derive(Debug)]
struct MyStruct {}
```
.
Handle derive and attr statements
.
~~~rust
#[derive(Debug)]
struct MyStruct {}
~~~
.
```rust
#[derive(Debug)]
struct MyStruct {}
```
.
[NIGHTLY] Preserve blank lines
.
~~~rust
# struct Something {}
#
#
# fn main() {}
#
#
~~~
.
```rust
# struct Something {}
# 
# fn main() {}
```
.
