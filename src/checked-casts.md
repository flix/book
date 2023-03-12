## Super Casts

The Flix type system does not natively support sub-typing. 

But, for interoperability with Java, Flix has a safe _supercast_ expression.

Consider, for example, the following program:

```flix
def main(): Unit =
    let s = "Hello World";
    let o: ##java.lang.Object = s;
    ()
```

which does not compile:

```
❌ -- Type Error --------------------------------------------------

>> Expected type: 'Object' but found type: 'String'.

4 |     let o: ##java.lang.Object = s;
                                    ^
                                    expression has unexpected type.
```

since in the Flix type system the `String` type is _not_ unifiable with the
`Object` type.

We can, however, safely _supercast_ from `String` to `Object`:

```flix
def main(): Unit =
    let s = "Hello World";
    let o: ##java.lang.Object = super_cast s;
    ()
```

We can use the the `super_cast` construct to safely upcast any Java type to one
of its super types:

```flix
let _: ##java.lang.Object       = super_cast "Hello World";
let _: ##java.lang.CharSequence = super_cast "Hello World";
let _: ##java.io.Serializable   = super_cast "Hello World";
let _: ##java.lang.Object       = super_cast null;
let _: ##java.lang.String       = super_cast null;
```
### Function Types

The `super_cast` construct does _not_ work on function types.

For example, the following will not work:

```flix
let f: Unit -> ##java.lang.Object = super_cast (() -> "Hello World")
```

because it tries to cast the function type `Unit -> String` to `String ->
Object`.

Instead, one should write:

```flix
let f: Unit -> ##java.lang.Object = (() -> super_cast "Hello World")
```

which works because it directly casts `String` to `Object`.
