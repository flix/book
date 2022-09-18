# Redundancy

The Flix compiler is aggressive in rejecting suspiciously looking code with unused elements.

In particular, the Flix compiler will reject code with:

- Unused local variables.
- Useless expressions.
- Unused non-unit values.

Flix rejects such programs to help programmers avoid bugs.

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

If the result of an impure expression is truly not needed, the `discard` expression can be used:

```flix
def main(): Unit \ IO =
    discard File.creationTime("foo.txt");
    println("Hello World!")
```

which a non-Unit result to be thrown away as long as the expression itself is non-pure.
