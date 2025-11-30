# Debugging

When debugging, it is often helpful to output the value of an expression or
variable.

We might try something like:

```flix
def sum(x: Int32, y: Int32): Int32 =
    let result = x + y;
    println("The sum of ${x} and ${y} is ${result}");
    result
```

Unfortunately this does not work:

```
❌ -- Type Error -------------------------------------------------- Main.flix

>> Unable to unify the effect formulas: 'IO' and 'Pure'.

1 |> def sum(x: Int32, y: Int32): Int32 =
2 |>     let result = x + y;
3 |>     println("The sum of ${x} and ${y} is ${result}");
4 |>     result
```

The problem is that `println` has the `IO`. Hence, we cannot use it to for 
print debugging inside pure functions. We could make our `sum` function have
the `IO` effect, but that is rarely what we want. Instead, Flix has a
built-in debugging facility that allows us to do print-line debugging.

## The `Debug.dprintln` Function

Instead, we can use the `Debug.dprintln` function and write:

```flix
use Debug.dprintln;

def sum(x: Int32, y: Int32): Int32 =
    let result = x + y;
    dprintln("The sum of ${x} and ${y} is ${result}");
    result
```

Inside the `sum` function, the `dprintln` has the effect `Debug`, but due to
its special nature, the `Debug` effect "disappears" once we exit the function,
i.e. it is not part of its type and effect signature.

## Debugging with Source Locations

We can use the special _debug string interpolator_ to add source locations
to our print statements:

```flix
use Debug.dprintln;

def sum(x: Int32, y: Int32): Int32 =
    let result = x + y;
    dprintln(d"The sum of ${x} and ${y} is ${result}");
    result
```

> A longer introduction to `dprintln` is available in the
> blog post [Effect Systems vs Print Debugging: A Pragmatic Solution](https://blog.flix.dev/blog/effect-systems-vs-print-debugging/)
