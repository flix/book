# リスト

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/lists.html)を参照してください。

List(リスト)は、`Nil` と書かれる空のリストか、
もしくは `x :: xs` と書かれる cons cell(コンスセル)のいずれかです。
ここで `x` は先頭の要素、`xs` はリストの残り（末尾）を表します。
`List` 型は多相的なので、整数のリスト（`List[Int32]` と書きます）や、
文字列のリスト（`List[String]` と書きます）を作ることができます。

空のリストは次のように書きます。

```flix
Nil
```

`"Hello"` と `"World"` という文字列を要素に持つ文字列のリストは、
次のように構築できます。

```flix
"Hello" :: "World" :: Nil
```

あるいは、次の記法を使うこともできます。

```flix
List#{"Hello", "World"}
```

リストに対しては、さまざまな便利な操作を行えます。

たとえば、リストの長さは次のように計算できます。

```flix
List.length(1 :: 2 :: 3 :: Nil)
```

リストの要素の順序を反転させることもできます。

```flix
List.reverse(1 :: 2 :: 3 :: Nil)
```

2 つのリストは、`List.append` 関数を使って次のように連結できます。

```flix
let xs = (1 :: 2 :: 3 :: Nil);
let ys = (4 :: 5 :: 6 :: Nil);
List.append(xs, ys)
```

あるいは、組み込みの連結演算子 `:::` を使って次のように書くこともできます。

```flix
let xs = (1 :: 2 :: 3 :: Nil);
let ys = (4 :: 5 :: 6 :: Nil);
xs ::: ys
```

Flix には、リストを操作するための関数が豊富に用意されています。

以下は、よく使われるものの一部です。

```flix
List.count(x -> x == 1, 1 :: 2 :: 3 :: Nil);
List.filter(x -> x == 1, 1 :: 2 :: 3 :: Nil);
List.map(x -> x + 1, 1 :: 2 :: 3 :: Nil);
List.foldLeft((x, y) -> x + y, 0, 1 :: 2 :: 3 :: Nil)
```

さらに、少し変わった関数もあります。

```flix
List.intersperse("X", "a" :: "b" :: "c" :: Nil)
```

これは、リストのすべての要素の間に `"X"` を挿入します。

```flix
let l1 = "X" :: "Y" :: Nil;
let l2 = ("a" :: "b" :: Nil) :: ("c" :: "d" :: Nil) :: Nil;
List.intercalate(l1, l2)
```

これは、リスト `l2` のすべての要素の間に、リスト `l1` を挿入します。

リストを操作する再帰関数を、自分で書くこともできます。

たとえば、`map` 関数の実装は次のようになります。

```flix
///
/// `l` のすべての要素に `f` を適用した結果を返します。
/// すなわち、結果は `f(x1) :: f(x2) :: ...` という形になります。
///
pub def map(f: a -> b \ ef, l: List[a]): List[b] \ ef = match l {
    case Nil     => Nil
    case x :: xs => f(x) :: map(f, xs)
}
```

<!--
# Lists

A list is either the empty list, written as `Nil`,
or a cons cell, written as `x :: xs` where `x` is
the head element and `xs` is the tail of the list.
The `List` type is polymorphic so you can have a
list of integers, written as `List[Int32]`, or a
list of strings written as `List[String]`.

We write the empty list as follows:

```flix
Nil
```

We can construct a list of strings with the strings
`"Hello"` and `"World"` as follows:

```flix
"Hello" :: "World" :: Nil
```

or using the following notation:

```flix
List#{"Hello", "World"}
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
-->
