# Purity Reflection

> **Note:** This is an advanced feature and should only be used by experts.

Purity reflection enables higher-order functions to inspect the purity of their
function arguments. 

This allows us to write functions that use _selective_ lazy and/or parallel
evaluation.

For example, here is the implementation of `Set.count`:

```flix
@ParallelWhenPure
pub def count(f: a -> Bool \ ef, s: Set[a]): Int32 \ ef =
    match purityOf(f) {
        case Purity.Pure(g) =>
            if (useParallelEvaluation(s))
                let h = (k, _) -> g(k);
                let Set(t) = s;
                RedBlackTree.parCount(h, t)
            else
                foldLeft((b, k) -> if (f(k)) b + 1 else b, 0, s)
        case Purity.Impure(g) => foldLeft((b, k) -> if (g(k)) b + 1 else b, 0, s)
    }
```

Here the `purityOf` function is used to reflect on the purity of `f`:

- If `f` is pure then we evaluate `Set.count` in _parallel_ over the elements of
  the set (if the set is big enough to warrant it). 
- If `f` is effectful then we use an ordinary (single-threaded) fold.

The advantage is that we get parallelism for free – _if_ `f` is pure.
