# Regions

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/regions.html)を参照してください。

Flix は _スコープ付き_ の可変メモリをサポートしています。Flix では、すべての可変メモリは、そのレキシカルスコープに紐づく _リージョン（region）_ に属します。実行がリージョンのレキシカルスコープを抜けると、そのリージョン内のすべてのメモリは到達不能になります。

リージョンが役立つのは、内部で _ミューテーション（mutation）_ を使う _純粋関数_ を実装できるようにするからです。この強力なアイデアを、いくつかの実例で説明していきますが、まずはリージョンの使い方から見ていきましょう。

新しいリージョンスコープは `region` 構文で導入します：

```flix
region rc { // リージョン開始。
  ...       // リージョンハンドル `rc` がスコープ内にあります。
}           // リージョンが終了し、`rc` に紐づくすべてのデータがスコープ外になります。
```

リージョンを使えば、内部でミューテーションを使いながらも純粋な `sort` 関数を実装できます：

```flix
def sort(l: List[a]): List[a] with Order[a] =
    region rc {
        let arr = List.toArray(rc, l);
        Array.sort(arr);
        Array.toList(arr)
    }
```

ここでは `rc` という名前のリージョンを導入しています。`List.toArray` 関数を使って、リスト `l` をリージョン `rc` に紐づく可変配列 `arr` に変換します。次に、効率的なインプレースソートアルゴリズムを使う `Array.sort` で `arr` をソートします。最後に、ソート済みの配列をリストに戻して返します。`sort` 関数は内部でミューテーションを使っているにもかかわらず、純粋です。

別の例として、`List[a]` 向けの `toString` 関数を実装してみましょう。これは純粋ですが、内部では可変な `StringBuilder` を使っています：

```flix
def toString(l: List[a]): String with ToString[a] =
    region rc {
        let sb = StringBuilder.empty(rc);
        List.forEach(x -> StringBuilder.appendString("${x} :: ", sb), l);
        StringBuilder.appendString("Nil", sb);
        StringBuilder.toString(sb)
    } // rc のスコープが終了し、式全体は純粋です。
```

プログラミングのパターンは同じです。新しいリージョンを開き、リージョン内に `StringBuilder` を確保し、ビルダーを文字列で埋め、最後に1つの文字列に変換します。

リージョンを使うと、特定の _関数型の操作_ をより効率的に実装できます。たとえば、次は `List.flatMap` の高速な実装です：

```flix
def flatMap(f: a -> List[b] \ ef, l: List[a]): List[b] \ ef =
    region rc {
        let ml = MutList.empty(rc);
        l |> List.forEach(x -> MutList.append(f(x), ml));
        MutList.toList(ml)
    }
```

## リージョンは値である

リージョン（またはリージョンハンドル）は、関数の引数として渡せる _値_ です。これは、たとえば可変データ構造を確保して返す再利用可能な関数を書きたいときに便利です。

たとえば、次は `List.toMutDeque` 関数です：

```flix
def toMutDeque(rc: Region[r], l: List[a]): MutDeque[a, r] \ r =
    let d = MutDeque.empty(rc);
    foreach (x <- l) {
        MutDeque.pushBack(x, d)
    };
    d
```

この関数はリージョンハンドル `rc` を受け取り、与えられたリージョン内に新しい可変な両端キュー（deque、`MutDeque`）を確保し、リスト `l` のすべての要素をデックに挿入して、それを返します。

## リージョンはスコープを持つ

リージョンと、それに紐づくすべてのメモリは、そのレキシカルスコープより長く生存することはできません。

次のプログラムを考えてみましょう：

```flix
def main(): Unit \ IO =
    let escaped = region rc {
        Array#{1, 2, 3} @ rc
    };
    println(escaped)
```

ここでは `Array#{1, 2, 3}` をリージョン `rc` 内に確保し、それを外側のスコープの外へ返そうとしています。Flix コンパイラはこのようなエスケープ違反を検出し、エラーを報告します：

```
❌ -- Type Error ----------------------------

>> The region variable 'rc' escapes its scope.

2 |>     let escaped = region rc {
3 |>         Array#{1, 2, 3} @ rc
4 |>     };

region variable escapes.
```

<!--
# Regions

Flix supports _scoped_ mutable memory. In Flix, all mutable memory belongs to a
_region_ that is tied to its lexical scope. When execution leaves the lexical
scope of a region, all memory in that region becomes unreachable.

Regions are useful because they enable us to implement _pure functions_ that
internally use _mutation_. We will illustrate this powerful idea with several
real-world examples, but let us first discuss how to use a region:

We introduce a new region scope with the `region` construct:

```flix
region rc { // region starts.
  ...       // the region handle `rc` is in scope.
}           // region ends and all data associated with `rc` is no longer in scope.
```

We can use regions to implement a pure `sort` function that internally uses mutation:

```flix
def sort(l: List[a]): List[a] with Order[a] =
    region rc {
        let arr = List.toArray(rc, l);
        Array.sort(arr);
        Array.toList(arr)
    }
```

Here we introduce a region named `rc`. We use the function `List.toArray` to
convert the list `l` to a mutable array `arr` associated with the region `rc`.
We then sort `arr` using `Array.sort` which uses an efficient in-place sorting
algorithm. Finally, we convert the sorted array back to a list and return it.
The `sort` function is pure, even though it internally uses mutation.

As another example, we can implement a `toString` function for `List[a]` which
is pure but internally uses a mutable `StringBuilder`:

```flix
def toString(l: List[a]): String with ToString[a] =
    region rc {
        let sb = StringBuilder.empty(rc);
        List.forEach(x -> StringBuilder.appendString("${x} :: ", sb), l);
        StringBuilder.appendString("Nil", sb);
        StringBuilder.toString(sb)
    } // scope of rc ends, the entire expression is pure.
```

The programming pattern is the same: We open a new region, allocate a
`StringBuilder` in the region, fill the builder with strings, and convert it
into one string.

We can use regions to implement certain _functional operations_ more
efficiently. For example, here is a fast implementation of `List.flatMap`:

```flix
def flatMap(f: a -> List[b] \ ef, l: List[a]): List[b] \ ef =
    region rc {
        let ml = MutList.empty(rc);
        l |> List.forEach(x -> MutList.append(f(x), ml));
        MutList.toList(ml)
    }
```

## Regions are Values

A region (or region handle) is a _value_ that can be passed as a function
argument. This is useful, for example, when we want to write a reusable function
that allocates and returns a mutable data structure.

For example, here is the `List.toMutDeque` function:

```flix
def toMutDeque(rc: Region[r], l: List[a]): MutDeque[a, r] \ r =
    let d = MutDeque.empty(rc);
    foreach (x <- l) {
        MutDeque.pushBack(x, d)
    };
    d
```

The function takes a region handle `rc`, allocates a new mutable deque
(`MutDeq`) in the given region, inserts all elements of the list `l` in the
deque, and returns it.

## Regions are Scoped

Regions and all memory associated with them cannot outlive their lexical scope.

Consider the following program:

```flix
def main(): Unit \ IO =
    let escaped = region rc {
        Array#{1, 2, 3} @ rc
    };
    println(escaped)
```

Here we allocate the `Array#{1, 2, 3}` in the region `rc` and try to return it
outside of its enclosing scope. The Flix compiler detects such escape violations
and reports an error:

```
❌ -- Type Error ----------------------------

>> The region variable 'rc' escapes its scope.

2 |>     let escaped = region rc {
3 |>         Array#{1, 2, 3} @ rc
4 |>     };

region variable escapes.
```
-->
