# Effect Casts

An *effect cast* instructs the compiler that an expression has a specific effect.

**Warning️️.** *Effect casts are by nature extremely dangerous and should be used with utmost caution!*



For example, we can cast an impure expression to a
pure expression:

```flix
println("Hello World") as Unit & Pure
```

As a short-hand, we can simply write:

```flix
println("Hello World") as & Pure
```

Casting an impure expression to a pure expression is
safe if the expression respects equational reasoning.
