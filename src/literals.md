## Built-in Literals

Flix has built-in syntactic sugar for lists, sets, and
maps.

### List Literals

A list literal is written using the infix `::`
constructor.
For example:

```flix
1 :: 2 :: 3 :: Nil
```

which is syntactic sugar for:

```flix
Cons(1, Cons(2, Cons(3, Nil)))
```

### Set Literals

A set literal is written using the notation
`Set#{v1, v2, ...}`.
For example:

```flix
Set#{1, 2, 3}
```

which is syntactic sugar for:

```flix
Set.insert(1, Set.insert(2, Set.insert(3, Set.empty())))
```

### Map Literals

A map literal is written using the notion
`Map#{k1 => v1, k2 => v2, ...}`.
For example:

```flix
Map#{1 => "Hello", 2 => "World"}
```

which is syntactic sugar for:

```flix
Map.insert(1, "Hello", Map.insert(2, "World", Map.empty()))
```
