# 可変コレクション

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/mutable-collections.html)を参照してください。

Flix の標準ライブラリは、option、list、chain、set、map をはじめとする多くの不変コレクションをサポートしています。これらの利用を強くおすすめします。

加えて、Flix の標準ライブラリはいくつかの可変コレクションも提供しています：

- `MutList[t, r]`      : 型 `t` の要素からなる、伸縮可能で連続した配列。
- `MutSet[t, r]`       : 型 `t` の要素からなる可変な set。
- `MutMap[k, v, r]`    : 型 `k` のキーを型 `v` の値に対応づける可変な map。
- `MutDeque[t, r]`     : 型 `t` の要素からなる可変な両端キュー（double-ended queue）。

Flix では、可変コレクションを含むすべての可変メモリがリージョンに属することを思い出してください。

次は `MutList[t]` の使い方の例です：

```flix
def main(): Unit \ IO =
    region rc {
        let fruits = MutList.empty(rc);
        MutList.push("Apple", fruits);
        MutList.push("Pear", fruits);
        MutList.push("Mango", fruits);
        MutList.forEach(println, fruits)
    }
```

これは `Apple`、`Pear`、`Mango` を出力します。ここで `MutList[String, rc]` は、要素が push（または pop）されるたびに自動的に拡張（または縮小）します。

上記のプログラムは、`!>` パイプライン演算子を使って、より _流れるようなスタイル（fluent-style）_ で書くこともできます：

```flix
def main(): Unit \ IO =
    region rc {
        let fruits =
            MutList.empty(rc) !>
            MutList.push("Apple") !>
            MutList.push("Pear") !>
            MutList.push("Mango");
        MutList.forEach(println, fruits)
    }
```

上記のプログラムは、次のように複数の関数に分割できます：

```flix
def main(): Unit \ IO =
    region rc {
        let fruits = sweetFruits(rc);
        printFruits(fruits)
    }

def sweetFruits(rc: Region[r]): MutList[String, r] \ r =
    MutList.empty(rc) !>
    MutList.push("Apple") !>
    MutList.push("Pear") !>
    MutList.push("Mango")

def printFruits(fruits: MutList[String, r]): Unit \ {r, IO} =
    MutList.forEach(println, fruits)
```

ここで `main` 関数は新しいリージョン `rc` を導入します。このリージョンを `sweetFruits` に渡し、`sweetFruits` は新しいフルーツの可変リストを作成して返します。`sweetFruits` は `rc` を使って可変メモリを確保するため、エフェクト `r` を持つことに注意してください。`printFruits` はフルーツの可変リストを受け取り、それらを出力します。この関数は `r` 内の可変メモリから読み取るためエフェクト `r` を持ち、また端末に出力するためエフェクト `IO` を持つことに注意してください。

<!--
# Mutable Collections

The Flix standard library supports many immutable collections, including
options, lists, chains, sets, and maps. We strongly encourage their use.

In addition, the Flix standard library also offers several mutable collections:

- `MutList[t, r]`      : a contiguous growable/shrinkable array of elements of type `t`.
- `MutSet[t, r]`       : a mutable set of elements of type `t`.
- `MutMap[k, v, r]`    : a mutable map of keys of type `k` to values of type `v`.
- `MutDeque[t, r]`     : a mutable double-ended queue of elements of type `t`.

Recall that in Flix all mutable memory, including mutable collections, belongs
to a region.

Here is an example of how to use `MutList[t]`:

```flix
def main(): Unit \ IO =
    region rc {
        let fruits = MutList.empty(rc);
        MutList.push("Apple", fruits);
        MutList.push("Pear", fruits);
        MutList.push("Mango", fruits);
        MutList.forEach(println, fruits)
    }
```

which prints `Apple`, `Pear`, and `Mango`. Here the `MutList[String, rc]`
automatically expands (and shrinks) as elements are pushed (or popped) from it.

We can write the above program in a more _fluent-style_ using the `!>` pipeline
operator:

```flix
def main(): Unit \ IO =
    region rc {
        let fruits =
            MutList.empty(rc) !>
            MutList.push("Apple") !>
            MutList.push("Pear") !>
            MutList.push("Mango");
        MutList.forEach(println, fruits)
    }
```

We can split the above program into several functions as follows:

```flix
def main(): Unit \ IO =
    region rc {
        let fruits = sweetFruits(rc);
        printFruits(fruits)
    }

def sweetFruits(rc: Region[r]): MutList[String, r] \ r =
    MutList.empty(rc) !>
    MutList.push("Apple") !>
    MutList.push("Pear") !>
    MutList.push("Mango")

def printFruits(fruits: MutList[String, r]): Unit \ {r, IO} =
    MutList.forEach(println, fruits)
```

Here the `main` function introduces a new region `rc`. We pass this region to
`sweetFruits` which creates and returns a new mutable list of fruits. Note that
`sweetFruits` has the effect `r` since it allocates mutable memory using `rc`.
The `printFruits` takes a mutable list of fruits and prints them. Note that this
function has effect `r` since it reads from mutable memory in `r` and it has
effect `IO` since it prints to the terminal.
-->
