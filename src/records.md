# レコード

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/records.html)を参照してください。

Flix は、行多相(Row Polymorphism)で拡張可能なレコードをサポートしています。

Flix のレコードはイミュータブル(不変)です（ただし、内部にミュータブルな参照セルを持つことはできます）。

## レコードリテラル

レコードリテラルは波括弧を使って記述します。

```flix
{ x = 1, y = 2 }
```

これは次のレコード型を持ちます。
`{ x = Int32, y = Int32 }`。

レコード内のラベルの順序は問いません。したがって上記のレコードは、次のものと等価です。

```flix
{ y = 2, x = 1 }
```

これは型 `{ y = Int32, x = Int32 }` を持ちます。この型は `{ x = Int32, y =
Int32 }` と等価です。言い換えると、レコード型におけるラベルの順序は問わないということです。

## ラベルアクセス

ハッシュ記号を使って、レコードのラベルにアクセスできます。

```flix
let p = { x = 1, y = 2 };
p#x + p#y
```

型システムによって、存在しないラベルにはアクセスできないことが保証されます。

レコードはイミュータブルです。いったん構築されると、レコードのラベルの値を変更することはできません。

## ラベルの更新

レコードはイミュータブルですが、ラベルの値を更新した新しいレコードを構築することはできます。

```flix
let p1 = { x = 1, y = 2 };
let p2 = { x = 3 | p1 };
p1#x + p2#x
```

式 `{ x = 3 | p1 }` は、レコード `p1` の `x` ラベルを新しい値で更新します。ラベルの更新には、そのラベルがレコード上に存在していることが必要である点に注意してください。レコードは新しいラベルで*更新*することはできませんが、後ほど見るように、新しいラベルで*拡張*することはできます。

## レコードの拡張

既存のレコードに新しいラベルを追加するには、次のようにします。

```flix
let p1 = { x = 1, y = 2 };
let p2 = { +z = 3 | p1 };
p1#x + p1#y + p2#z
```

ここで式 `{ +z = 3 | p1 }` は、レコード `p1` を新しいラベル `z` で拡張し、その結果は `x`、`y`、`z` の3つのラベルを持ちます。これらはすべて `Int32` 型です。

## レコードの制限

レコードの拡張と同様に、レコードからラベルを取り除くこともできます。

```flix
let p1 = { x = 1, y = 2 };
let p2 = { -y | p1 };
```

ここでレコード `p2` は、`y` ラベルが取り除かれている点を除いて、`p1` と同じラベルを持ちます。

## 行多相

関数は、2つのラベルを持つレコードを要求すると指定できます。

```flix
def f(r: {x = Int32, y = Int32}): Int32 = r#x + r#y
```

この関数はレコード `{ x = 1, y = 2 }` や `{ y = 2, x = 1 }` で呼び出せますが、レコード `{ x = 1, y = 2, z = 3 }` では呼び出せ*ません*。`f` のシグネチャは `x` と `y` という*ちょうど*2つのラベルを持つレコードを要求するからです。このとき、レコード `r` は*閉じている(closed)*といいます。

行多相を使うことで、この制約を緩和できます。

```flix
def g(r: {x = Int32, y = Int32 | s}): Int32 = r#x + r#y
```

この関数は、`Int32` 型の `x` と `y` ラベルを持ってさえいれば、*任意の*レコードで呼び出せます。このとき、`r` のレコード型は*開いている(open)*といいます。

## 名前付きパラメータ

関数が同じ型の複数のパラメータを持つ場合、正しい引数の順序が分からなくなりがちです。例えば、`String.contains("Hello","Hello World")` は何を返すでしょうか？ `String.contains("Hello World", "Hello")` は何を返すでしょうか？

この問題に対するよくある解決策が、*名前付きパラメータ(named parameters)*を使うことです。Flix はレコードを基盤とした名前付きパラメータの一形態をサポートしています。例えば、ある言語から別の言語へ翻訳する関数 translate を次のように書けます。

```flix
def translate(src: {src = Language}, dst: {dst = Language}, text: String): String = ???
```

この関数は次のように呼び出せます。

```flix
translate({src = English}, {dst = French}, "Where is the library?")
```

このような冗長な書き方は煩雑になるため、次の糖衣構文を使うこともできます。

```flix
translate(src = English, dst = French, "Where is the library?")
```

これは上記と等価です。

<!--
# Records

Flix supports row polymorphic extensible records.

Flix records are immutable (but may contain mutable reference cells).

## Record Literals

A record literal is written with curly braces:

```flix
{ x = 1, y = 2 }
```

which has the record type
`{ x = Int32, y = Int32 }`.

The order of labels in a record does not matter. Hence the above record is
equivalent to:

```flix
{ y = 2, x = 1 }
```

which has type `{ y = Int32, x = Int32 }`. This type is equivalent to `{ x =
Int32, y = Int32 }`. In other words, the order of labels within a record type
does not matter.

## Label Access

We can access the label of a record using a hash:

```flix
let p = { x = 1, y = 2 };
p#x + p#y
```

The type system ensures that we cannot access a label that does not exist.

Records are immutable. Once constructed, the values of the record labels cannot
be changed.

## Label Update

While records are immutable, we can construct a new
record with an updated label value:

```flix
let p1 = { x = 1, y = 2 };
let p2 = { x = 3 | p1 };
p1#x + p2#x
```

The expression `{ x = 3 | p1 }` updates the record `p1` with a new value of its
`x` label. Note that updating a label requires that the label exists on the
record. A record cannot be *updated* with a new label, but it can be *extended*
with a new label, as we shall see later.

## Record Extension

We can add a new label to an existing record as follows:

```flix
let p1 = { x = 1, y = 2 };
let p2 = { +z = 3 | p1 };
p1#x + p1#y + p2#z
```

Here the expression `{ +z = 3 | p1 }` extends the record `p1` with a new label
`z` such that the result has three labels: `x`, `y`, and `z` all of which are of
`Int32` type.

## Record Restriction

Similarly to record extension, we can also remove a label from a record:

```flix
let p1 = { x = 1, y = 2 };
let p2 = { -y | p1 };
```

Here the record `p2` has the same labels as `p1` except that the `y` label has
been removed.

## Row Polymorphism

A function may specify that it requires a record with two labels:

```flix
def f(r: {x = Int32, y = Int32}): Int32 = r#x + r#y
```

We can call this function with the records `{ x = 1, y = 2 }` and `{ y = 2, x =
1 }`, but we *cannot* call it with the record `{ x = 1, y = 2, z = 3 }` since
the signature of `f` demands a record with *exactly* two labels: `x` and `y`. We
say that the record `r` is *closed*.

We can lift this restriction by using row polymorphism:

```flix
def g(r: {x = Int32, y = Int32 | s}): Int32 = r#x + r#y
```

We can call this function with *any* record as long as it has `x` and `y` labels
which are of type `Int32`. We say that the record type of `r` is *open*.

## Named Parameters

When a function has multiple parameters that share the same type, it is easy to
get confused about the right argument order. For example, what does
`String.contains("Hello","Hello World")` return? What does
`String.contains("Hello World", "Hello")` return?

A common solution to this problem is to use *named parameters*. Flix supports a
form of named parameters building on records. For example, we can write a
function translate to translate from one language to another as follows:

```flix
def translate(src: {src = Language}, dst: {dst = Language}, text: String): String = ???
```

We can call this function as follows:

```flix
translate({src = English}, {dst = French}, "Where is the library?")
```

Since such verbosity gets tedious, we can also use the syntactic sugar:

```flix
translate(src = English, dst = French, "Where is the library?")
```

which is equivalent to the above.
-->
