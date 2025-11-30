# Checked Type and Effect Casts

The Flix type and effect system – by design – does not support sub-typing nor
sub-effecting. To work around these limitations, which are rare in practice,
Flix has two _safe_ upcast constructs: 

- A checked *type* cast: `checked_cast(exp)`, and 
- A checked *effect* cast `checked_ecast(exp)`.

> **Note:** The `checked_cast` and `checked_ecast` expressions are guaranteed to
> be _safe_. The Flix compiler will check at compile-time that every checked
> cast cannot go wrong. 

## Checked Type Casts

The following program:

```flix
def main(): Unit =
    let s = "Hello World";
    let o: ##java.lang.Object = s;
    ()
```

does not compile:

```
❌ -- Type Error --------------------------------------------------

>> Expected type: 'Object' but found type: 'String'.

4 |     let o: ##java.lang.Object = s;
                                    ^
                                    expression has unexpected type.
```

because in Flix the `String` type is _not_ a subtype of `Object`.

We can use a checked type cast to safely upcast from `String` to `Object`:

```flix
def main(): Unit =
    let s = "Hello World";
    let o: ##java.lang.Object = checked_cast(s);
    ()
```

We can use the `checked_cast` construct to safely upcast any Java type to one of
its super-types:

```flix
let _: ##java.lang.Object       = checked_cast("Hello World");
let _: ##java.lang.CharSequence = checked_cast("Hello World");
let _: ##java.io.Serializable   = checked_cast("Hello World");
let _: ##java.lang.Object       = checked_cast(null);
let _: ##java.lang.String       = checked_cast(null);
```

## Checked Effect Casts

The following program:

```flix
def hof(f: Int32 -> Int32 \ IO): Int32 \ IO = f(42)

def main(): Int32 \ IO =
    hof(x -> x + 1)
```

does not compile:

```
❌ -- Type Error --------------------------------------------------

>> Expected argument of type 'Int32 -> Int32 \ IO', but got 'Int32 -> Int32'.

4 |     hof(x -> x + 1)
            ^^^^^^^^^^
            expected: 'Int32 -> Int32 & Impure \ IO'

The function 'hof' expects its 1st argument to be of type 'Int32 -> Int32 \ IO'.

Expected: Int32 -> Int32 & Impure \ IO
  Actual: Int32 -> Int32
```

because in Flix a _pure_ function is _not_ a subtype of an impure function.
Specifically, the `hof` requires a function with the `IO` effect, but we are
passing in a pure function. 

We can use a checked effect cast to safely upcast a pure expression to an
impure expression: 

```flix
def main(): Int32 \ IO =
    hof(x -> checked_ecast(x + 1))
```

The `checked_ecast` construct allows us to pretend that `x + 1` has the `IO` effect. 

> **Note:** In Flix – as a general rule – higher-order functions should _not_
> require their function arguments to have a specific effect. Instead they
> should be effect polymorphic. 

## Function Types

Neither the `checked_cast` nor the `checked_ecast` constructs work on function types. 

For example, the following does not work:

```flix
let f: Unit -> ##java.lang.Object = checked_cast(() -> "Hello World")
```

because it tries to cast the function type `Unit -> String` to `Unit ->
Object`.

Instead, we should write:

```flix
let f: Unit -> ##java.lang.Object = (() -> checked_cast("Hello World"))
```

because it directly casts `String` to `Object`.