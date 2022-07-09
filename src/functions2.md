# First-Class and Higher-Order Functions

A *higher-order function* is a function that takes a
parameter which is itself a function.
For example:

```flix
def twice(f: Int32 -> Int32, x: Int32): Int32 = f(f(x))
```

Here the `twice` function takes two arguments, a
function `f` and an integer `x`, and applies `f` to
`x` two times.

We can pass a lambda expression to the `twice`
function:

```flix
twice(x -> x + 1, 42)
```

which evaluates to `44` since `42` is incremented
twice.

We can also define a higher-order function that
requires a function which takes two arguments:

```flix
def twice(f: (Int32, Int32) -> Int32, x: Int32): Int32 =
    f(f(x, x), f(x, x))
```

which can be called as follows:

```flix
twice((x, y) -> x + y, 42)
```

We can call a higher-order function with a top-level
function as follows:

```flix
def inc(x: Int32): Int32 = x + 1

def twice(f: Int32 -> Int32, x: Int32): Int32 = f(f(x))

twice(inc, 42)
```
