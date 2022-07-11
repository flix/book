# Data Types

Flix comes with a collection of built-in data types,
such as booleans, floats and integers, and
compound types, such as tuples and records.
Moreover, the standard library defines types such as
`Option[a]`, `Result[t, e]`, `List[a]`, `Set[a]`,
and `Map[k, v]`.

In addition to these types, Flix allows programmers
to define their own types, including *enumerated
types*, *recursive types*, and *polymorphic types*.

Flix also supports type aliases (new types).

## Primitive Types

Flix supports the usual primitive types:

| Type    | Syntax                                  | Description                      |
|:-------:|:---------------------------------------:|:--------------------------------:|
| Unit    | `()`                                    | The unit value.                  |
| Bool    | `true`, `false`                         | A boolean value.                 |
| Char    | `'a'`, `'b'`, `'c'`                     | A character value.               |
| Float32 | `0.0f32`, `21.42f32`, `-21.42f32`       | A 32-bit floating point integer. |
| Float64 | `0.0f64`, `21.42f64`, `-21.42f64`       | A 64-bit floating point integer. |
| Int8    | `0i8`, `1i8`, `-1i8`, `127i8`, `-128i8` | A signed 8-bit integer.          |
| Int16   | `0i16`, `123i16`, `-123i16`             | A signed 16-bit integer.         |
| Int32   | `0i32`, `123i32`, `-123i32`             | A signed 32-bit integer.         |
| Int64   | `0i64`, `123i64`, `-123i64`             | A signed 64-bit integer.         |
| String  | `"hello"`, `"world"`                    | A string value.                  |
| BigInt  | `0ii`, `123ii`, `-123ii`                | An arbitrary precision integer.  |

`Float64` and `Int32` values can be
written without suffix, i.e. `123.0f64` can simply be written
as `123.0` and `123i32` can be written as `123`.

## Tuples

A tuple is a product of values.

A tuple is written with parentheses.
For example, here is a 2-tuple (a pair) of an
`Int32` and a `Bool`:

```flix
(123, true)
```

The type of the tuple is `(Int32, Bool)`.

We can destructure a tuple using pattern matching.
For example:

```flix
let t = ("Lucky", "Luke", 42, true);
let (fstName, lstName, age, male) = t;
lstName
```

evaluates to the string `"Luke"`.

The Flix prelude defines the `fst` and `snd`
functions:

```flix
let t = (1, 2);
let x = fst(t); // x = 1
let y = snd(t)  // y = 2
```

which are useful when working with 2-tuples (i.e.
pairs).
For example:

```flix
let l = (1, 1) :: (2, 2) :: Nil; // has type List[(Int32, Int32)]
List.map(fst, l)                 // has type List[Int32]
```

which evaluates to a list that contains all the
first components of the list `l`.

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

## Type Aliases

Type aliases introduces a short-hand name for a
type.
For example:

```flix
///
/// A type alias for a map from keys of type `k`
/// to values of type `Result[v, String]`
///
type alias M[k, v] = Map[k, Result[v, String]]

def foo(): M[Bool, Int32] = Map#{true => Ok(123)}
```

A *type alias* does not define a new distinct type.
Rather a type alias is simply a syntactic short-hand
for a (usually complex) type.

The Flix compiler expands type aliases before type
checking.
Consequently, type errors are always reported with
respect to the actual underlying types.

#### Warning

A type alias cannot be recursively defined in terms
of itself.
The Flix compiler will detect and report such
recursive cycles.
