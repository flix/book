## Debugging

When debugging, it is often helpful to output the values of expressions and variables. This can be challenging in a functional language like Flix because `print` is impure, so:

```flix
def myAdd(x: Int32): Int32 =
    println("myAdd called with: ${x}");
    x + 1
```

Results in an error:

```
Impure function declared as pure.
```

### `debug`

Flix provides a special-case `debug` function which has the same signature as the `identity` fuction:

```flix
def debug(x: a): a
```

> **Note:** `debug` isn't a true function, which means that there are a few limitations on how it can be used: see [Limitations](#limitations) for details.

Because `debug` appears to be pure, it can be used anywhere within Flix, including pure functions:

```flix
def myAdd(x: Int32): Int32 =
    debug("myAdd called with: ${x}");
    x + 1
```

And because it returns its argument, it can be inserted within expressions without modifying their behaviour. For example let statements:

```flix
let x = debug(1 + 1);
```

For-yield expressions:

```flix
for(i <- List.range(0, 10);
    j <- debug(List.range(i, 10)))
    yield (i, j)
```

Or pipelines:

```flix
DelayList.from(42) |> DelayList.map(x -> x + 10) |> debug |> DelayList.take(10)
```

### Debug Format

The `debug` expression (and its variants) do _not_ use the `ToString` type
class. Instead they print the internal Flix representation of the given value. 

For example, the expression:

```flix
debug(1 :: 2 :: Nil)
```

prints:

```flix
Cons(1, Cons(2, Nil))
```

We can also print values that do not have a `ToString` instance: 

```flix
debug(x -> x + 123)
```

prints:

```
Int32 -> Int32
```

We can always obtain the `ToString` representation by using an interpolated
string. For example:

```flix
debug("${x}")
```

### Debug Variants

The `debug` function comes in three variants:

- `debug`: Prints its argument.
- `debug!`: Prints its argument and source location.
- `debug!!`: Prints its argument, source location, and source code.

The following program:

```flix
def main(): Unit = 
    debug("A message");
    debug!("Another message");
    debug!!("A third message");
    ()
```

prints:

```
"A message"
[C:\tmp\flix\Main.flix:3] "Another message"
[C:\tmp\flix\Main.flix:4] A third message = "A third message"
```

The third `debug!!` variant is intended to be used in situations like:

```flix
let x = 123;
let y = 456;
debug!!(x + y)
```

where it prints:

```
[C:\tmp\flix\Main.flix:3] x + y = 579
```

> **Note:** The `debug` expression should not be used in production code. 

> **Warning:** The Flix compiler treats the `debug` expression as pure, hence
> under certain circumstances the compiler may reorder or entirely remove a use
> of `debug`.

