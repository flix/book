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

>> Unable to unify the effect formulas: 'IO' and 'Pure'.

1 |> def sum(x: Int32, y: Int32): Int32 =
2 |>     println(x);
3 |>     println(y);
4 |>     x + y
```

The problem is that `println` has the `IO`. Hence, we cannot use it to for 
print debugging inside pure functions. We could make our `sum` function have
the `IO` effect, but that is rarely what we want. Instead, Flix has a
built-in debugging facility that allows us to do print-line debugging.

### The `Debug.dprint` and `Debug.dprintln` Functions

We can write:

```flix
use Debug.dprintln;

def sum(x: Int32, y: Int32): Int32 =
    dprintln(x);
    dprintln(y);
    x + y
```

Inside the `sum` function, the `dprintln` has the effect `Debug`, but due to
its special nature, the `Debug` effect "disappears" once we exit the function,
i.e. it is not part of its type and effect signature.

### Debugging with Source Locations

We can use the special _debug string interpolator_ to add source locations
to our print statements:

```flix
use Debug.dprintln;

def sum(x: Int32, y: Int32): Int32 =
    dprintln(d"Hello World!");
    x + y
```

> A longer introduction to `dprintln` is available in the
> blog post [Effect Systems vs Print Debugging: A Pragmatic Solution](https://blog.flix.dev/blog/effect-systems-vs-print-debugging/)
