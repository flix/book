# 列挙型

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/enums.html)を参照してください。

## 列挙型 (Enumerated Types)

列挙型は、有限個（列挙可能）の値を持つ型を定義するために使われます。列挙型は、方角、トランプの札、曜日などをモデル化するのに便利です。

例えば、以下は曜日の列挙です：

```flix
enum Weekday {
    case Monday,
    case Tuesday,
    case Wednesday,
    case Thursday,
    case Friday,
    case Saturday,
    case Sunday
}
```

ここで `Monday`、`Tuesday` などは enum の*コンストラクタ*と呼ばれます。

曜日は `Monday` または `Weekday.Monday` のように参照できます。後者は、似た名前のコンストラクタを持つ複数の enum がスコープ内にある場合に必要になります。

パターンマッチングを使って enum 値を分解できます。例えば：

```flix
enum Animal {
    case Cat,
    case Dog,
    case Giraffe
}

def isTall(a: Animal): Bool = match a {
    case Animal.Cat        => false
    case Animal.Dog        => false
    case Animal.Giraffe    => true
}
```

`isTall` 関数は `Animal` 型の値を受け取り、それに対してパターンマッチを行います。値が `Giraffe` の場合、関数は `true` を返します。そうでなければ `false` を返します。

Flix はパターンマッチが網羅的であること、つまりすべてのケースがカバーされていることを保証します。パターンマッチが非網羅的である場合はコンパイル時エラーになります。パターンマッチは、最後のケースとしてデフォルトケースを追加することで、常に網羅的にできます。デフォルトケースはアンダースコアを使って `case _ => ???` と書きます。

## 再帰型 (Recursive Types)

再帰型は、自己参照的な型を定義するために使われます。

例えば、整数の二分木は以下のように定義できます：

```flix
enum Tree {
    case Leaf(Int32),
    case Node(Tree, Tree)
}
```

木は `Int32` の値を持つ `Leaf` か、左右のサブツリーを持つ内部ノード `Node` のいずれかです。`Tree` の定義は自分自身を参照していることに注意してください。

パターンマッチングを使って、そのような木に含まれるすべての整数の合計を計算する関数を書くことができます：

```flix
def sum(t: Tree): Int32 = match t {
    case Tree.Leaf(x)    => x
    case Tree.Node(l, r) => sum(l) + sum(r)
}
```

`sum` 関数は木の値に対してパターンマッチを行います。木が葉である場合、その値をそのまま返します。そうでなければ、関数は両方のサブツリーに対して再帰的に呼び出し、その結果を加算します。

## 多相型 (Polymorphic Types)

多相型は、他の型によってパラメータ化された型です。例えば、以下のように書けます：

```flix
enum Bottle[a] {
    case Empty,
    case Full(a)
}

def isEmpty(b: Bottle[a]): Bool = match b {
    case Bottle.Empty   => true
    case Bottle.Full(_) => false
}
```

ここで `Bottle` 型は型パラメータ `a` によってパラメータ化されています。Flix では、型パラメータは通常のパラメータと同様に、常に小文字で書きます。`Bottle` 型には2つのケースがあります。ボトルが空である（値を含まない）か、満たされている（型 `a` の値を1つ含む）かのいずれかです。`isEmpty` 関数は、型 `a` でパラメータ化されたボトルを受け取り、そのボトルが空かどうかを判定します。

注意深い読者は、`Bottle` がより広く知られている `Option` 型と等価であることに気づいたかもしれません。

一般に、多相型は複数の型引数を持つことができます。例えば、標準ライブラリの `Result` の実装には2つの型パラメータがあります：

```flix
enum Result[e, t] {
    case Ok(t),
    case Err(e)
}
```

## 省略形の Enum 構文

典型的な enum は以下のような形をしています：

```flix
enum Weekday {
    case Monday,
    case Tuesday,
    case Wednesday,
    case Thursday,
    case Friday,
    case Saturday,
    case Sunday
}
```
同じ enum は以下のようにも宣言できます：

```flix
enum Weekday {
    case Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
}
```

