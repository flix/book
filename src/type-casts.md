# Type Casts

A *type cast* instructs the compiler that an expression has a specific type.

**Warning️️.** *Type casts are by nature dangerous and should be used with caution!*

A Flix programmer should not normally use type casts except for Java interoperability:

- To cast a Java type to a super-type.
- To cast the `null` value to a nullable type.

### Super-type Cast Example

The following casts a `String` value to the `Object` type:

```flix
"Hello World" as ##java.lang.Object
```

### Null Cast Example

The following casts the `null` value to the `String` type:

```flix
null as ##java.lang.String
```

### Unsound Cast Example

The following cast triggers a `ClassCastException` at run-time:

```flix
(123, 456) as String
```

