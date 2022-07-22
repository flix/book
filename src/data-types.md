# Data Types

Flix comes with a collection of built-in data types,
such as booleans, floats and integers, and
compound types, such as tuples and records.
Moreover, the standard library defines types such as
`Option[a]`, `Result[t, e]`, `List[a]`, `Set[a]`,
and `Map[k, v]`.

In addition to these types, Flix allows programmers
to define their own types, including *enumerated
types*, *recursive types*, and *polymorphic types*.

Flix also supports type aliases (new types).

## Primitive Types

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

## Tuples

A tuple is a product of values.

A tuple is written with parentheses.
For example, here is a 2-tuple (a pair) of an
`Int32` and a `Bool`:

```flix
(123, true)
```

The type of the tuple is `(Int32, Bool)`.

We can destructure a tuple using pattern matching.
For example:

```flix
let t = ("Lucky", "Luke", 42, true);
let (fstName, lstName, age, male) = t;
lstName
```

evaluates to the string `"Luke"`.

The Flix prelude defines the `fst` and `snd`
functions:

```flix
let t = (1, 2);
let x = fst(t); // x = 1
let y = snd(t)  // y = 2
```

which are useful when working with 2-tuples (i.e.
pairs).
For example:

```flix
let l = (1, 1) :: (2, 2) :: Nil; // has type List[(Int32, Int32)]
List.map(fst, l)                 // has type List[Int32]
```

which evaluates to a list that contains all the
first components of the list `l`.



