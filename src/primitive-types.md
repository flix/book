## Primitive Types

Flix supports the primitive types:

| Type         | Syntax                                   | Description                       |
|--------------|------------------------------------------|-----------------------------------|
| Unit         | `()`                                     | The unit value.                   |
| Bool         | `true`, `false`                          | A boolean value.                  |
| Char         | `'a'`, `'b'`, `'c'`                      | A character value.                |
| Float32      | `0.0f32`, `21.42f32`, `-21.42f32`        | A 32-bit floating point integer.  |
| Float64      | `0.0f64`, `21.42f64`, `-21.42f64`        | A 64-bit floating point integer.  |
| Int8         | `0i8`, `1i8`, `-1i8`, `127i8`, `-128i8`  | A signed 8-bit integer.           |
| Int16        | `0i16`, `123i16`, `-123i16`              | A signed 16-bit integer.          |
| Int32        | `0i32`, `123i32`, `-123i32`              | A signed 32-bit integer.          |
| Int64        | `0i64`, `123i64`, `-123i64`              | A signed 64-bit integer.          |
| String       | `"hello"`, `"world"`                     | A string value.                   |
| BigInt       | `0ii`, `123ii`, `-123ii`                 | An arbitrary precision integer.   |
| BigDecimal   | `0.0ff`, `123.45ff`, `-123.45ff`         | An arbitrary precision decimal.   |

`Float64` and `Int32` values can be
written without suffix, i.e. `123.0f64` can simply be written
as `123.0` and `123i32` can be written as `123`.

### Built-in Literals

Flix has built-in syntactic sugar for lists, sets, and
maps.

#### List Literals

A list literal is written using the infix `::` constructor. For example:

```flix
1 :: 2 :: 3 :: Nil
```

which is syntactic sugar for:

```flix
Cons(1, Cons(2, Cons(3, Nil)))
```

Alternatively, the same list can also be written as:

```flix
List#{1, 2, 3}
```

#### Set Literals

A set literal is written using the notation `Set#{v1, v2, ...}`. For example:

```flix
Set#{1, 2, 3}
```

which is syntactic sugar for:

```flix
Set.insert(3, Set.insert(2, Set.insert(1, Set.empty())))
```

Note that the elements are inserted from left to right, thus 1 is inserted first.

#### Map Literals

A map literal is written using the notion
`Map#{k1 => v1, k2 => v2, ...}`.
For example:

```flix
Map#{1 => "Hello", 2 => "World"}
```

which is syntactic sugar for:

```flix
Map.insert(2, "World", Map.insert(1, "Hello", Map.empty()))
```

Note that similar to sets above, the entries are inserted left to right. In particular, if multiple entries share the same key, the rightmost one overwrites the previous values.