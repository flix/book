# 型エイリアス

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/type-aliases.html)を参照してください。

型エイリアス(Type alias)は、ある型に対する短縮名を導入します。例えば：

```flix
///
/// 型 `k` のキーから型 `Result[String, v]` の値への
/// Map に対する型エイリアス
///
type alias M[k, v] = Map[k, Result[String, v]]

def foo(): M[Bool, Int32] = Map#{true => Ok(123)}
```

*型エイリアス*は新しい別個の型を定義するわけではありません。型エイリアスは単に、（通常は複雑な）型に対する構文上の短縮形に過ぎません。

Flix コンパイラは型検査の前に型エイリアスを展開します。そのため、型エラーは常に、実際の基となる型に基づいて報告されます。

> **注意:** 型エイリアスは自分自身を使って再帰的に定義することはできません。Flix コンパイラはそのような再帰的な循環を検出して報告します。

<!--
# Type Aliases

Type aliases introduces a short-hand name for a
type.
For example:

```flix
///
/// A type alias for a map from keys of type `k`
/// to values of type `Result[String, v]`
///
type alias M[k, v] = Map[k, Result[String, v]]

def foo(): M[Bool, Int32] = Map#{true => Ok(123)}
```

A *type alias* does not define a new distinct type.
Rather a type alias is simply a syntactic short-hand
for a (usually complex) type.

The Flix compiler expands type aliases before type
checking.
Consequently, type errors are always reported with
respect to the actual underlying types.

> **Note:** A type alias cannot be recursively defined in terms
> of itself. The Flix compiler will detect and report such
> recursive cycles.
-->
