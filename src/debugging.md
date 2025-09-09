## Debugging

When debugging, it is often helpful to output the value of an expression or
variable.

We might try something like:

```flix
def sum(x: Int32, y: Int32): Int32 =
    println(x);
    println(y);
    x + y
```

Unfortunately this does not work:

```
❌ -- Type Error -------------------------------------------------- Main.flix

>> Impure function declared as pure.

1 | def sum(x: Int32, y: Int32): Int32 =
        ^^^
        impure function.
```

The problem is that printing is inherently an effectful operation and hence we
cannot use it to debug our pure functions! We could make our `sum` function have
the `IO` effect, but that is rarely what we want. Fortunately, Flix has a
built-in debugging facility that allows us to do print-line debugging.

### The dbg Function

Flix has a `dbg` (short for "debug") function, with the same signature as the `identity` function:

```flix
def dbg(x: a): a
```

The `dbg` "function" isn't really a function; rather it's internal compiler
magic that allows you to print _any value_ while fooling the type and effect
system into believing that it is still pure. Using the `dbg` function this
program:

```flix
def sum(x: Int32, y: Int32): Int32 =
    dbg(x);
    dbg(y);
    x + y
```

Now compiles and runs.

The `dbg` function returns its argument. Hence it's convenient to use in many
situations.

For example, we can write:

```flix
def sum(x: Int32, y: Int32): Int32 = dbg(x + y)
```

to print the value of `x + y` _and_ return it.

We can also use it inside a pipeline:

```flix
List.range(1, 100) |>
List.map(x -> dbg(x + 1)) |>
List.filter(x -> dbg(x > 5))
```

### Debug Format

The `dbg` expression (and its variants) do _not_ use the `ToString` trait.
Instead they print the internal Flix representation of the given value.

For example, the expression:

```flix
dbg(1 :: 2 :: Nil)
```

prints:

```flix
Cons(1, Cons(2, Nil))
```

We can also print values that do not have a `ToString` instance:

```flix
dbg(x -> x + 123)
```

prints:

```
Int32 -> Int32
```

We can always obtain the `ToString` representation by using an interpolated
string. For example:

```flix
dbg("${x}")
```

### Debug Variants

The `dbg` function comes in three variants:

- `dbg`: Prints its argument.
- `dbg!`: Prints its argument and source location.
- `dbg!!`: Prints its argument, source location, and source code.

The following program:

```flix
def main(): Unit =
    dbg("A message");
    dbg!("Another message");
    dbg!!("A third message");
    ()
```

prints:

```
"A message"
[C:\tmp\flix\Main.flix:3] "Another message"
[C:\tmp\flix\Main.flix:4] A third message = "A third message"
```

The third `dbg!!` variant is intended to be used in situations like:

```flix
let x = 123;
let y = 456;
dbg!!(x + y)
```

where it prints:

```
[C:\tmp\flix\Main.flix:3] x + y = 579
```

> **Note:** The `dbg` expression should not be used in production code.

> **Warning:** The Flix compiler treats the `dbg` expression as pure, hence
> under certain circumstances the compiler may reorder or entirely remove a use
> of `dbg`.

