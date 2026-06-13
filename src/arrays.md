# 配列

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/arrays.html)を参照してください。

Flix は、ミュータブル(可変)な _スコープ付き_ 配列(Array)をサポートしています。配列とは、同じ型を共有する固定長でミュータブルな要素の列です。配列はメモリ上に連続して配置されます。配列はミュータブルであるため、その要素は時間とともに変化し得ます。ただし、いったん作成すると、配列の長さは変更できません。

Flix では、配列の型は `Array[t, r]` です。ここで `t` は要素の型、`r` はそのリージョン(region)です。Flix のすべての可変メモリと同様に、すべての配列はいずれかのリージョンに属さなければなりません。配列の読み取りと書き込みは _エフェクトを持つ_ 操作です。たとえば、型 `Array[t, r]` の配列から要素を読み取る操作はエフェクト `r` を持ちます。同様に、リージョン内で配列を作成する操作もエフェクトを持つ操作です。

配列は _常に_ アンボックス(unboxed)化されています。たとえば、型 `Array[Int32, r]` の配列は、プリミティブな32ビット整数の列として表現されます。すなわち JVM の用語で言えば、その配列は `int[]` として表現されます。Flix はプリミティブな整数を `java.lang.Integer` オブジェクトとしてボックス化することは決してありませんが、それでもジェネリックなコレクションや関数の中でプリミティブを使うことは許可しています。これは他の種類のプリミティブやプリミティブの配列についても同様です。

配列は低レベルのデータ構造であり、通常はより高レベルなデータ構造を実装するために使われます。したがって、そのようなデータ構造を実装する場合を除いては、配列の使用は控えめにすることをおすすめします。代わりに、`MutList`、`MutDeque`、`MutSet`、`MutMap` といったデータ構造を使うことをおすすめします。

> **ヒント:** 要素の _伸長可能(growable)_ な可変列が必要な場合は、`MutList` を使ってください。

## 配列リテラル

配列リテラルの構文は `Array#{e1, e2, e3, ...} @ r` の形をとります。ここで `e1`、`e2` などは _要素式_ であり、`r` は _リージョン式_ です。たとえば次のようになります。

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    println(Array.toString(fruits))
}
```

ここでは `rc` という名前のリージョンを導入しています。このリージョン内で、`"Apple"`、`"Pear"`、`"Mango"` という3つの文字列を含む配列 `fruits` を作成しています。`fruits` の型は `Array[String, rc]` です。リージョンの詳細については、[リージョン](regions.md)の章を参照してください。

このプログラムを実行すると `Array#{"Apple", "Pear", "Mango"}` が出力されます。

## 配列の確保

`Array.repeat` 関数を使うと、同じ要素で満たされたサイズ `n` の配列を確保できます。たとえば次のようになります。

```flix
region rc {
    let arr = Array.repeat(rc, 1_000, 42);
    println(Array.toString(arr))
}
```

ここでは、各要素が値 `42` を持つ、長さ `1_000` の配列 `arr` を作成しています。`Array.repeat` にはリージョン `rc` を引数として渡す必要がある点に注意してください。返される配列がどのリージョンに属するべきかを、この関数が知る必要があるからです。

ゼロから99までのすべての整数で満たされた配列を作成することもできます。

```flix
region rc {
    let arr = Array.range(rc, 0, 100);
    println(Array.toString(arr))
}
```

さらに、ほとんどのデータ構造は配列に変換できます。たとえば次のようになります。

```flix
region rc {
    let fruitList = List#{"Apple", "Pear", "Mango"};
    let fruitArray = List.toArray(rc, fruitList);
}
```

`List.toArray` にはリージョン `rc` を引数として渡す必要がある点に注意してください。返される配列がどのリージョンに属するべきかを、この関数が知る必要があるからです。

## 未初期化の要素を持つ配列の確保

`Array.empty` 関数を使うと、内容が未初期化の、指定した長さの配列を作成できます。たとえば次のようになります。

```flix
region rc {
    let arr: Array[String, rc] = Array.empty(rc, 100);
    // ... ここで `arr` を初期化します ...
}
```

ここでは、型 `Array[String, rc]` の長さ `100` の配列を作成しています。配列の期待される型を Flix に伝えるために、明示的な型注釈 `: Array[String, rc]` を使っています。

