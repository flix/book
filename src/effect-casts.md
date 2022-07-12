# Effect Casts

An **effect cast** instructs the compiler that an expression has a specific effect.

> **Warning️️:** *Effect casts are by nature extremely dangerous and should be used with utmost caution!*

A Flix programmer should not normally use effect casts except in two cases:

- To cast an pure function to an effect polymorphic function.
- To cast a pure function to an impure function.

Both cases are legitimate and safe.

#### Example: Safe Cast of Pure Function to Effect Polymorphic

Flix does not (yet) have sub-effecting which means that in certain rare cases it 
can be necessary to manually insert a cast. For example:

```flix
pub def findRight(f: a -> Bool & ef, l: List[a]): Option[a] & ef =
    def loop(ll, k) = match ll {
        case Nil     => k()
        case x :: xs => loop(xs, () -> if (f(x)) Some(x) else k())
    };
    loop(l, () -> None as & ef)
```

Here the cast `() -> None as & ef` is required because otherwise 
the function `() -> None` would be pure and not effect polymorphic as required.

> **Warning:** Never cast effectful expression to pure. Do so at your own peril. You have been warned.
