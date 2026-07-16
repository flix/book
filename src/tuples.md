# タプル

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/tuples.html)を参照してください。

Tuple(タプル)は値の積です。タプルは `(exp1, ..., expn)` という形式で記述します。

例えば、以下は `Int32` と `Bool` からなる 2 要素タプル（ペア）です：

```flix
(123, true)
```

このタプルの型は `(Int32, Bool)` です。

タプルはパターンマッチングを使って分解できます。例えば：

```flix
let t = ("Lucky", "Luke", 42, true); // 4要素タプル
let (fstName, lstName, age, male) = t;
lstName
```

は文字列 `"Luke"` に評価されます。

Flix の `Prelude` では `fst` と `snd` 関数が定義されています：

```flix
let t = (1, 2);
let x = fst(t); // x = 1
let y = snd(t)  // y = 2
```

これらは 2 要素タプル（つまりペア）を扱うときに便利です。例えば：

```flix
let l = (1, 1) :: (2, 2) :: Nil; // 型は List[(Int32, Int32)]
List.map(fst, l)                 // 型は List[Int32]
```

これは次のリストに評価されます：

```flix
1 :: 2 :: Nil
```

<!--
# Tuples

A tuple is a product of values. The form of a tuple is `(exp1, ..., expn)`.

For example, here is a 2-tuple (a pair) of an
`Int32` and a `Bool`:

```flix
(123, true)
```

The type of the tuple is `(Int32, Bool)`.

We can destructure a tuple using pattern matching. For example:

```flix
let t = ("Lucky", "Luke", 42, true); // 4-tuple
let (fstName, lstName, age, male) = t;
lstName
```

evaluates to the string `"Luke"`.

The Flix `Prelude` defines the `fst` and `snd` functions:

```flix
let t = (1, 2);
let x = fst(t); // x = 1
let y = snd(t)  // y = 2
```

which are useful when working with 2-tuples (i.e. pairs). For example:

```flix
let l = (1, 1) :: (2, 2) :: Nil; // has type List[(Int32, Int32)]
List.map(fst, l)                 // has type List[Int32]
```

which evaluates to the list:

```flix
1 :: 2 :: Nil
```
-->
