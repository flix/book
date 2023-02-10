# Immutable Data

The _bread-and-butter_ of functional programming is _immutable data types_. 

We have already seen several examples of immutable data types:

- [Primitive Types](./primitive-types.md)
- [Tuple Types](./tuples.md)
- [Enumerated, Recursive, and Polymorphic Types](./enums.md)

In addition, The Flix standard library offers several immutable data types:

- `List[t]`     : An immutable singly-linked list of elements of type `t`.
- `Chain[t]`    : An immutable chain of elements of type `t` with fast append.
- `Vector[t]`   : An immutable sequence of elements of type `t` with fast lookup.
- `Set[t]`      : An immutable set of elements of type `t`.
- `Map[k, v]`   : An immutable map of keys of type `k` to values of type `v`.

Other immutable data types include:

- `Option[t]`       : A type that is either `None` or `Some(t)`.
- `Result[e, t]`    : A type that is either `Ok(t)` or `Err(e)`.
- `Chain[t]`        : An immutable sequence of elements of type `t` that supports fast append.
- `Nel[t]`          : An immutable non-empty singly-linked list of elements of type `t`.
- `Nec[t]`          : An immutable non-empty sequence of elements of type `t` that supports fast append.
- `MultiMap[k, v]`  : An immutable map of keys of type `k` to _sets_ of values of type `v`.
