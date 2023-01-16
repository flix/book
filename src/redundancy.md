## Redundancy

The Flix compiler aggressively rejects programs that contain unused elements.
The idea is to help programmers avoid subtle bugs[^1]. While this can take some
time getting used to, we believe the trade-off is worth it.

Specifically, the Flix compiler will ensure that a program does not have:

- [Unused local variables](#unused-local-variables): local variables that are declared, but never used. 
- [Shadowed local variables](#shadowed-local-variables): local variables that shadow other local variables.
- [Useless expressions](#useless-expressions): pure expressions whose values are discarded.
- [Must use values](#must-use-values): expressions whose values are unused but their type is marked as `@MustUse`.

### Unused Local Variables

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

### Shadowed Local Variables

Flix rejects programs with shadowed variables.

For example, the following program is rejected:

```flix
def main(): Unit \ IO = 
    let x = 123;
    let x = 456;
    println("The value of x is ${x}.")
```

with the message:

```
❌ -- Redundancy Error -------------------------------------------------- Main.flix

>> Shadowed variable 'x'.

3 |     let x = 456;
            ^
            shadowing variable.

The shadowed variable was declared here:

2 |     let x = 123;
            ^
            shadowed variable.
```



### Useless Expressions

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

### Must Use Values

Flix rejects programs with expressions whose values are discarded but where
their type is marked with the `@MustUse` annotation. Function types, and the
`Result` and `Validation` types from the Flix Standard Library are marked as
`@MustUse`.

For example, the following program is rejected:

```flix
def main(): Unit \ IO =
    File.creationTime("foo.txt");
    println("Hello World!")
```

with the message:

```
❌ -- Redundancy Error -------------------------------------------------- Main.flix

>> Unused value but its type is marked as @MustUse.

2 |     File.creationTime("foo.txt");
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        unused value.

The expression has type 'Result[String, Int64]'
```

Even though `File.creationTime` has a side-effects, we should probably be using the result `Result[String, Int64]`.
At least to ensure that the operation was successful. 

If the result of an impure expression is truly not needed, then the `discard` expression can be used:

```flix
def main(): Unit \ IO =
    discard File.creationTime("foo.txt");
    println("Hello World!")
```

which permits a `@MustUse` value to be thrown away as long as the expression is non-pure.

[^1] See e.g. [Using Redundancies to Find Errors](https://dl.acm.org/doi/abs/10.1145/605466.605475).
