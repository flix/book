# イミュータブルなデータ

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/immutable-data.html)を参照してください。

関数型プログラミングの_要_となるのが、イミュータブル(不変)なデータ型です。

これまでにも、イミュータブルなデータ型の例をいくつか見てきました。

- [プリミティブ型](./primitive-types.md)
- [Tuple 型](./tuples.md)
- [列挙型・再帰型・多相型](./enums.md)

加えて、Flix の標準ライブラリは次のようなイミュータブルなデータ型を提供しています。

- `List[t]`     : 型 `t` の要素からなるイミュータブルな単方向リスト。
- `Chain[t]`    : 型 `t` の要素からなり、追加(append)が高速なイミュータブルなチェーン。
- `Vector[t]`   : 型 `t` の要素からなり、要素の参照(lookup)が高速なイミュータブルなシーケンス。
- `Set[t]`      : 型 `t` の要素からなるイミュータブルな Set(セット)。
- `Map[k, v]`   : 型 `k` のキーを型 `v` の値に対応づけるイミュータブルな Map(マップ)。

その他のイミュータブルなデータ型には、次のものがあります。

- `Option[t]`       : `None` または `Some(t)` のいずれかになる型。
- `Result[e, t]`    : `Ok(t)` または `Err(e)` のいずれかになる型。
- `Nel[t]`          : 型 `t` の要素からなる、空でないイミュータブルな単方向リスト。
- `Nec[t]`          : 型 `t` の要素からなり、追加(append)が高速な、空でないイミュータブルなシーケンス。
- `MultiMap[k, v]`  : 型 `k` のキーを型 `v` の値の_Set_に対応づけるイミュータブルな Map。

<!--
# Immutable Data

The _bread-and-butter_ of functional programming is _immutable data types_. 

We have already seen several examples of immutable data types:

- [Primitive Types](./primitive-types.md)
- [Tuple Types](./tuples.md)
- [Enumerated, Recursive, and Polymorphic Types](./enums.md)

In addition, The Flix standard library offers several immutable data types:

- `List[t]`     : An immutable singly-linked list of elements of type `t`.
- `Chain[t]`    : An immutable chain of elements of type `t` with fast append.
- `Vector[t]`   : An immutable sequence of elements of type `t` with fast lookup.
- `Set[t]`      : An immutable set of elements of type `t`.
- `Map[k, v]`   : An immutable map of keys of type `k` to values of type `v`.

Other immutable data types include:

- `Option[t]`       : A type that is either `None` or `Some(t)`.
- `Result[e, t]`    : A type that is either `Ok(t)` or `Err(e)`.
- `Nel[t]`          : An immutable non-empty singly-linked list of elements of type `t`.
- `Nec[t]`          : An immutable non-empty sequence of elements of type `t` that supports fast append.
- `MultiMap[k, v]`  : An immutable map of keys of type `k` to _sets_ of values of type `v`.
-->
