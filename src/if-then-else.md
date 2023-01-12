## If-then-else

Flix supports the usual *if-then-else* expression:

```flix
if (1 == 1) "Hello" else "World"
```

which evaluates to `Hello`.

But `if` guards are also supported in other parts of the language.

### Guarded Pattern Matches

We can use an `if`-guard in a pattern match:

```flix
def isSquare(s: Shape): Bool = match s {
    case Rectangle(h, w) if h == w => true
    case _                         => false
}
```

### Guarded Datalog Rules

We can use an `if`-guard in a Datalog rule:

```flix
Path(x, z) :- Path(x, y), Edge(y, z), if x != z.
```
