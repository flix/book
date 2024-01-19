## Type Ascriptions

While Flix supports local type inference, it can sometimes be useful to annotate
an expression or a let-binding with its type. We call such annotations *type
ascriptions*. A type ascription cannot change the type of an expression nor can
it be used to violate type safety.

A type ascription can be placed after an expression:

```flix
("Hello" :: "World" :: Nil) : List[String]
```

and it can also be placed on a let-binding:

```flix
let l: List[String] = "Hello" :: "World" :: Nil
```
### Kind Ascriptions

Flix also supports kind ascriptions. Where a type ascription specifies the
_type_ of an _expression_, a kind ascription specifies the _kind_ of a _type_.

We can use kind ascriptions on type parameters. For example: 

```flix
def fst1[a: Type, b: Type](p: (a, b)): a = let (x, _) = p; x
```

Here we have specified that the _kind_ of the two type parameters `a` and `b` is
`Type`. We will typically never have to specify such kinds since they can
inferred. 

We can also provide kind ascriptions on algebraic data types:

```flix
enum A[t: Type] {
    case A(t, t)
}
```

and on traits:

```flix
trait MyTrait[t: Type] {
    // ...
}
```

We typically only use kind ascriptions for [higher-kinded
types](./higher-kinded-types.md).
