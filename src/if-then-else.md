# If-then-else

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/if-then-else.html)を参照してください。

Flix は、おなじみの *if-then-else* 式をサポートしています。

```flix
if (1 == 1) "Hello" else "World"
```

これは `Hello` に評価されます。

加えて、`if` ガードは言語の他の部分でもサポートされています。

## ガード付きパターンマッチ

パターンマッチの中で `if` ガードを使えます。

```flix
def isSquare(s: Shape): Bool = match s {
    case Rectangle(h, w) if h == w => true
    case _                         => false
}
```

## ガード付き Datalog ルール

Datalog ルールの中で `if` ガードを使えます。

```flix
Path(x, z) :- Path(x, y), Edge(y, z), if (x != z).
```

ガードを囲む括弧は必須である点に注意してください。

<!--
# If-then-else

Flix supports the usual *if-then-else* expression:

```flix
if (1 == 1) "Hello" else "World"
```

which evaluates to `Hello`.

But `if` guards are also supported in other parts of the language.

## Guarded Pattern Matches

We can use an `if`-guard in a pattern match:

```flix
def isSquare(s: Shape): Bool = match s {
    case Rectangle(h, w) if h == w => true
    case _                         => false
}
```

## Guarded Datalog Rules

We can use an `if`-guard in a Datalog rule:

```flix
Path(x, z) :- Path(x, y), Edge(y, z), if (x != z).
```

Note that the parentheses around the guard are mandatory.
-->
