# Type Casts

A *type cast* instructs the compiler that an expression has a specific type. A type cast has no semantic meaning other than subverting the Flix type system, as such, it should rarely be used. 

> **Warning️️.** *Type casts are by nature dangerous and should be used with caution!*

A Flix programmer should not normally use type casts except for Java interoperability:

- To cast a Java type to one of its super-types.
- To cast the `null` value to a nullable type.

#### Example: Safe Cast to a Super-Type

The following program fragment casts a `String` value to the `Object` type:

```flix
"Hello World" as ##java.lang.Object
```

#### Example: Safe Cast from Null to an Object-Type

The following program fragment casts the `null` value (of type `Null`) to the `String` type:

```flix
null as ##java.lang.String
```

#### Example: Unsafe Cast

The following program fragment contains an illegal cast and will trigger a `ClassCastException` at run-time:

```flix
(123, 456) as String
```
