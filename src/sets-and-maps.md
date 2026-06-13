# Set と Map

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/sets-and-maps.html)を参照してください。

Flix は平衡木に基づく（イミュータブルな）`Set`(セット)と `Map`(マップ)を強力にサポートしています。そのため、`Set` の要素と `Map` のキーは `Order` trait を実装している必要があります。

> **ヒント:** Flix の `Set` および `Map` データ構造は、特定の操作を自動的に並列化します。そのような操作には、API ドキュメント内で `@ParallelWhenPure` という印が付けられています。

## Set

空の Set は次のように記述します。

```flix
Set#{}
```

これは `Set.empty()` と同等です。Set リテラルは次のように記述します。

```flix
Set#{1, 2, 3}
```

`Set.insert` を使って Set に要素を挿入することができます（この関数は新しい Set を返します）。

```flix
let s1 = Set#{1, 2, 3};
let s2 = Set.insert(4, s1);
```

`Set.memberOf` を使って、Set がある要素を含んでいるかどうかを判定することができます。

```flix
let s = Set#{1, 2, 3};
Set.memberOf(2, s)
```

`Set.union` を使って 2 つの Set を結合することができます。

```flix
let s1 = Set#{1, 2, 3};
let s2 = Set#{3, 4, 5};
let sr = Set.union(s1, s2);
```

`Set` は `SemiGroup` であるため、`++` 演算子を使って `s1 ++ s2` と書くこともできます。

## Map

空の Map は次のように記述します。

```flix
Map#{}
```

これは `Map.empty()` と同等です。Map リテラルは次のように記述します。

```flix
Map#{"a" => 1, "b" => 2, "c" => 3}
```

`Map.insert` を使って Map に要素を挿入することができます（この関数は新しい Map を返します）。

```flix
let m1 = Map#{"a" => 1, "b" => 2, "c" => 3};
let m2 = Map.insert("d", 4, m1);
```

`Map.get` を使って、あるキーに関連付けられた値を取得することができます。

```flix
let m = Map#{"a" => 1, "b" => 2, "c" => 3};
Map.get("b", m) 
```

`Map.get` 関数は `Option[v]` を返します。

`Map.unionWith` および `Map.unionWithKey` 関数のいずれかを使って 2 つの Map を結合することができます。

<!--
# Sets and Maps

Flix has excellent support for (immutable) `Set`s and `Map` based on balanced
trees; hence the elements of a `Set` and the keys of `Map` must implement the
`Order` trait. 

> **Tip:** The Flix `Set` and `Map` data structures will automatically
> parallelize certain operations. Such operations are marked with
> `@ParallelWhenPure` in the API docs. 

## Sets

The empty set is written as:

```flix
Set#{}
```

which is equivalent to `Set.empty()`. A set literal is written as:

```flix
Set#{1, 2, 3}
```

We can insert into a set using `Set.insert` (which returns a new set):

```flix
let s1 = Set#{1, 2, 3};
let s2 = Set.insert(4, s1);
```

We can determine if a set contains an element using `Set.memberOf`:

```flix
let s = Set#{1, 2, 3};
Set.memberOf(2, s)
```

We can merge two sets using `Set.union`:

```flix
let s1 = Set#{1, 2, 3};
let s2 = Set#{3, 4, 5};
let sr = Set.union(s1, s2);
```

Since `Set`s are `SemiGroup`s, we can also use the `++` operator and write `s1
++ s2`. 

## Maps

The empty map is written as:

```flix
Map#{}
```

which is equivalent to `Map.empty()`. A map literal is written as:

```flix
Map#{"a" => 1, "b" => 2, "c" => 3}
```

We can insert into a map using `Map.insert` (which returns a new map):

```flix
let m1 = Map#{"a" => 1, "b" => 2, "c" => 3};
let m2 = Map.insert("d", 4, m1);
```

We can lookup the value associated with a key using `Map.get`:

```flix
let m = Map#{"a" => 1, "b" => 2, "c" => 3};
Map.get("b", m) 
```

The `Map.get` function returns an `Option[v]`.

We can merge two maps using one of `Map.unionWith` and `Map.unionWithKey`
functions.
-->
