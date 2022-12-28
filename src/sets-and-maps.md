# Sets and Maps

Flix has excellent support for (immutable) `Set`s and `Map` based on balanced
trees; hence the elements of a `Set` and the keys of `Map` must implement the
`Order` type class. 

> **Tip:** The Flix `Set` and `Map` data structures will automatically
> parallelize certain operations. Such operations are marked with
> `@ParallelWhenPure` in the API docs. 

## Sets

The empty set is written as:

```flix
Set#{}
```

which is equivalent to `Set.empty()`. A set literal is written as:

```flix
Set#{1, 2, 3}
```

We can insert into a `Set` using `Set.insert`:

```flix
let s1 = Set#{1, 2, 3};
let s2 = Set.insert(4, s1);
```

We can determine if a `Set` contains an element using `Set.memberOf`:

```flix
let s = Set#{1, 2, 3};
Set.memberOf(2, s)
```

We can merge two sets using `Set.union`:

```flix
let s1 = Set#{1, 2, 3};
let s2 = Set#{3, 4, 5};
let sr = Set.union(s1, s2);
```

Since `Set`s are `SemiGroup`s, we can also use the `++` operator and write `s1
++ s2`. 

## Maps

