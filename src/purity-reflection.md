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
    typematch f {
        case g: a -> Bool \ {} =>
            let h = (k, _) -> g(k);
            let Set(t) = s;
            RedBlackTree.parCount(threads() - 1, h, t)
        case g: a -> Bool \ ef => foldLeft((b, k) -> if (g(k)) b + 1 else b, 0, s)
        case _: _ => unreachable!()
    }
```

Here the `typematch` construct is used to reflect on the purity of `f`:

- If `f` is pure then we evaluate `Set.count` in _parallel_ over the elements of
  the set. 
- If `f` is effectful then we use an ordinary (single-threaded) fold.

The advantage is that we get parallelism for free – _if_ `f` is pure.
