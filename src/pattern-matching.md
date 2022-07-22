# Pattern Matching

## Let Pattern Match

In addition to the pattern `match` construct, a
let-binding can be used to destruct a value.
For example:

```flix
let (x, y, z) = (1, 2, 3)
```

Binds the variables `x`, `y`, and `z` to the values
`1`, `2`, and `3`, respectively.

Any exhaustive pattern may be used in a let-binding.
For example:

```flix
let (x, Foo(y, z)) = (1, Foo(2, 3))
```

is legal provided that the `Foo` constructor belongs
to a type where it is the only constructor.

The following let-bindings are *illegal* because they
are not exhaustive:

```flix
let (1, 2, z) = ...
let Some(x) = ...
```

The Flix compiler will reject such non-exhaustive
patterns.

## Match Lambdas

Pattern matches can also be used with lambda
expressions.
For example:

```flix
List.map(match (x, y) -> x + y, (1, 1) :: (2, 2) :: Nil)
```

is equivalent to:

```flix
List.map(w -> match w { case (x, y) => x + y }, (1, 1) :: (2, 2) :: Nil)
```

As for let-bindings, such pattern matches must be
exhaustive.

Note the difference between the two lambda expressions:

```flix
let f = (x, y, z) -> x + y + z + 42i32
let g = match (x, y, z) -> x + y + z + 42i32
```

Here `f` is a function that expects *three* `Int32`
arguments,whereas `g` is a function that expects *one*
three tuple `(Int32, Int32, Int32)` argument.

## Let* (Do-notation)

Flix supports a feature similar to *do-notation* in
Haskelland *for-comprehensions* in Scala.

The following monadic code:

```flix
use Option.flatMap;
let o1 = Some(21);
let o2 = Some(42);
flatMap(x -> flatMap(y -> Some(x + y), o2), o1)
```

May be expressed more concisely as:


```flix
use Option.flatMap;
let* o1 = Some(21);
let* o2 = Some(42);
Some(o1 + o2)
```

where each `let*` corresponds to a `flatMap` use.
