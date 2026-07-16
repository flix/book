# パターンマッチング

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/pattern-matching.html)を参照してください。

## Enum に対するマッチング

Flix は、代数的データ型（algebraic data type）に対するパターンマッチングを
サポートしています。

たとえば、図形をモデル化する代数的データ型があるとします。

```flix
enum Shape {
    case Circle(Int32)
    case Square(Int32)
    case Rectangle(Int32, Int32)
}
```

このとき、パターンマッチングを使って `Shape` の面積を計算する関数を、
次のように書けます。

```flix
def area(s: Shape): Int32 = match s {
    case Shape.Circle(r)       => 3 * (r * r)
    case Shape.Square(w)       => w * w
    case Shape.Rectangle(h, w) => h * w
}
```

## レコードに対するマッチング

上記はレコード型に対しても機能しますが、構文が少し異なります。先ほどの
`Shape` 型を、今度はレコードを使って書き換えてみましょう。

```flix
enum Shape {
    case Circle({ radius = Int32 })
    case Square({ width = Int32 })
    case Rectangle({ height = Int32, width = Int32 })
}

def area(s: Shape): Int32 = match s {
    case Shape.Circle({ radius })           => 3 * (radius * radius)
    case Shape.Square({ width })            => width * width
    case Shape.Rectangle({ height, width }) => height * width
}
```

上の例では、各パターンが指定されたラベルをちょうど持つことを、暗黙に
要求しています。多すぎても少なすぎてもいけません。
しかし一般に、レコードパターンの構文はその型の構文と似ています。
そのため、少なくとも特定のラベルを 1 つ持つレコードにマッチさせることができます。

```flix
def f(r: { height = Int32 | a }): Int32 = match r {
    case { height | _ } => height
    // 拡張部分は使われないのでワイルドカードパターンになっています
}
```

ただし、パターンは型も規定する（imply）ことに注意してください。そのため、
次の例は動作しません。

```flix
def badTypes(r: { height = Int32 | a }): Int32 = match r {
    case { height } => height
}
```

さらに、すべての case は同じ型でなければならないため、これも動作しません。

```flix
match ??? {
    case { height | _ } => height
    case { height }     => height
}
```

これはやや不自然な（こじつけのような）例かもしれませんが、よくある落とし穴を示しており、
簡単に修正できます。

これは、最初の case が `height` ラベルを持つ多相的なレコード（polymorphic
record）であるのに対し、2 番目の case が `height` ラベル *のみ* が定義された
閉じたレコード（closed record）にマッチするためです。

さらに、`{ label }` パターンは実際には `{ label = pattern }` の
糖衣構文（syntactic sugar）です。そのため、複数のレコードを扱う場合は、
異なるパターンを使う必要があるかもしれません。

```flix
def shadowing(r1: { height = Int32 | a }, r2: { height = Int32 | b }): Int32 =
    match (r1, r2) {
        case ({ height | _ }, { height | _ }) => height + height
        // `height = height` が 2 回定義されるため、これは動作しません
    }
```

しかし、変数の名前を変えれば、プログラムは型検査を通ります。

```flix
def renaming(r1: { height = Int32 | a }, r2: { height = Int32 | b }): Int32 =
    match (r1, r2) {
        case ({ height = h1 | _ }, { height = h2 | _ }) => h1 + h2
    }
```

まとめると、レコードパターンの例をいくつか挙げます。

- `{ }` - 空のレコード
- `{ radius = r }` - `radius` ラベルだけを持つレコード。その値はスコープ内で `r` に束縛されます
- `{ radius }` - `radius` ラベルだけを持つレコード（これは実際には `{ radius = radius }` の糖衣構文です）
- `{ radius | _ }` - 少なくとも `radius` ラベルを持つレコード
- `{ radius | r }` - 少なくとも `radius` ラベルを持つレコード。レコードの残りの部分は `r` に束縛されます

## let パターンマッチ

パターン `match` 構文に加えて、let 束縛（let-binding）を使って値を分解する
こともできます。たとえば：

```flix
let (x, y, z) = (1, 2, 3)
```

これは変数 `x`、`y`、`z` を、それぞれ値 `1`、`2`、`3` に束縛します。

網羅的（exhaustive）なパターンであれば、let 束縛の中で使えます。たとえば：

```flix
let (x, Foo(y, z)) = (1, Foo(2, 3))
```

これは、`Foo` コンストラクタが、それが唯一のコンストラクタであるような型に
属している場合に限り、正当です。

次の let 束縛は網羅的でないため *不正* です。

```flix
let (1, 2, z) = ...
let Some(x) = ...
```

Flix コンパイラは、このような網羅的でないパターンを拒否します。

let パターンマッチはレコードと相性が良く、レコードを分解して、関心のある
ラベルだけを使うことができます。

```flix
let { height | _ } = r;
height + height
```

## マッチラムダ

パターンマッチは、ラムダ式とともに使うこともできます。たとえば：

```flix
List.map(match (x, y) -> x + y, (1, 1) :: (2, 2) :: Nil)
```

は次と等価です。

```flix
List.map(w -> match w { case (x, y) => x + y }, (1, 1) :: (2, 2) :: Nil)
```

