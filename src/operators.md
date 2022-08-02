# Operators

Flix has a number of built-in unary and infix operators.
In addition Flix supports infix function application by enclosing
the function name in backticks. For example:

```flix
123 `sum` 456
```
is equivalent to the normal function call:

```flix
sum(123, 456)
```

In addition, a function named with an operator name (some combination of `+`, `-`, `*`, `<`, `>`, `=`, `!`, `&`, `|`, `^`, and `$`) can also be used infix. For example:

```flix
def <*>(x: Int32, y: Int32): Int32 = ???
```

can be used as follows:

```flix
1 <*> 2
```

## Precedence

1. Unary operators (`+`, `-`, `~~~`, and `not`)
1. User-defined operators (including operators defined in the standard library such as `|>`)
1. Functions applied infix with backticks
1. Composition (`<+>`)
1. Multiplicative (`**`, `*`, `/`, `mod`, and `rem`)
1. Additive (`+` and `-`)
1. Shift (`<<<` and `>>>`)
1. Comparison (`<=`, `>=`, `<`, and `>`)
1. Equality (`==`, `!=`, and `<==>`)
1. Bitwise And (`&&&`)
1. Bitwise Xor (`^^^`)
1. Bitwise Or (`|||`)
1. Logical `and`
1. Logical `or`
1. Channel `<-`
