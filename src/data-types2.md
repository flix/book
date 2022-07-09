# Primitive Types

Flix supports the usual primitive types:

| Type    | Syntax                                  | Description                      |
|:-------:|:---------------------------------------:|:--------------------------------:|
| Unit    | `()`                                    | The unit value.                  |
| Bool    | `true`, `false`                         | A boolean value.                 |
| Char    | `'a'`, `'b'`, `'c'`                     | A character value.               |
| Float32 | `0.0f32`, `21.42f32`, `-21.42f32`       | A 32-bit floating point integer. |
| Float64 | `0.0f64`, `21.42f64`, `-21.42f64`       | A 64-bit floating point integer. |
| Int8    | `0i8`, `1i8`, `-1i8`, `127i8`, `-128i8` | A signed 8-bit integer.          |
| Int16   | `0i16`, `123i16`, `-123i16`             | A signed 16-bit integer.         |
| Int32   | `0i32`, `123i32`, `-123i32`             | A signed 32-bit integer.         |
| Int64   | `0i64`, `123i64`, `-123i64`             | A signed 64-bit integer.         |
| String  | `"hello"`, `"world"`                    | A string value.                  |
| BigInt  | `0ii`, `123ii`, `-123ii`                | An arbitrary precision integer.  |

`Float64` and `Int32` values can be
written without suffix, i.e. `123.0f64` can simply be written
as `123.0` and `123i32` can be written as `123`.

