# Unchecked Type and Effect Casts

Flix also supports _unchecked_ type and effect casts.

## Unchecked Type Casts

An *unchecked type cast* instructs the compiler that an expression has a specific type.

> **Warning:** Type casts are very dangerous and should be used with utmost
> caution!

Flix programmers should normally never need to use an unchecked type cast.

### Example: Safe Cast to a Super-Type

The expression below casts a `String` to an `Object`:

```flix
unchecked_cast("Hello World" as ##java.lang.Object)
```

Note: It is safer to use the `checked_cast` expression.

### Example: Safe Cast from Null to an Object-Type

The expression below casts the `null` value (of type `Null`) to `String`:

```flix
unchecked_cast(null as ##java.lang.String)
```

Note: It is safer to use the `checked_cast` expression.

### Example: Unsafe Type Cast

The expression below contains an illegal cast and triggers a
`ClassCastException` at runtime:

```flix
unchecked_cast((123, 456) as ##java.lang.Integer)
```

## Effect Casts

An *unchecked effect cast* instructs the compiler that an expression has a
specific effect.

> **Warning:** Effect casts are extremely dangerous and should be used with
> extreme caution!

Flix programmers should normally never need to use an unchecked effect cast.

### Example: Unsafe Effect Cast

We can pretend an impure expression is pure:

```flix
def main(): Unit =
    unchecked_cast(println("Hello World") as _ \ {})
```

Here we call `println` which has the `IO` effect and then we explicitly, and
unsafely, cast away the effect, pretending that the expression is pure.

> **Warning:** Never cast effectful expressions to pure. You have been warned.
