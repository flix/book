# Unsafe Type and Effect Casts

Flix supports both type and effects casts but they should be used with extreme
care.

A better solution is to use a compiler-checked _supercast_ or effect _upcast_
(if possible).

## Type Casts

A **type cast** instructs the compiler that an expression has a specific type.

> **Warning️️:** Type casts are very dangerous and should be used with utmost
> caution!

A Flix programmer should, under normal circumstances, never need to use a type
cast. 

#### Example: Safe Cast to a Super-Type

The expression below casts a `String` to an `Object`:

```flix
unsafe_cast "Hello World" as ##java.lang.Object
```

(Note: It is safer to use the `supercast` expression.)

#### Example: Safe Cast from Null to an Object-Type

The expression below casts the `null` value (of type `Null`) to `String`:

```flix
unsafe_cast null as ##java.lang.String
```

(Note: It is safer to use the `supercast` expression.)

#### Example: Unsafe Cast

The expression below contains an illegal cast and triggers a `ClassCastException`:

```flix
unsafe_cast (123, 456) as ##java.lang.Integer
```

#### Primitive Values and Boxing

A type cast should *not* be used to box or unbox primitive values. Instead use
the designated Java methods. For example, `Integer.valueOf` and
`Integer.intValue`.

## Effect Casts

An **effect cast** instructs the compiler that an expression has a specific effect.

> **Warning️️:** Effect casts are extremely dangerous and should be used with
> extreme caution!

A Flix programmer should, under normal circumstances, never need to use an
effect cast. In a few rare cases, which involve sub-effecting, an effect cast
may be necessary. Most of these cases can be handled by the safer `upcast`
expression.

#### Example: Safe Cast of Pure Function to Effect Polymorphic

Flix does not (yet) have sub-effecting which means that in certain rare cases it
can be necessary to manually insert a cast. For example:

```flix
def findRight(f: a -> Bool \ ef, l: List[a]): Option[a] \ ef =
    def loop(ll, k) = match ll {
        case Nil     => k()
        case x :: xs => loop(xs, () -> if (f(x)) Some(x) else k())
    };
    loop(l, () -> (unsafe_cast None as _ \ ef))
```

Here the cast `unsafe_cast None as _ \ ef` is required because otherwise the
function `() -> None` would be pure and not effect polymorphic as required.

> **Warning:** Never cast effectful expressions to pure. You have been warned.
