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

### Output format

Debug output is not generated with `toString`. Instead `debug` prints the internal Flix datastructure. For example `debug(1 :: 2 :: Nil)` outputs:

```flix
Cons(1, Cons(2, Nil))
```

This means that `debug` can output any Flix datastructure, whether or not it implements the `ToString` class.

You can bypass this by calling `toString` yourself, or using string interpolation:

```flix
debug("${x}")
```

The debug format is available within string interploation by using `%{...}`:

```flix
println("Internally, lists look like this: %{1 :: 2 :: Nil}")
```

### Source location and expression

Flix provides two additional variants of `debug`: `debug!` and `debug!!`. The first displays the source location from which `debug` was called, and the second both the source location and the source code of the expression passed to `debug!!`

### Limitations

* Although `debug` *appears* to be pure, it is not, and should not be used in production code. Future versions of Flix will enforce this requirement by raising an error if `debug` appears in production builds.
* The location and expression output by `debug!` and `debug!!` are not guaranteed to be correct if they're used as values (e.g. within a pipeline).
* Because `debug` appears to be pure, it can be optimised away, for example if the value is not used:
  ```flix
  let _ = debug(...)
  ```