この省略形の構文は常に利用可能ですが、単純な enum にのみ使うべきです。

## シングルトン Enum 構文

単一ケースの enum：

```flix
enum USD {
  case USD(Int32)
}
```

は以下のように短縮できます：

```flix
enum USD(Int32)
```

<!--
# Enums

## Enumerated Types

Enumerated types are used to define a type that has
a finite (enumerated) set of values.
Enumerated types are useful for things such as
modeling compass directions, the cards in a deck,
and the days in a week.

For example, here is an enumeration of the days in a
week:

```flix
enum Weekday {
    case Monday,
    case Tuesday,
    case Wednesday,
    case Thursday,
    case Friday,
    case Saturday,
    case Sunday
}
```

Here `Monday`, `Tuesday` and so on are referred to as
the *constructors* of the enum.

We can refer to a weekday as `Monday` or
`Weekday.Monday`.
The latter is required if we have multiple enums in
scope with similarly named constructors.

We can use pattern matching to destruct an enum
value.
For example:

```flix
enum Animal {
    case Cat,
    case Dog,
    case Giraffe
}

def isTall(a: Animal): Bool = match a {
    case Animal.Cat        => false
    case Animal.Dog        => false
    case Animal.Giraffe    => true
}
```

The function `isTall` takes a value of type `Animal`
and performs a pattern match on it.
If the value is `Giraffe` the function returns
`true`.
Otherwise it returns `false`.

Flix guarantees that pattern matches are exhaustive,
i.e. that all cases have been covered.
It is a compile-time error if a pattern match is
non-exhaustive.
A pattern match can always be made exhaustive by
adding a default case as the last case.
A default case is written with an underscore
`case _ => ???`.

## Recursive Types

Recursive types are used to define types that are
self-referential.

For example, we can define a binary tree of integers
as follows:

```flix
enum Tree {
    case Leaf(Int32),
    case Node(Tree, Tree)
}
```

A tree is either a `Leaf` with an `Int32` value or an
internal `Node` with a left and a right sub-tree.
Note that the definition of `Tree` refers to itself.

We can write a function, using pattern matching, to
compute the sum of all integers in such a tree:

```flix
def sum(t: Tree): Int32 = match t {
    case Tree.Leaf(x)    => x
    case Tree.Node(l, r) => sum(l) + sum(r)
}
```

The `sum` function pattern matches on a tree value.
If the tree is a leaf its value is simply returned.
Otherwise the function recurses on both subtrees and
adds their results.

## Polymorphic Types

Polymorphic types are types parameterized by other
types.
For example, we can write:

```flix
enum Bottle[a] {
    case Empty,
    case Full(a)
}

def isEmpty(b: Bottle[a]): Bool = match b {
    case Bottle.Empty   => true
    case Bottle.Full(_) => false
}
```

Here the `Bottle` type is parameterized by the type
parameter `a`.
In Flix, type parameters, like ordinary parameters
are always written in lowercase.
The `Bottle` type has two cases: either the bottle
is empty (and contains no value) or it is full (and
contains one value of type `a`).
The `isEmpty` function takes a bottle, type
parameterized by `a`, and determines if the bottle
is empty.

The careful reader might have noticed that `Bottle`
is equivalent to the more well-known `Option` type.

In general, polymorphic types can have more than one
type argument.
For example, the standard library implement of the
`Result` has two type parameters:

```flix
enum Result[e, t] {
    case Ok(t),
    case Err(e)
}
```

## Shorthand Enum Syntax

A typical enum may look like:

```flix
enum Weekday {
    case Monday,
    case Tuesday,
    case Wednesday,
    case Thursday,
    case Friday,
    case Saturday,
    case Sunday
}
```
The same enum can also be declared as:

```flix
enum Weekday {
    case Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
}
```

This shorthand syntax is always available, but should
only be used for simple enums.

## Singleton Enum Syntax

An enum with a single case:

```flix
enum USD {
  case USD(Int32)
}
```

can be shortened to:

```flix
enum USD(Int32)
```
-->
