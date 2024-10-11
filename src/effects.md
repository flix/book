# Effect System

The Flix type and effect system separates pure and
impure expressions.
A pure expression is guaranteed to be referentially
transparent.
A pure function always returns the same value when
given the same argument(s) and cannot have any
(observable) side-effects.

For example, the following expression is of type
`Int32` and is pure (marked with `\ {}`):

```flix
1 + 2 : Int32 \ {}
```

whereas the following expression is impure (marked with `\ IO`):

```flix
println("Hello World") : Unit \ IO
```
