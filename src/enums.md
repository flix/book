# Enums

## Enumerated Types

Enumerated types are used to define a type that has
a finite (enumerated) set of values.
Enumerated types are useful for things such as
modeling compass directions, the cards in a deck,
and the days in a week.

For example, here is an enumeration of the days in a
week:

```flix
enum Weekday {
    case Monday,
    case Tuesday,
    case Wednesday,
    case Thursday,
    case Friday,
    case Saturday,
    case Sunday
}
```

Here `Monday`, `Tuesday` and so on are referred to as
the *constructors* of the enum.

We can refer to a weekday as `Monday` or
`Weekday.Monday`.
The latter is required if we have multiple enums in
scope with similarly named constructors.

We can use pattern matching to destruct an enum
value.
For example:

```flix
enum Animal {
    case Cat,
    case Dog,
    case Giraffe
}

def isTall(a: Animal): Bool = match a {
    case Cat        => false
    case Dog        => false
    case Giraffe    => true
}
```

The function `isTall` takes a value of type `Animal`
and performs a pattern match on it.
If the value is `Giraffe` the function returns
`true`.
Otherwise it returns `false`.

Flix guarantees that pattern matches are exhaustive,
i.e. that all cases have been covered.
It is a compile-time error if a pattern match is
non-exhaustive.
A pattern match can always be made exhaustive by
adding a default case as the last case.
A default case is written with an underscore
`case _ => ???`.

## Recursive Types

Recursive types are used to define types that are
self-referential.

For example, we can define a binary tree of integers
as follows:

```flix
enum Tree {
    case Leaf(Int32),
    case Node(Tree, Tree)
}
```

A tree is either a `Leaf` with an `Int32` value or an
internal `Node` with a left and a right sub-tree.
Note that the definition of `Tree` refers to itself.

We can write a function, using pattern matching, to
compute the sum of all integers in such a tree:

```flix
def sum(t: Tree): Int32 = match t {
    case Leaf(x)    => x
    case Node(l, r) => sum(l) + sum(r)
}
```

The `sum` function pattern matches on a tree value.
If the tree is a leaf its value is simply returned.
Otherwise the function recurses on both subtrees and
adds their results.

## Polymorphic Types

Polymorphic types are types parameterized by other
types.
For example, we can write:

```flix
enum Bottle[a] {
    case Empty,
    case Full(a)
}

def isEmpty[a](b: Bottle[a]): Bool = match b {
    case Empty   => true
    case Full(_) => false
}
```

Here the `Bottle` type is parameterized by the type
parameter `a`.
In Flix, type parameters, like ordinary parameters
are always written in lowercase.
The `Bottle` type has two cases: either the bottle
is empty (and contains no value) or it is full (and
contains one value of type `a`).
The `isEmpty` function takes a bottle, type
parameterized by `a`, and determines if the bottle
is empty.

The careful reader might have noticed that `Bottle`
is equivalent to the more well-known `Option` type.

In general, polymorphic types can have more than one
type argument.
For example, the standard library implement of the
`Result` has two type parameters:

```flix
enum Result[t, e] {
    case Ok(t),
    case Err(e)
}
```

## Shorthand Enum Syntax

A typical enum may look like:

```flix
enum Weekday {
    case Monday,
    case Tuesday,
    case Wednesday,
    case Thursday,
    case Friday,
    case Saturday,
    case Sunday
}
```
The same enum can also be declared as:

```flix
enum Weekday {
    case Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
}
```

This shorthand syntax is always available, but should
only be used for simple enums.

## Singleton Enum Syntax

An enum with a single case:

```flix
enum USD {
  case USD(Int32)
}
```

can be shortened to:

```flix
enum USD(Int32)
```
