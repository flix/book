# Tips and Tricks

This page documents a few features that make Flix
code easier to read and write.

## Main

The entry point of any Flix program is the `main`
function which *must* have the signature:

```flix
def main(): Unit & Impure = ...
```

That is, the main function (i) must return `Unit`,
and (ii) must be `Impure`.

## Singleton Enums

An enum with a single case:

```flix
enum USD {
    case USD(Int32)
}
```

can simply be expressed as:

```flix
enum USD(Int32)
```

The same syntax works with type class derivation:

```flix
enum USD with Eq, Order, ToString {
    case USD(Int32)
}
```

can be expressed as:

```flix
enum USD(Int32) with Eq, Order, ToString
```

## Type Casts

A cast subverts the type system by changing the type
of an expression.
Casts are by their nature dangerous and should be
used with caution.
If possible a region should be used instead.

The following cast changes the type of an expression
and triggers a ClassCastException at run-time:

```flix
(123, 456) as String
```

A cast can also change the effect of an expression.
Such casts are safer, but should still be used with
caution.

For example, we can cast an impure expression to a
pure expression:

```flix
println("Hello World") as Unit & Pure
```

As a short-hand, we can simply write:

```flix
println("Hello World") as & Pure
```

Casting an impure expression to a pure expression is
safe if the expression respects equational reasoning.
