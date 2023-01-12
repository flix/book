## Anonymous and Named Holes

During development, Flix encourages the use of holes
for incomplete code.
For example:

```flix
def sum(x: Int32, y: Int32): Int32 = ???
```

The triple question marks `???` represents an
anonymous hole and can be used wherever an expression
is expected.
In the above code, `???` represents a missing function
body, but it can also be used inside an expression.
For example:

```flix
def length(l: List[a]): Int32 = match l {
    case Nil     => 0
    case x :: xs => ???
}
```

When a program has multiple holes, it can be useful to
name them.
For example:

```flix
def length(l: List[a]): Int32 = match l {
    case Nil     => ?base
    case x :: xs => ?step
}
```

Flix requires that each named hole has a unique name.
