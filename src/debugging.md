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

### The `Debug.dprint` and `Debug.dprintln` Functions

Instead, we can write the following:

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

We should only use `dprintln` and `dprint` for debugging. 

A future version of Flix will disallow it in production mode.
