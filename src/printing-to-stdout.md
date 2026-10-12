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
eff Console {
    def readln(): Option[String]
    def write(s: String): Unit
    def writeLine(s: String): Unit
    def writeErr(s: String): Unit
    def writeErrLine(s: String): Unit
}
```

The `Sys.Console` module defines `Console.print`, `Console.println`,
`Console.eprint`, and `Console.eprintln` on top of these operations. Like the
`println` of the Prelude, they accept any value with a `ToString` instance, but
they have the `Console` effect rather than `IO`. See the
[Console](./console.md) chapter for details.
