## Printing to Standard Out

The Flix Prelude defines the `println` function which prints to standard out.
For example:

```flix
println("Hello World")
```

The `println` function can print any value whose type implements `ToString` type
class and consequently can be converted to a `String`. For example:

```flix
let o = Some(123);
let l = 1 :: 2 :: 3 :: Nil;
println(o);
println(l)
```

The `println` function is rightfully effectful, hence it cannot be called from a
pure function. To debug a pure function, use the builtin [debugging
facilities](./debugging.md).

### The Console Module

The `Console` module defines additional functions for reading from or writing to
the terminal: 

```flix
mod Console {
    def print(x: a): Unit \ IO with ToString[a]
    def printLine(x: a): Unit \ IO with ToString[a]
    def readLine(): Result[String, String] \ IO Impure
}
```
