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
let x = 5;
let y = 6;
}
~~~
.
```rust
fn main() {
#   // comment
    let s = "asdf
## literal hash";
    let x = 5;
    let y = 6;
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
trait SomeTrait {   fn nothing() {} }
 struct Another;

 impl  Another {}
~~~
.
```rust
# struct Something {}
# 
# fn main() {}
# 
trait SomeTrait {
    fn nothing() {}
}

struct Another;

impl Another {}
```
.
Comment collapse does not delete lines
.
~~~rust
# fn main() -> Result<(), amethyst::Error> {
#   let game_data = DispatcherBuilder::default().with_bundle(
        // inside your rendering bundle setup
        RenderingBundle::<DefaultBackend>::new()
            .with_plugin(RenderFlat2D::default())
#   )?;
#   Ok(())
# }
~~~
.
```rust
# fn main() -> Result<(), amethyst::Error> {
#   let game_data = DispatcherBuilder::default().with_bundle(
        // inside your rendering bundle setup
        RenderingBundle::<DefaultBackend>::new().with_plugin(RenderFlat2D::default()),
#   )?;
#   Ok(())
# }
```
.