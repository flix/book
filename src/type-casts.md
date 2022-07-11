# Type Casts

A cast subverts the type system by changing the type
of an expression.
Casts are by their nature dangerous and should be used
with caution.

The following cast changes the type of an expression
and triggers a `ClassCastException` at run-time:

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
