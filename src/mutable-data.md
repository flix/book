# Mutable Data

> **Note:** This documentation is relevant for Flix version 0.35.0 or higher.

Flix is a _functional-first_ programming language that _encourages_ but does not
demand, the use of immutable data structures. While immutable data structures
should be the default, Flix has rich support for imperative programming with
destructive updates to mutable data. Notably, in Flix, all mutable memory _must_
belong to a region. 

Flix has two types of "primitive" mutable data:

- [References](./references.md)
- [Arrays](./arrays.md)

which are used to build higher-level mutable data structures, such as `MutList`,
`MutDeque`, `MutSet`, and `MutMap`. In general, these higher-level data
structures should be used instead of working directly with references and
arrays. 

Before we dive into references and arrays, we begin with a discussion of
[regions](./regions.md).