> **警告:** 未初期化の要素を持つ配列を使うのは危険です。

未初期化の配列の要素は何になるのでしょうか？ Flix は Java（および JVM）に従い、すべてのプリミティブ型および参照型に対して _デフォルト値_ を定義しています。たとえば `Bool` と `Int32` のデフォルト値は、それぞれ `false` と `0` です。参照型のデフォルト値は `null` です。ですから注意してください！ Flix には `null` 値はありませんが、適切に初期化されていない配列を読み取ることで間接的に `null` が持ち込まれてしまい、`NullPointerException` を引き起こす可能性があります。

## 配列の読み取りと書き込み

`Array.get` と `Array.put` を使うと、配列の特定の位置にある要素をそれぞれ取得・更新できます。たとえば次のようになります。

```flix
region rc {
    let strings = Array.empty(rc, 2);
    Array.put("Hello", 0, strings);
    Array.put("World", 1, strings);
    let s1 = Array.get(0, strings);
    let s2 = Array.get(1, strings);
    println("${s1} ${s2}")
}
```

ここでは長さ2の空の配列を作成しています。次に、位置ゼロに文字列 `"Hello"` を、位置1に文字列 `"World"` を格納します。続いて、その2つの文字列を取得して出力します。したがって、このプログラムをコンパイルして実行すると `Hello World` が出力されます。

`!>` パイプライン演算子を使うと、プログラムの一部をより _流れるようなスタイル(fluent-style)_ で書くこともできます。

```flix
let strings =
    Array.empty(rc, 2) !>
    Array.put("Hello", 0) !>
    Array.put("World", 1);
```

## 配列のスライス

`Array.slice` を使って配列をスライスできます。配列のスライスとは、元の配列の部分範囲を新しく（浅く）コピーしたものです。たとえば次のようになります。

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    let result = Array.slice(rc, start = 1, end = 2, fruits);
    println(Array.toString(result))
}
```

これは実行すると `Array#{"Pear"}` を出力します。

## 配列の長さの取得

`Array.length` 関数を使って配列の長さを計算できます。たとえば次のようになります。

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    println(Array.length(fruits))
}
```

これは実行すると `3` を出力します。

> **注意:** 配列をインデックスベースで反復処理することはおすすめしません。代わりに、`Array.count`、`Array.forEach`、`Array.transform` といった関数を使うことをおすすめします。

## その他の配列操作

`Array` モジュールは、配列を扱うための関数を豊富に取りそろえています。いくつか挙げると、たとえば `Array.append`、`Array.copyOfRange`、`Array.findLeft`、`Array.findRight`、`Array.sortWith`、`Array.sortBy` などがあります。このモジュールは合計で100を超える関数をすぐに使える形で提供しています。

<!--
# Arrays

Flix supports mutable _scoped_ arrays. An array is a fixed-length mutable
sequence of elements that share the same type. Arrays are laid out consecutively
in memory. Arrays are mutable; hence their elements can change over time.
However, once created, the length of an array cannot be changed.

In Flix, the type of an array is `Array[t, r]` where `t` is the type of its
elements and `r` is its region. Like all mutable memory in Flix, every array
must belong to some region. Reading from and writing to arrays are _effectful_
operations. For example, reading an element from an array of type `Array[t, r]`
has the effect `r`. Likewise, creating an array in a region is also an effectful
operation.

Arrays are _always_ unboxed. For example, an array of type `Array[Int32, r]` is
represented as a sequence of primitive 32-bit integers, i.e., in JVM
terminology, the array is represented as `int[]`. Flix will never box primitive
integers as `java.lang.Integer` objects but still permits primitives in generic
collections and functions. The same is true for other types of primitives and
arrays of primitives.

Arrays are low-level data structures typically used to implement higher-level
data structures. Therefore, unless implementing such data structures, we
recommend that arrays are used sparingly. Instead, we recommend using the
`MutList`, `MutDeque`, `MutSet`, and `MutMap` data structures.

> **Hint:** Use `MutList` if you need a _growable_ mutable sequence of elements.

## Array Literals

The syntax of an array literal is of the form `Array#{e1, e2, e3, ...} @ r`
where `e1`, `e2`, and so forth are _element expressions_, and `r` is the _region
expression_. For example:

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    println(Array.toString(fruits))
}
```

Here we introduce a region named `rc`. Inside the region, we create an array of
`fruits` that contain the three strings `"Apple"`, `"Pear"`, and `"Mango"`. The
type of `fruits` is `Array[String, rc]`. For more information about regions, we
refer to the chapter on [Regions](regions.md).

Running the program prints `Array#{"Apple", "Pear", "Mango"}`.

