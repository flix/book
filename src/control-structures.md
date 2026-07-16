# 制御構造

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/control-structures.html)を参照してください。

Flix は関数型プログラミング言語であるため、制御構造は多くありません。
制御のほとんどは、単なる関数適用によって行われます。Flix の制御構造は次のとおりです。

- [If-Then-Else](./if-then-else.md): 従来の if-then-else 式です。
- [Pattern Matching](./pattern-matching.md): 代数的データ型(algebraic data type)を分解するための関数型の構文です。
- [Foreach](./foreach.md): コレクションを反復処理するための命令型の構文です。
- [Monadic For-Yield](./monadic-for-yield.md): モナドの操作のための関数型の構文で、Scala の `for` 内包表記や Haskell の `do` 記法に似ています。
- [Applicative For-Yield](./applicative-for-yield.md): アプリカティブな操作のための関数型の構文で、Haskell のアプリカティブな `do` 記法に似ています。

`foreach`、モナドの `forM`、アプリカティブの `forA` の違いは何でしょうか。

次の表は、各構文の使用例を示しています。

| アクション                                                | 構文                                  |
|----------------------------------------------------------|---------------------------------------|
| コレクション内のすべての要素を出力する。                  | [Foreach](./foreach.md)               |
| コレクション内の各要素にエフェクトを伴う操作を適用する。  | [Foreach](./foreach.md)               |
| `Option` や `Result` を扱う。                            | [Monadic For-Yield](./monadic-for-yield.md) |
| `Monad` を介して `flatMap` する。                        | [Monadic For-Yield](./monadic-for-yield.md) |
| `Validation` を扱う。                                    | [Applicative For-Yield](./applicative-for-yield.md) |

> **注意:** Flix には従来の `while` ループや `for` ループはありません。代わりに、再帰や上記の構文のいずれかを使用することを推奨します。

<!--
# Control Structures

Flix — being a functional programming language — has few control-structures.
Most control is simply function application. The Flix control structures are:

- [If-Then-Else](./if-then-else.md): A traditional if-then-else expression.
- [Pattern Matching](./pattern-matching.md): A functional construct for
  taking apart algebraic data types. 
- [Foreach](./foreach.md): An imperative construct for iteration through
  collections.
- [Monadic For-Yield](./monadic-for-yield.md): A functional construct for
  monadic operations, similar to Scala's `for`-comprehensions and Haskell's
  `do`-notation.
- [Applicative For-Yield](./applicative-for-yield.md): A functional construct
  for applicative operations, similar to Haskell's applicative `do`-notation.

What's the difference between `foreach`, monadic `forM`, and applicative `forA`?:

The following table gives some uses cases for each construct:

| Action                                                        | Construct                           |
|---------------------------------------------------------------|-------------------------------------|
| Print all elements in a collection.                           | [Foreach](./foreach.md)             |
| Apply an effectful operation to each element in a collection. | [Foreach](./foreach.md)             |
| Work with `Option`s and `Result`s.                            | [Monadic For-Yield](./monadic-for-yield.md) |
| `flatMap` through a `Monad`.                                  | [Monadic For-Yield](./monadic-for-yield.md) |
| Work with `Validation`s                                       | [Applicative For-Yield](./applicative-for-yield.md) |

> **Note:** Flix does not have traditional `while` or `for`-loops. Instead, we
> recommend the use of recursion and/or one of the above constructs.
-->
