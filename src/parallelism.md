# Parallelism

> **Note:** This feature is available in Flix 0.31 and onwards.

We have seen how the `spawn` expression can be used to run an expression in another light-weight
thread:

```flix
spawn (1 + 2)
```

This allows us to write both concurrent and parallel programs. The downside is that we must
manually coordinate communication between threads using channels. A more light-weight approach is to use the `par` expression.

The `par` expression:

```flix
par f(e1, e2, e3)
```

evaluates the function expression `f`, and its argument expressions `e1`, `e2`, and `e3` in parallel.
Once all four expressions have been reduced to a value, the function `f` is called with the arguments.

This allows us to write a parallel `List.map` function:

```flix
def parMap(f: a -> b, l: List[a]): List[b] = match l {
    case Nil     => Nil
    case x :: xs => par f(x) :: parMap(f, xs)
}
```

This function will evaluate `f(x)` and `parMap(f, xs)` in parallel and combine their results.
