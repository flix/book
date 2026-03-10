# Printing to Standard Out

The Flix Prelude defines the `println` function which prints to standard out.
For example:

```flix
println("Hello World")
```

The `println` function can print any value whose type implements the `ToString`
trait and consequently can be converted to a `String`. For example:

```flix
let o = Some(123);
let l = 1 :: 2 :: 3 :: Nil;
println(o);
println(l)
```

The `println` function is rightfully effectful, hence it cannot be called from a
pure function. To debug a pure function, use the builtin [debugging
facilities](./debugging.md).

## The Console Effect

The `Console` effect defines operations for reading from and writing to the
terminal:

```flix
use Sys.Console

eff Console {
    def readln(): String
    def print(s: String): Unit
    def eprint(s: String): Unit
    def println(s: String): Unit
    def eprintln(s: String): Unit
}
```
