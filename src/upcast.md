# Upcast

> **Note:** This feature is experimental and not yet intended for use.

Flix does not support sub-typing nor sub-effecting.

Nevertheless, there is way to use both in a safe manner.

For example, the following program does not compile:

```flix
def main(): Unit =
    let s = "Hello World";
    let o: ##java.lang.Object = s;
    ()
```

because:

```
❌ -- Type Error --------------------------------------------------

>> Expected type: 'Object' but found type: 'String'.

4 |     let o: ##java.lang.Object = s;
                                    ^
                                    expression has unexpected type.
```

i.e. the `String` type is not the same as the `Object` type.

We can, however, safely _upcast_ from `String` to `Object`:

```flix
def main(): Unit =
    let s = "Hello World";
    let o: ##java.lang.Object = upcast s;
    ()
```

As another example, if we have a higher-order function which expects an effectful function:

```flix
def hof(f: a -> b \ IO): Unit = ???

def main(): Unit =
    hof(x -> x + 1) // Does not compile
```

We cannot pass the pure function `x -> x + 1` because `hof` expects a function with effect `IO`.

We can, however, safely upcast the pure function type `Int32 -> Int32` to `Int32 -> Int32 \ IO`:

```flix
def hof(f: a -> b \ IO): Unit = ???

def main(): Unit =
    hof(upcast (x -> x + 1))
```

which permits the program to compile.
