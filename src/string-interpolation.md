# String Interpolation

Flix strings support interpolation. Inside a string, the form `"${e}"` evaluates
`e` to a value and converts it to a string using the `ToString` trait. For
example:

```flix
let fstName = "Lucky";
let lstName = "Luke";
"Hello Mr. ${lstName}. Do you feel ${fstName}, punk?"
```

String interpolation works for any type that implements a `ToString` instance.
For example:

```flix
let i = 123;
let o = Some(123);
let l = 1 :: 2 :: 3 :: Nil;
"i = ${i}, o = ${o}, l = ${l}"
```

String interpolations may contain arbitrary expressions. For example:

```flix
let x = 1;
let y = 2;
"${x + y + 1}"
```

String interpolation is the preferred way to concatenate two strings:

```flix
let x = "Hello";
let y = "World";
"${x}${y}" // equivalent to x + y
```

String interpolation is the preferred way to convert a value to a string:

```flix
let o = Some(123);
"${o}"
```

which is equivalent to an explicit use of the `toString` function from the
`ToString` trait:

```flix
ToString.toString(o)
```

String interpolators may nest, but this is discouraged.