## Allocating Arrays

We can allocate an array of size `n` filled with the same element using the
`Array.repeat` function. For example:

```flix
region rc {
    let arr = Array.repeat(rc, 1_000, 42);
    println(Array.toString(arr))
}
```

Here we create an array `arr` of length `1_000` where each array element has the
value `42`. Note that we must pass the region `rc` as an argument to
`Array.repeat` because the function must know to which region the returned array
should belong.

We can also create an array filled with all integers from zero to ninety-nine:

```flix
region rc {
    let arr = Array.range(rc, 0, 100);
    println(Array.toString(arr))
}
```

Moreover, we can convert most data structures to arrays. For example:

```flix
region rc {
    let fruitList = List#{"Apple", "Pear", "Mango"};
    let fruitArray = List.toArray(rc, fruitList);
}
```

Note that we must pass the region `rc` as an argument to `List.toArray` since
the function must know to which region the returned array should belong.

## Allocating Arrays with Uninitialized Elements

We can use the `Array.empty` function to create an array of a given length where
the content of the array is uninitialized. For example:

```flix
region rc {
    let arr: Array[String, rc] = Array.empty(rc, 100);
    // ... initialize `arr` here ...
}
```

Here we create an array of length `100` of type `Array[String, rc]`. We use an
explicit type annotation `: Array[String, rc]` to inform Flix of the expected
type of the array.

> **Warning:** It is dangerous to use arrays that have uninitialized elements.

What are the elements of an uninitialized array? Flix follows Java (and the JVM)
which defines a _default value_ for every primitive-- and reference type. So,
for example, the default values for `Bool` and `Int32` are `false` and `0`,
respectively. The default value for reference types are `null`. So be careful!
Flix does not have a `null` value, but one can be indirectly introduced by
reading from improperly initialized arrays which can lead to
`NullPointerException`s.

## Reading from and Writing to Arrays

We can retrieve or update the element at a specific position in an array using
`Array.get` and `Array.put`, respectively. For example:

```flix
region rc {
    let strings = Array.empty(rc, 2);
    Array.put("Hello", 0, strings);
    Array.put("World", 1, strings);
    let s1 = Array.get(0, strings);
    let s2 = Array.get(1, strings);
    println("${s1} ${s2}")
}
```

Here we create an empty array of length of two. We then store the string
`"Hello"` at position zero and the string `"World"` at position one. Next, we
retrieve the two strings, and print them. Thus the program, when compiled and
run, prints `Hello World`.

We can also write part of the program in a more _fluent-style_ using the `!>`
pipeline operator:

```flix
let strings =
    Array.empty(rc, 2) !>
    Array.put("Hello", 0) !>
    Array.put("World", 1);
```

## Slicing Arrays

We can slice arrays using `Array.slice`. A slice of an array is a new (shallow)
copy of a sub-range of the original array. For example

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    let result = Array.slice(rc, start = 1, end = 2, fruits);
    println(Array.toString(result))
}
```

which prints `Array#{"Pear"}` when run.

## Taking the Length of an Array

We can compute the length of an array using the `Array.length` function. For
example

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    println(Array.length(fruits))
}
```

which prints `3` when run.

> **Note**: We advise against indexed-based iteration through arrays. Instead,
> we recommend to use functions such as `Array.count`, `Array.forEach`, and
> `Array.transform`.

## Additional Array Operations

The `Array` module offers an extensive collection of functions for working with
arrays. For example, `Array.append`, `Array.copyOfRange`, `Array.findLeft`,
`Array.findRight`, `Array.sortWith`, and `Array.sortBy` to name a few. In
total, the module offers more than 100 functions ready for use.
-->
