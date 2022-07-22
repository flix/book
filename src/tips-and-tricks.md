# Tips & Tricks

This page documents a few features that make Flix
code easier to read and write.



## Pipelines

Flix supports the pipeline operator `|>` which is
simply a prefix version of function application (i.e.
the argument appears before the function).

The pipeline operator can often be used to make
functional code more readable.
For example:

```flix
let l = 1 :: 2 :: 3 :: Nil;
l |>
List.map(x -> x * 2) |>
List.filter(x -> x < 4) |>
List.count(x -> x > 1)
```

Here is another example:

```flix
"Hello World" |> String.toUpperCase |> println
```

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

## Infix Application

Flix supports infix function application by enclosing
the function name in backticks.
For example:

```flix
123 `sum` 456
```

is equivalent to the normal function call:

```flix
sum(123, 456)
```


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

#### DesignNote

This feature is experimental and subject to change.

## `bug!` and `unreachable!`

Flix supports two special "functions": `bug!` and
`unreachable!` that can be used to indicate when an
internal program invariant is broken and execute
should abort.
For example:

```flix
match o {
    case Some(x) => ...
    case None    => bug!("The value of `o` cannot be empty.")
}
```

As another example:

```flix
match k {
    case n if n == 0 => ...
    case n if n >= 0 => ...
    case n if n <= 0 => ...
    case n           =>  unreachable!()
}
```

Use of `bug!` and `unreachable!` should be avoided
whenever possible.

## Type Ascriptions

While Flix supports local type inference, it can
sometimes be useful to annotate an expression or a
let-binding with its type.
We call such annotations *type ascriptions*.
A type ascription cannot change the type of an
expression nor can it be used to violate type safety.

A type ascription can be placed after an expression:

```flix
("Hello" :: "World" :: Nil) : List[String]
```

and it can also be placed on a let-binding:

```flix
let l: List[String] = "Hello" :: "World" :: Nil
```
