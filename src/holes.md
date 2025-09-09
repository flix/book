## Anonymous and Named Holes

During development, Flix encourages the use of holes for incomplete code. For
example:

```flix
def sum(x: Int32, y: Int32): Int32 = ???
```

The triple question marks `???` represents an anonymous hole and can be used
wherever an expression is expected. In the above code, `???` represents a
missing function body, but it can also be used inside an expression. For
example:

```flix
def length(l: List[a]): Int32 = match l {
    case Nil     => 0
    case x :: xs => ???
}
```

When a program has multiple holes, it can be useful to name them. For example:

```flix
def length(l: List[a]): Int32 = match l {
    case Nil     => ?base
    case x :: xs => ?step
}
```

Flix requires that each named hole has a unique name.


### Variable Holes and Auto-Completion

Flix has support for a special _variable hole_ which enables type-driven
auto-completion suggestions. For example, in the program:

```flix
def main(): Unit \ IO = 
    let s: String = "Hello World";
    let n: Int32 = s?;
    println("The length of ${s} is ${n}!")
```

If we place the cursor on `s?` and ask for auto-completion suggestions, Flix
will suggest:

- `String.length(s: String): Int32`
- `String.countSubstring(substr: {substr: String}, s: String): Int32`
- `String.levenshtein(s: String, t: String): Int32`
- ...

since these are functions that can convert a `String` to an `Int32`.

As another example, in the program:

```flix
def main(): Unit \ IO = 
    let l: List[Int32] = List.range(1, 10);
    let n: Int32 = l?;
    println("The value of `n` is ${n}.")
```

If we place the cursor on `l?`, Flix will suggest:

- `List.product(l: List[Int32]): Int32`
- `List.sum(l: List[Int32]): Int32`
- `List.fold(l: List[Int32]): Int32`
- `List.length(l: List[Int32]): Int32`
- `List.count(f: a -> Bool \ ef, l: List[a]): a \ ef`
- ...

since these are functions that can convert a `List[Int32]` to an `Int32`.
