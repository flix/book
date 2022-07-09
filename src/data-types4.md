# Enumerated Types

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
