# Type and Effect Casts

Flix supports both type and effects casts, but they should be used with extreme care.

A better solution is almost always to us a compiler-checked _upcast_.

## Type Casts

A **type cast** instructs the compiler that an expression has a specific type.

> **Warning️️**
>
> *Type casts are by nature dangerous and should be used with caution!*

A Flix programmer should not normally use type casts except in two cases:

- To cast a Java type to one of its super-types.
- To cast the `null` value to a nullable type.

Both use cases are legitimate and safe.

#### Example: Safe Cast to a Super-Type

The expression below casts a `String` to an `Object`:

```flix
"Hello World" as ##java.lang.Object
```

#### Example: Safe Cast from Null to an Object-Type

The expression below casts the `null` value (of type `Null`) to `String`:

```flix
null as ##java.lang.String
```

#### Example: Unsafe Cast

The expression below contains an illegal cast and triggers a `ClassCastException`:

```flix
(123, 456) as String
```

#### Primitive Values and Boxing

A type cast should *not* be used to box or unbox primitive values.
Instead use the designated Java methods.
For example, `Integer.valueOf` and `Integer.intValue`.

## Effect Casts

An **effect cast** instructs the compiler that an expression has a specific effect.

> **Warning️️**
>
> *Effect casts are by nature extremely dangerous and should be used with utmost caution!*

A Flix programmer should not normally use effect casts except in two cases:

-   To cast an pure function to an effect polymorphic function.
-   To cast a pure function to an impure function.

Both cases are legitimate and safe.

#### Example: Safe Cast of Pure Function to Effect Polymorphic

Flix does not (yet) have sub-effecting which means that in certain rare cases it
can be necessary to manually insert a cast. For example:

```flix
def findRight(f: a -> Bool \ ef, l: List[a]): Option[a] \ ef =
    def loop(ll, k) = match ll {
        case Nil     => k()
        case x :: xs => loop(xs, () -> if (f(x)) Some(x) else k())
    };
    loop(l, () -> None as \ ef)
```

Here the cast `() -> None as \ ef` is required because otherwise
the function `() -> None` would be pure and not effect polymorphic as required.

> **Warning**
>
> Never cast effectful expression to pure.
> You have been warned.