let 束縛の場合と同様に、このようなパターンマッチも網羅的でなければなりません。

2 つのラムダ式の違いに注意してください。

```flix
let f = (x, y, z) -> x + y + z + 42i32
let g = match (x, y, z) -> x + y + z + 42i32
```

ここで `f` は *3 つ* の `Int32` 引数を取る関数であるのに対し、`g` は *1 つ* の
3 要素タプル `(Int32, Int32, Int32)` を引数に取る関数です。

<!--
# Pattern Matching

## Matching on Enums

Flix supports pattern matching on algebraic data types.

For example, if we have an algebraic data type that models shapes:

```flix
enum Shape {
    case Circle(Int32)
    case Square(Int32)
    case Rectangle(Int32, Int32)
}
```

Then we can write a function to compute the area of a `Shape` using pattern
matching:

```flix
def area(s: Shape): Int32 = match s {
    case Shape.Circle(r)       => 3 * (r * r)
    case Shape.Square(w)       => w * w
    case Shape.Rectangle(h, w) => h * w
}
```

## Matching on Records

The above also works for record types; however, the syntax is slightly different.
Let us rewrite the `Shape` type from before, this time using records.

```flix
enum Shape {
    case Circle({ radius = Int32 })
    case Square({ width = Int32 })
    case Rectangle({ height = Int32, width = Int32 })
}

def area(s: Shape): Int32 = match s {
    case Shape.Circle({ radius })           => 3 * (radius * radius)
    case Shape.Square({ width })            => width * width
    case Shape.Rectangle({ height, width }) => height * width
}
```

In the example above, we implicitly require that each pattern
has exactly the specified labels.
No more, no less.
However, in general, the syntax for record patterns is similar to their types.
Thus, we can match on a record that has at least one specific label.

```flix
def f(r: { height = Int32 | a }): Int32 = match r {
    case { height | _ } => height
    // The extension has a wildcard pattern since it is unused
}
```

Note, however, that the pattern also implies a type,
thus the following example will not work.

```flix
def badTypes(r: { height = Int32 | a }): Int32 = match r {
    case { height } => height
}
```

Additionally, all cases must have the same type,
so this will also not work:

```flix
match ??? {
    case { height | _ } => height
    case { height }     => height
}
```

This may be a contrived example, but it
demonstrates a common pitfall, which is easily fixed.

This is because the first case is a polymorphic record
with a defined `height`-label, whereas the second case
matches on a closed record that *only* has the
`height`-label defined.

Additionally, the `{ label }` pattern is actually
syntactic sugar for `{ label = pattern }`.
Thus, if you are dealing with multiple records,
then it may be necessary to use different patterns.

```flix
def shadowing(r1: { height = Int32 | a }, r2: { height = Int32 | b }): Int32 =
    match (r1, r2) {
        case ({ height | _ }, { height | _ }) => height + height
        // This does not work because `height = height` is defined twice
    }
```

However, renaming the variables makes the program type check.

```flix
def renaming(r1: { height = Int32 | a }, r2: { height = Int32 | b }): Int32 =
    match (r1, r2) {
        case ({ height = h1 | _ }, { height = h2 | _ }) => h1 + h2
    }
```

To summarize, here are a few examples of record patterns:

- `{ }` - the empty record
- `{ radius = r }` - a record containg only the label `radius` where the value is bound to `r` in the scope
- `{ radius }` - a record containing only the label `radius` (this is actually syntactic sugar for `{ radius = radius }`)
- `{ radius | _ }` - a record containg at least the label `radius`
- `{ radius | r }` - a record containg at least the label `radius` where the rest of the record is bound to `r`

## Let Pattern Match

In addition to the pattern `match` construct, a let-binding can be used to
destruct a value. For example:

```flix
let (x, y, z) = (1, 2, 3)
```

Binds the variables `x`, `y`, and `z` to the values `1`, `2`, and `3`,
respectively.

Any exhaustive pattern may be used in a let-binding. For example:

```flix
let (x, Foo(y, z)) = (1, Foo(2, 3))
```

is legal provided that the `Foo` constructor belongs to a type where it is the
only constructor.

The following let-bindings are *illegal* because they are not exhaustive:

```flix
let (1, 2, z) = ...
let Some(x) = ...
```

The Flix compiler will reject such non-exhaustive patterns.

Let-pattern-matches work well with records, as they
allow you to destructure a record and only use the
labels you are interested in:

```flix
let { height | _ } = r;
height + height
```

## Match Lambdas

Pattern matches can also be used with lambda expressions. For example:

```flix
List.map(match (x, y) -> x + y, (1, 1) :: (2, 2) :: Nil)
```

is equivalent to:

```flix
List.map(w -> match w { case (x, y) => x + y }, (1, 1) :: (2, 2) :: Nil)
```

As for let-bindings, such pattern matches must be exhaustive.

Note the difference between the two lambda expressions:

```flix
let f = (x, y, z) -> x + y + z + 42i32
let g = match (x, y, z) -> x + y + z + 42i32
```

Here `f` is a function that expects *three* `Int32` arguments, whereas `g` is a
function that expects *one* three tuple `(Int32, Int32, Int32)` argument.
-->
