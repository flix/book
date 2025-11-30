# Chains and Vectors

In addition to immutable `List`s, Flix also supports immutable `Chain`s and
`Vector`s. 

The following table illustrates the performance trade-offs between lists,
chains, and vectors:

| Operation \ Type      |   List   | Chain |  Vector  |
|-----------------------|:--------:|:-----:|:--------:|
| Find First Element    |   O(1)   |  O(n) |   O(1)   |
| Find Last Element     |   O(n)   |  O(n) |   O(1)   |
| Find Element at Index |   O(n)   |  O(n) |   O(1)   |
| Cons                  |   O(1)   |  O(n) |   O(n)   |
| Append                | O(n + m) |  O(1) | O(n + m) |

When to use `List`, `Chain`, or `Vector`?:

- The `List` data structure should be the default choice as it is simple and
  well-known.
- The `Vector` data structure is an excellent choice when the size of a
  collection is fixed and/or when fast random access is required. 
- The `Chain` data structure is more rarely used, but shines when fast appends
  are required. 

## Chains

A `Chain[t]` is an immutable linked sequence of elements. 

The `Chain[t]` data type is defined as: 

```flix
enum Chain[t] {
    case Empty
    case One(t)
    case Chain(Chain[t], Chain[t])
}
```

The data structure supports `O(1)` append because we can construct a new chain
from two existing chains using the `Chain` constructor (or more appropriately
using `Chain.append`).

We can build chains using `Chain.empty`, `Chain.singleton`, `Chain.cons`, and
`Chain.append`.

For example, we can write:

```flix
let c = Chain.cons(1, Chain.empty());
println(c)
```

which prints `Chain#{1}` when compiled and executed.

## Vectors

A `Vector[t]` is an immutable fixed-length sequence of contiguous elements of
type `t`.

Flix has support for `Vector` literals. For example, we can write:


```flix
Vector#{1, 2, 3}
```

which creates a vector of length three with the elements: 1, 2, and 3.

Vectors support fast random access with the `Vector.get` operation:

```flix
let v = Vector#{1, 2, 3};
println(Vector.get(2, v))
```

which prints `3` when compiled and executed. 

> **Warning:** Indexing into a vector beyond its bounds will panic the program. 

Vectors support many operations. For example, we can map a function over a vector:

```flix
let v = Vector#{1, 2, 3};
Vector.map(x -> x + 1, v)
```

evaluates to `Vector#{2, 3, 4}`.
