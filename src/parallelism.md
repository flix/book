# Parallelism

> **Note:** This feature is experimental and not yet intended for use.

We have seen how the `spawn` expression allow us to evaluate an expression in another thread:

```flix
spawn (1 + 2)
```

This allows us to write both concurrent and parallel programs. 
The downside is that we must manually coordinate communication between threads using channels. 
If want parallelism, but not concurrency, a more light-weight approach is to use the `par` expression.

The `par` expression:

```flix
par (1 + 2, 3 + 4)
```

evaluates `1 + 2` and `3 + 4` in *parallel* and returns a tuple with the result. 

If we have expressions `e1`, `e2`, and `e3` and we want evaluate them in parallel, we can write:

```flix
let (x, y, z) = par (e1, e2, e3)
```

which will spawn a thread for each of `e1`, `e2`, and `e3` and bind the result to the local variables `x`, `y`, and `z`.

For convenience, Flix also supports a parallel function application expression.

The `par` expression:

```flix
par f(e1, e2, e3)
```

evaluates the function expression `f`, and its argument expressions `e1`, `e2`, and `e3` in parallel.

Once all four expressions have been evaluated, the function `f` is called with the arguments in the current thread.

This allows us to write a parallel `List.map` function:

```flix
def parMap(f: a -> b, l: List[a]): List[b] = match l {
    case Nil     => Nil
    case x :: xs => par (f(x) :: parMap(f, xs))
}
```

This function will evaluate `f(x)` and `parMap(f, xs)` in parallel. Thus each recursive call spawns a new thread.
Whether this leads to performance improvements depends on how expensive `f` is to compute.

> **Note:** The `par` construct requires the sub-expression(s) to be pure.
