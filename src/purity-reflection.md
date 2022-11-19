# Purity Reflection

> **Note:** This feature is experimental and not yet intended for use.

Purity reflection is an advanced Flix feature that enables higher-order functions to inspect
the purity of their function arguments. This allows us to write functions that use _selective_ lazy
and/or parallel evaluation.

For example, here is the implementation of `Set.count`:

```flix
@ParallelWhenPure
pub def count(f: a -> Bool \ ef, s: Set[a]): Int32 \ ef =
    typematch f {
        case g: a -> Bool \ {} =>
            if (useParallelEvaluation(s))
                let h = (k, _) -> g(k);
                let Set(t) = s;
                RedBlackTree.parCount(threads() - 1, h, t) as \ {}
            else
                foldLeft((b, k) -> if (f(k)) b + 1 else b, 0, s)
        case g: a -> Bool \ ef => foldLeft((b, k) -> if (g(k)) b + 1 else b, 0, s)
        case _: _ => unreachable!()
    }
```

Here the `reifyEff` construct allows us to reflect on the purity of `f`.
We have two cases: `f` is guaranteed to be pure (in which case we bind it to `g` and
take the first branch) and `f` may be impure.

If `f` is pure then we apply it in parallel over the set. Otherwise we apply it
sequentially.
