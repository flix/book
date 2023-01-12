## Sets and Maps

Flix has excellent support for (immutable) `Set`s and `Map` based on balanced
trees; hence the elements of a `Set` and the keys of `Map` must implement the
`Order` type class. 

> **Tip:** The Flix `Set` and `Map` data structures will automatically
> parallelize certain operations. Such operations are marked with
> `@ParallelWhenPure` in the API docs. 

### Sets

The empty set is written as:

```flix
Set#{}
```

which is equivalent to `Set.empty()`. A set literal is written as:

```flix
Set#{1, 2, 3}
```

We can insert into a set using `Set.insert` (which returns a new set):

```flix
let s1 = Set#{1, 2, 3};
let s2 = Set.insert(4, s1);
```

We can determine if a set contains an element using `Set.memberOf`:

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

### Maps

The empty map is written as:

```flix
Map#{}
```

which is equivalent to `Map.empty()`. A map literal is written as:

```flix
Map#{"a" => 1, "b" => 2, "c" => 3}
```

We can insert into a map using `Map.insert` (which returns a new map):

```flix
let m1 = Map#{"a" => 1, "b" => 2, "c" => 3};
let m2 = Map.insert("d", 4, m1);
```

We can lookup the value associated with a key using `Map.get`:

```flix
let m = Map#{"a" => 1, "b" => 2, "c" => 3};
Map.get("b", m) 
```

The `Map.get` function returns an `Option[v]`.

We can merge two maps using one of `Map.unionWith` and `Map.unionWithKey`
functions.

