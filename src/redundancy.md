# Redundancy

The Flix compiler is aggressive in rejecting suspiciously looking code with unused elements.

In particular, the Flix compiler will reject code with:

- Unused local variables.
- Useless expressions.

## Unused Local Variables

The following program, where the variable `y` is unused, is rejected by Flix:

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
