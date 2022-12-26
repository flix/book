# Mutable Data

While Flix recommends the use of immutable data structures (such as immutable
lists, sets, and maps), mutable data structures may be useful for performance
critical code.

In Flix, the primitive mutable data types are:

- [References](./references.md)
- [Arrays](./arrays.md)

from which we can build higher-level data structures, such as mutable lists, deques, sets, and maps.

But before we can use these, we have to understand the concept of [Regions](./regions.md).
