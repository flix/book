# Parallelism

We have seen how the `spawn` expression allows us to evaluate an expression in a
new thread:

```flix
region rc {
    spawn (1 + 2) @ rc
}
```

This allows us to write concurrent and parallel programs using structured
concurrency. The downside is that we must manually coordinate communication
between threads using channels.
If we want parallelism, but not concurrency, a more light-weight approach
is to use the `par-yield` expression:

```flix
par (x <- e1; y <- e2; z <- e3)
    yield x + y + z
```

which evaluates `e1`, `e2`, and `e3` in parallel and binds their results to `x`, `y`, and `z`.

We can use `par-yield` to write a parallel `List.map` function:

```flix
def parMap(f: a -> b, l: List[a]): List[b] = match l {
    case Nil     => Nil
    case x :: xs =>
        par (r <- f(x); rs <- parMap(f, xs))
            yield r :: rs
}
```

This function will evaluate `f(x)` and `parMap(f, xs)` in parallel.

> **Note:** The `par-yield` construct only works with pure expressions.

If you want to run effectful operations in parallel, you must use explicit
regions and threads.
