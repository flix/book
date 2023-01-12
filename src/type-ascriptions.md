## Type Ascriptions

While Flix supports local type inference, it can
sometimes be useful to annotate an expression or a
let-binding with its type.
We call such annotations *type ascriptions*.
A type ascription cannot change the type of an
expression nor can it be used to violate type safety.

A type ascription can be placed after an expression:

```flix
("Hello" :: "World" :: Nil) : List[String]
```

and it can also be placed on a let-binding:

```flix
let l: List[String] = "Hello" :: "World" :: Nil
```
