# Polymorphic Types

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
