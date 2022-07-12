# Type Casts

A **type cast** instructs the compiler that an expression has a specific type.

> **Warning️️:** *Type casts are by nature dangerous and should be used with caution!*

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

> **Note:** A type cast should *not* be used to box or unbox primitive values. Instead use the designated Java methods. For example, `Integer.valueOf` and `Integer.intValue`.
