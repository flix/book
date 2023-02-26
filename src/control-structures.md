# Control Structures

Flix — being a functional programming language — has few control-structures.
Most control is simply function application. The Flix control structures are:

- [If-Then-Else](./if-then-else.md): A traditional if-then-else expression.
- [Pattern Matching](./pattern-matching.md): A functional construct for
  taking apart algebraic data types. 
- [Foreach](./foreach.md): An imperative construct for iteration through
  collections.
- [Foreach-Yield](./foreach-yield.md): An imperative construct for building new
  collections from existing collections.
- [Monadic For-Yield](./monadic-for-yield.md): A functional construct for
  monadic operations, similar to Scala's `for`-comprehensions and Haskell's
  `do`-notation.
- [Applicative For-Yield](./applicative-for-yield.md): A functional construct
  for applicative operations, similar to Haskell's applicative `do`-notation.

What's the difference between `foreach`, `foreach-yield`, monadic `forM`, and applicative `forA`?:

The following table gives some uses cases for each construct:

| Action                                                        | Construct                           |
|---------------------------------------------------------------|-------------------------------------|
| Print all elements in a collection.                           | [Foreach](./foreach.md)             |
| Apply an effectful operation to each element in a collection. | [Foreach](./foreach.md)             |
| Build a new collection from existing collections.             | [Foreach-Yield](./foreach-yield.md) |
| Transform the elements of a collection.                       | [Foreach-Yield](./foreach-yield.md) |
| Convert a collection of one type into another type.           | [Foreach-Yield](./foreach-yield.md) |
| Work with `Option`s and `Result`s.                            | [Monadic For-Yield](./monadic-for-yield.md) |
| `flatMap` through a `Monad`.                                  | [Monadic For-Yield](./monadic-for-yield.md) |
| Work with `Validation`s                                       | [Applicative For-Yield](./applicative-for-yield.md) |

> **Note:** Flix does not have traditional `while` or `for`-loops. Instead, we
> recommend the use recursion and/or one of the above constructs. 
