# Redundancy

The Flix compiler aggressively rejects programs that contain unused elements. 
The idea is to help programmers avoid subtle bugs. While this can take some
getting use to during development, we believe in the long-run the trade-off
is worth it. 

In particular, the Flix compiler ensures that a program does not have:

- Unused local variables.
- Useless expressions.
- Unused non-unit values.

## Unused Local Variables

Flix rejects programs with unused variables.

For example, the following program is rejected:

```flix
def main(): Unit \ IO =
    let x = 123;
    let y = 456;
    println("The sum is ${x + x}")
```

with the message:

```
❌ -- Redundancy Error -------------------------------------------------- Main.flix

>> Unused local variable 'y'. The variable is not referenced within its scope.

3 |     let y = 456;
            ^
            unused local variable.
```

Unused local variables can be prefixed by an underscore `_` to supress the error.
For example, if we replace `y` by `_y` the above program compiles:

```flix
def main(): Unit \ IO =
    let x = 123;
    let _y = 456; // OK
    println("The sum is ${x + x}")
```

## Useless Expressions

Flix rejects programs with _pure_ expressions whose results are discarded.

For example, the following program is rejected:

```flix
def main(): Unit \ IO =
    123 + 456;
    println("Hello World!")
```

with the message:

```
❌ -- Redundancy Error -------------------------------------------------- Main.flix

>> Useless expression: It has no side-effect(s) and its result is discarded.

2 |     123 + 456;
        ^^^^^^^^^
        useless expression.

The expression has type 'Int32'
```

An expression that has no side-effect and whose result is unused is suspicious,
since it could just be removed from the program without changing its meaning.

## Unused Non-Unit Values

Flix rejects programs with non-Unit valued expressions whose results are discarded.

For example, the following program is rejected:

```flix
def main(): Unit \ IO =
    File.creationTime("foo.txt");
    println("Hello World!")
```

with the message:

```
❌ -- Redundancy Error -------------------------------------------------- Main.flix

>> Unused non-unit value: The impure expression value is not used.

2 |     File.creationTime("foo.txt");
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        discarded value.

The expression has type 'Result[Int64, String]'
```

Even though `File.creationTime` has a side-effects, we should probably be using the result `Result[Int64, String]`.
At least to ensure that the operation was successful. 

If the result of an impure expression is truly not needed, then the `discard` expression can be used:

```flix
def main(): Unit \ IO =
    discard File.creationTime("foo.txt");
    println("Hello World!")
```

which permits a non-Unit value to be thrown away as long as the expression is non-pure.
