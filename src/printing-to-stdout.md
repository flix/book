## Printing to Standard Out

The Flix prelude defines two impure functions:
`print` and `println` that can be used to print a
string to standard out.
For example:

```flix
println("Hello World")
```

The `println` function prints with a newline after the
string.
The `print` function can be used to print without this
newline.
For example:

```flix
let name = "Lucky Luke";
print("Hello");
print(" ");
println(name)
```

which prints `Hello Lucky Luke` on one line.

The `print` and `println` functions can print any
value whose type implements `ToString` type class and
consequently can be converted to a `String`.
For example:

```flix
let o = Some(123);
let l = 1 :: 2 :: 3 :: Nil;
println(o);
println(l)
```

The `print` and `println` functions are rightfully
`Impure`.
Consequently they cannot be called from a pure
context.
This can sometimes hinder debugging of a pure function
where you want to log some intermediate computation.
A solution is to cast the `print` and `println`
functions as `Pure`.
Here is an example:

```flix
def sum(x: Int32, y: Int32): Int32 =
    let _ = println(x) as \ {};
    let _ = println(y) as \ {};
    x + y
```

Note that `sum` remains a pure function despite the
two calls to `println`.
Moreover, since the call `println(x)` is pure we must
introduce a let-binding with an unused variable to
prevent Flix from rejecting the program due to a
redundant pure computation.
