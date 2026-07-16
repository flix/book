# ミュータブルなデータ

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/mutable-data.html)を参照してください。

Flix は _関数型ファースト（functional-first）_ なプログラミング言語であり、
immutable(イミュータブル)なデータ構造の使用を推奨しますが、必須とはしません。
immutable なデータ構造をデフォルトとすべきではありますが、Flix は
mutable(ミュータブル)なデータへの破壊的更新（destructive update）を伴う
命令型プログラミングも手厚くサポートしています。

Flix は、その effect system（エフェクトシステム）を使って、純粋（pure）な
コードと純粋でない（impure）コードを分離します。具体的には、Flix は
region(リージョン)という概念を使って、mutable なメモリの使用を追跡します。
すなわち、すべての mutable なメモリは、静的にスコープの定まった何らかの
region に属します。

Flix には、基本的な mutable メモリの型が 3 種類あります。

- [References](./references.md)
- [Arrays](./arrays.md)
- [Structs](./structs.md)

これらのデータ型を使って、より高水準な mutable データ構造を構築できます。
たとえば、Flix 標準ライブラリは `MutList`、`MutDeque`、`MutSet`、`MutMap`
といったコレクションを提供しています。原則として、こうした高水準なデータ構造は、
低水準な参照や配列よりも優先して使うべきです。

本章は、まず [regions](./regions.md) についての説明から始めます。

<!--
# Mutable Data

Flix is a _functional-first_ programming language that encourages but does not
demand, the use of immutable data structures. While immutable data structures
should be the default, Flix has rich support for imperative programming with
destructive updates to mutable data. 

Flix uses its effect system to separate pure and impure code. In particular,
Flix uses the region concept to track the use of mutable memory. That is, all
mutable memory belongs to some statically-scoped region.

Flix has three basic types of mutable memory:

- [References](./references.md)
- [Arrays](./arrays.md)
- [Structs](./structs.md)

We can use these data types to build higher-level mutable data structures.
For example, the Flix Standard Library offers collections such as `MutList`,
`MutDeque`, `MutSet`, and `MutMap`. As a rule, these higher-level data
structures should be preferred over lower-level references and arrays.

We begin this chapter with a discussion of [regions](./regions.md).
-->
