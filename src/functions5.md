# Curried by Default

Functions are curried by default.
A curried function can be called with fewer
arguments than it declares returning a new function
that takes the remainder of the arguments.
For example:

```flix
def sum(x: Int32, y: Int32): Int32 = x + y

def main(): Unit & Impure =
    let inc = sum(1);
    inc(42) |> println
```

Here the `sum` function takes two arguments, `x` and
`y`, but it is only called with one argument inside
`main`.
This call returns a new function which is
similar to `sum`, except that in this function `x`
is always bound to `1`.
Hence when `inc` is called with `42` it returns `43`.

Currying is useful in many programming patterns.
For example, consider the `List.map` function.
This function takes two arguments, a function of
type `a -> b` and a list of type `List[a]`, and
returns a `List[b]` obtained by applying the
function to every element of the list.
Now, if we combine currying with the pipeline
operator `|>` we are able to write:

```flix
def main(): Unit & Impure =
    List.range(1, 100) |>
    List.map(x -> x + 1) |>
    println
```

Here the call to `List.map` passes the function
`x -> x + 1` which *returns* a new function that
expects a list argument.
This list argument is then supplied by the pipeline
operator `|>` which, in this case, expects a list
and a function that takes a list.
