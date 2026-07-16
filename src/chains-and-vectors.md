# Chains and Vectors

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/chains-and-vectors.html)を参照してください。

Flix は不変な `List` に加えて、不変な `Chain` と `Vector` もサポートしています。

次の表は、list、chain、vector のあいだの性能上のトレードオフを示しています：

| 操作 \ 型             |   List   | Chain |  Vector  |
|-----------------------|:--------:|:-----:|:--------:|
| 先頭要素の取得        |   O(1)   |  O(n) |   O(1)   |
| 末尾要素の取得        |   O(n)   |  O(n) |   O(1)   |
| インデックス指定の取得 |   O(n)   |  O(n) |   O(1)   |
| Cons                  |   O(1)   |  O(n) |   O(n)   |
| Append                | O(n + m) |  O(1) | O(n + m) |

`List`、`Chain`、`Vector` のどれを使うべきでしょうか？：

- `List` データ構造は、シンプルでよく知られているため、デフォルトの選択肢になります。
- `Vector` データ構造は、コレクションのサイズが固定されている場合や、高速なランダムアクセスが必要な場合に最適な選択肢です。
- `Chain` データ構造はあまり使われませんが、高速な append が必要な場合に真価を発揮します。

## Chains

`Chain[t]` は、要素の不変な連結シーケンスです。

`Chain[t]` データ型は次のように定義されています：

```flix
enum Chain[t] {
    case Empty
    case One(t)
    case Chain(Chain[t], Chain[t])
}
```

このデータ構造が `O(1)` の append をサポートするのは、`Chain` コンストラクタ（より適切には `Chain.append`）を使って、既存の2つの chain から新しい chain を構築できるためです。

chain は `Chain.empty`、`Chain.singleton`、`Chain.cons`、`Chain.append` を使って構築できます。

たとえば、次のように書けます：

```flix
let c = Chain.cons(1, Chain.empty());
println(c)
```

これはコンパイルして実行すると `Chain#{1}` を出力します。

## Vectors

`Vector[t]` は、型 `t` の連続した要素からなる、不変で固定長のシーケンスです。

Flix は `Vector` リテラルをサポートしています。たとえば、次のように書けます：


```flix
Vector#{1, 2, 3}
```

これは、要素 1、2、3 を持つ長さ 3 の vector を作成します。

vector は `Vector.get` 操作による高速なランダムアクセスをサポートしています：

```flix
let v = Vector#{1, 2, 3};
println(Vector.get(2, v))
```

これはコンパイルして実行すると `3` を出力します。

> **警告:** vector の範囲を超えたインデックスでアクセスすると、プログラムはパニックします。

vector は多くの操作をサポートしています。たとえば、vector に対して関数をマップできます：

```flix
let v = Vector#{1, 2, 3};
Vector.map(x -> x + 1, v)
```

これは `Vector#{2, 3, 4}` に評価されます。

<!--
# Chains and Vectors

In addition to immutable `List`s, Flix also supports immutable `Chain`s and
`Vector`s. 

The following table illustrates the performance trade-offs between lists,
chains, and vectors:

| Operation \ Type      |   List   | Chain |  Vector  |
|-----------------------|:--------:|:-----:|:--------:|
| Find First Element    |   O(1)   |  O(n) |   O(1)   |
| Find Last Element     |   O(n)   |  O(n) |   O(1)   |
| Find Element at Index |   O(n)   |  O(n) |   O(1)   |
| Cons                  |   O(1)   |  O(n) |   O(n)   |
| Append                | O(n + m) |  O(1) | O(n + m) |

When to use `List`, `Chain`, or `Vector`?:

- The `List` data structure should be the default choice as it is simple and
  well-known.
- The `Vector` data structure is an excellent choice when the size of a
  collection is fixed and/or when fast random access is required. 
- The `Chain` data structure is more rarely used, but shines when fast appends
  are required. 

## Chains

A `Chain[t]` is an immutable linked sequence of elements. 

The `Chain[t]` data type is defined as: 

```flix
enum Chain[t] {
    case Empty
    case One(t)
    case Chain(Chain[t], Chain[t])
}
```

The data structure supports `O(1)` append because we can construct a new chain
from two existing chains using the `Chain` constructor (or more appropriately
using `Chain.append`).

We can build chains using `Chain.empty`, `Chain.singleton`, `Chain.cons`, and
`Chain.append`.

For example, we can write:

```flix
let c = Chain.cons(1, Chain.empty());
println(c)
```

which prints `Chain#{1}` when compiled and executed.

## Vectors

A `Vector[t]` is an immutable fixed-length sequence of contiguous elements of
type `t`.

Flix has support for `Vector` literals. For example, we can write:


```flix
Vector#{1, 2, 3}
```

which creates a vector of length three with the elements: 1, 2, and 3.

Vectors support fast random access with the `Vector.get` operation:

```flix
let v = Vector#{1, 2, 3};
println(Vector.get(2, v))
```

which prints `3` when compiled and executed. 

> **Warning:** Indexing into a vector beyond its bounds will panic the program. 

Vectors support many operations. For example, we can map a function over a vector:

```flix
let v = Vector#{1, 2, 3};
Vector.map(x -> x + 1, v)
```

evaluates to `Vector#{2, 3, 4}`.
-->
