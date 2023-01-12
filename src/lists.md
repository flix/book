## Lists

The bread and butter of functional programming is
list processing.
A list is either the empty list, written as `Nil`,
or a cons cell, written as `x :: xs` where `x` is
the head element and `xs` is the tail of the list.
The `List` type is polymorphic so you can have a
list of integers, written as `List[Int32]`, or a
list of strings written as `List[String]`.
The `List` type and list operations are part of the
Flix standard library.

We write the empty list as follows:

```flix
Nil
```

We can construct a list of strings with the strings
`"Hello"` and `"World"` as follows:

```flix
"Hello" :: "World" :: Nil
```

Given a list there are many useful operations we can
perform on it.

For example, we can compute the length of a list as
follows:

```flix
List.length(1 :: 2 :: 3 :: Nil)
```

We can also reverse the order of elements in a list:

```flix
List.reverse(1 :: 2 :: 3 :: Nil)
```

We can append two lists using the `List.append`
function as follows:

```flix
let xs = (1 :: 2 :: 3 :: Nil);
let ys = (4 :: 5 :: 6 :: Nil);
List.append(xs, ys)
```

Or, alternatively, we can use the built-in append
operator `:::` as follows:

```flix
let xs = (1 :: 2 :: 3 :: Nil);
let ys = (4 :: 5 :: 6 :: Nil);
xs ::: ys
```

Flix has an extensive collection of functions to
operate on lists.

Here are some of the most common:

```flix
List.count(x -> x == 1, 1 :: 2 :: 3 :: Nil);
List.filter(x -> x == 1, 1 :: 2 :: 3 :: Nil);
List.map(x -> x + 1, 1 :: 2 :: 3 :: Nil);
List.foldLeft((x, y) -> x + y, 0, 1 :: 2 :: 3 :: Nil)
```

And here are some more exotic functions:

```flix
List.intersperse("X", "a" :: "b" :: "c" :: Nil)
```

which inserts `"X"` between every element in the
list.

```flix
let l1 = "X" :: "Y" :: Nil;
let l2 = ("a" :: "b" :: Nil) :: ("c" :: "d" :: Nil) :: Nil;
List.intercalate(l1, l2)
```

which inserts the list `l1` between every element in
the list `l2`.

We can write our own recursive functions to operate
on lists.

For example, here is an implementation of the `map`
function:

```flix
///
/// Returns the result of applying `f` to every element in `l`.
/// That is, the result is of the form: `f(x1) :: f(x2) :: ...`.
///
pub def map(f: a -> b \ ef, l: List[a]): List[b] \ ef = match l {
    case Nil     => Nil
    case x :: xs => f(x) :: map(f, xs)
}
```
