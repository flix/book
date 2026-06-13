# エフェクト多相

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/effect-polymorphism.html)を参照してください。

Flix では、関数が純粋である（つまり副作用がない）ことを表現できます。

```flix
def inc(x: Int32): Int32 \ { } = x + 1
                        // ^^^ 空のエフェクト集合
```

`inc` 関数はエフェクト集合が空であるため _純粋_ です。関数が純粋である場合、その関数は同じ引数を与えられれば同じ値を返さなければならないことがわかります。さらに、その関数は外の世界に対していかなる副作用も持つことができません。

空のエフェクト集合は書かなくても構いません。単純に次のように書けます。

```flix
def inc(x: Int32): Int32 = x + 1
```

Flix では、関数が単一のエフェクトを持つことを表現できます。

```flix
def incAndPrint(x: Int32): Int32 \ {IO} = 
    let result = x + 1;         // ^^^^ 単一要素のエフェクト集合
    println(result);
    result
```


ここで `incAndPrint` 関数はプリミティブな `IO` エフェクトを持ちます。

関数が複数のエフェクトを持つことも表現できます。

```flix
def copyFile(src: File, dst: File): Unit \ {FsRead, FsWrite, IO} = ...
                                         // ^^^^^^^^^^^^^^^^^^^^ 複数のエフェクト
```

ここで `copyFile` 関数は `FsRead`、`FsWrite`、`IO` という3つのプリミティブエフェクトを持ちます。

Flix では、ヒープエフェクトを持つ関数を表現できます。

```flix
def nth(i: Int32, a: Array[t, r]): Option[a] \ {r} = ....
                                            // ^^^ ヒープエフェクト
```

ここで `nth` 関数はリージョン `r` におけるヒープエフェクトを持ちます。

異なるエフェクトを混在させた関数を書くこともできます。

```flix
use Time.Clock

def strange(a: Array[t, r]): Unit \ {r, Clock, Http, IO}
                                 // ^^^^^^^^^^^^^^^^^^^ エフェクトの混在
```

この関数はヒープエフェクト `r` と、`Clock`、`Http`、`IO` という3つのエフェクトを持ちます。

## 高階関数

高階関数を書くときには、そのエフェクトの振る舞いについて注意深く考えなければなりません。

例えば、高階関数 `Set.exists` を次のように書くことができます。

```flix
def exists(f: a -> Bool \ { }, s: Set[a]): Bool = ...
                          ^^^
```

ここで `exists` 関数は述語関数 `f` が純粋であることを強制します。なぜこのようにするのでしょうか。少なくとも2つの理由があります。(a) Set で使われる反復順序を隠蔽できること、(b) カウントを並列に実行できることです。

とはいえ、必要でない限り関数を純粋であるよう要求するのは、悪いプログラミングスタイルと考えられます。代わりに、_エフェクト多相な_ 関数を書くべきです。エフェクト多相な関数とは、その関数引数のエフェクトに依存してエフェクトが定まる高階関数のことです。

例えば、エフェクト多相な map 関数を次のように書くことができます。

```flix
def map(f: a -> b \ ef, l: List[a]): List[b] \ ef = ...
                    ^^ // エフェクト変数      ^^ エフェクト変数
```

`map` の型・エフェクトのシグネチャは次のことを示しています。`map` にエフェクト `ef` を持つ関数 `f` が与えられた場合、`map` の呼び出しはエフェクト `ef` を持ちます。つまり、`f` が純粋（つまりエフェクトを持たない）であれば、`map` の呼び出しも純粋になります。`f` が `IO` エフェクトを持つ場合、`map` の呼び出しは `IO` エフェクトを持ちます。


```flix
List.map(x -> x + 1, l)               // { } エフェクトを持つ（つまり純粋）
List.map(x -> {println(x); x + 1}, l) // { IO } エフェクトを持つ
```

複数の関数引数を取る高階関数は、それらのエフェクトを組み合わせることがあります。

例えば、Flix 標準ライブラリにおける前方関数合成 `>>` の定義は、2つの関数 `f` と `g` を取り、それらを合成します。

```flix
def >>(f: a -> b \ ef1, g: b -> c \ ef2): a -> c \ (ef1 + ef2) = x -> g(f(x))
```

`>>` の型・エフェクトのシグネチャは次のことを示しています。`map` にエフェクト `ef1` を持つ関数 `f` とエフェクト `ef2` を持つ関数 `g` が与えられた場合、エフェクトの和集合 `ef1 + ef2` を持つ新しい関数を返します。

Flix では、エフェクトの言語は集合の式に基づいています。

- `ef` の *補集合* は `~ef` と書きます。
- `ef1` と `ef2` の *和集合* は `ef1 + ef2` と書きます。
- `ef1` と `ef2` の *共通部分（積集合）* は `ef1 & ef2` と書きます。
- `ef1` と `ef2` の *差集合* は `ef1 - ef2` と書きます。

最もよく使われる操作は、圧倒的にエフェクトの和集合を計算することです。

同じエフェクト集合を書く方法が複数あり得ることを理解しておくことが重要です。例えば、`ef1 + ef2` は、予想される通り `ef2 + ef1` と等価です。

## エフェクト除外

Flix の新しい機能として、[エフェクト除外](https://dl.acm.org/doi/abs/10.1145/3607846) のサポートがあります。簡単に言うと、エフェクト除外によって、特定のエフェクトを許可しない一方でその他すべてのエフェクトを許可するような高階関数を書くことができます。

例えば、イベントリスナーの登録関数を次のように書くことができます。

```flix
def onClick(listener: KeyEvent -> Unit \ (ef - Block), ...): ... 
```

ここで `onClick` 関数は、`Block` エフェクトを _除く_ _任意の_ エフェクトを持ち得るイベントリスナーを取ります。したがって、リスナーは UI スレッドをブロックするようなアクションを除いて、任意のアクションを実行できます。

別の例として、例外ハンドラ関数を次のように書くことができます。

```flix
def recoverWith(f: Unit -> a \ Throw, h: ErrMsg -> a \ (ef - Throw)): a = ... 
```

ここで `recoverWith` 関数は2つの関数引数を取ります。例外を投げる可能性のある関数 `f` と、そのエラーを処理できるハンドラ `h` です。注目すべきは、エフェクトシステムが `h` 自身は例外を投げられないことを強制する点です。

## サブエフェクト

> **注意:** この機能はまだ有効化されていません。

Flix は _サブエフェクト_ をサポートしており、これによって式や関数がそのエフェクト集合を _広げる_ ことができます。

例えば、次のように書いた場合を考えます。

```flix
if (???) { x -> x + 1 } else { x -> {println(x); x + 1}}
```

最初の分岐は型 `Int32 -> Int32 \ { }`（つまり純粋）を持つはずであり、一方で2番目の分岐は型 `Int32 -> Int32 \ { IO }` を持ちます。サブエフェクトがなければ、`{ } != { IO }` であるためこれら2つの型は互換性がありません。しかし、サブエフェクトのおかげで、Flix は最初の分岐に新しいエフェクト変数 `ef` を用いた型 `Int32 -> Int32 \ ef` を与えます。これによって型推論は最初の分岐のエフェクトを `IO` に _広げる_ ことができます。したがってコンパイラは式全体を型検査できます。

別の例として、次を考えます。

```flix
def handle(f: Unit -> a \ (ef + Throw)): a = ...
```

ここで `handle` 関数は `Throw` エフェクトを持つ関数引数 `f` を期待します。しかし、サブエフェクトのおかげで、純粋な関数を使って `handle` 関数を呼び出すこともできます。つまり、次の通りです。

```flix
def handle(x -> Throw.throw(x))    // OK。`Throw` エフェクトを持つ。
def handle(x -> x)                 // OK。サブエフェクトによる。
def handle(x -> println(x))        // NG。handle は `IO` を許可しない。
```

Flix はインスタンス宣言でもサブエフェクトを許可します。

例えば、次のトレイトを定義できます。

```flix
trait Foo[t] {
    def f(x: t): Bool \ { IO }
}
```

ここで `f` は `IO` エフェクトを持ちます。これを次のように実装できます。

```flix
instance Foo[Int32] {
    def f(x: Int32): Bool = x == 0 // 純粋関数
}
```

`f` の宣言されたエフェクトは `IO` ですが、ここでの `f` の実装は純粋です（つまり、空のエフェクト集合 `{ }` を持ちます）。`{ }` は `IO` に広げることができるため、このプログラムは依然として型検査を通ります。

しかし、Flix はトップレベル関数についてはサブエフェクトを許可しません。

例えば、次の関数を宣言した場合を考えます。

```flix
def foo(): Bool \ IO = true
```

Flix コンパイラは次のエラーメッセージを出力します。

```
❌ -- Type Error ------------------------------

>> Expected type: 'IO' but found type: 'Pure'.

1 | def foo(): Bool \ IO = true
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    expression has unexpected type.
```

まとめると、Flix は2つの場合にエフェクトの拡大を許可します。(a) ラムダ式と (b) インスタンス定義です。これを、Flix は _抽象化サイトのサブエフェクト_ と _インスタンス定義のサブエフェクト_ をサポートしている、と言います。

<!--
# Effect Polymorphism

In Flix, we can express that a function is pure (i.e. has no side-effects): 

```flix
def inc(x: Int32): Int32 \ { } = x + 1
                        // ^^^ empty effect set
```

The `inc` function is _pure_ because its effect set is empty. When a function is
pure, we know that the function must return the same value when given the same
arguments. Moreover, the function cannot have any side-effect on the outside
world. 

We do not have to write the empty effect set. We can simply write:

```flix
def inc(x: Int32): Int32 = x + 1
```

In Flix, we can express that a function has a single effect:

```flix
def incAndPrint(x: Int32): Int32 \ {IO} = 
    let result = x + 1;         // ^^^^ singleton effect set
    println(result);
    result
```


Here the `incAndPrint` function has the primitive `IO` effect. 

We can also express that a function has multiple effects:

```flix
def copyFile(src: File, dst: File): Unit \ {FsRead, FsWrite, IO} = ...
                                         // ^^^^^^^^^^^^^^^^^^^^ multiple effects
```

Here the `copyFile` function has three primitive effects: `FsRead`, `FsWrite`,
and `IO`.

In Flix, we can express a function that has a heap effect:

```flix
def nth(i: Int32, a: Array[t, r]): Option[a] \ {r} = ....
                                            // ^^^ heap effect
```

Here the `nth` function has a heap effect in the region `r`.

We can also write functions that mix different effects:

```flix
use Time.Clock

def strange(a: Array[t, r]): Unit \ {r, Clock, Http, IO}
                                 // ^^^^^^^^^^^^^^^^^^^ a mixture of effects
```

This function has a heap effect `r` and three effects: `Clock`, `Http`, and `IO`.

## Higher-Order Functions

When we write higher-order functions, we must think carefully about their effect behavior. 

For example, we can write a higher-order function `Set.exists`:

```flix
def exists(f: a -> Bool \ { }, s: Set[a]): Bool = ...
                          ^^^
```

Here the `exists` function enforces the predicate function `f` to be pure. Why
would we do this? For at least two reasons: (a) it allows us to hide the
iteration order used in the set, and (b) it allows us to perform the counting in
parallel. 

Nevertheless, requiring a function to be pure unless necessary is considered a
bad programming style. Instead, we should write _effect polymorphic_ functions.
An effect polymorphic function is a higher-order function whose effects depend
on the effects of its function arguments. 

For example, we can write an effect polymorphic map function:

```flix
def map(f: a -> b \ ef, l: List[a]): List[b] \ ef = ...
                    ^^ // effect variable      ^^ effect variable
```

The type and effect signature of `map` states: If `map` is given a function `f`
with effects `ef` then calling `map` has the effects `ef`. That is, if `f` is
pure (i.e. has no effects) then the call to `map` will be pure. If `f` has the
`IO` effect then the call to `map` will have the `IO` effect: 


```flix
List.map(x -> x + 1, l)               // has the { } effect (i.e., is pure)
List.map(x -> {println(x); x + 1}, l) // has the { IO } effect
```

A higher-order function that takes multiple function arguments may combine their
effects.

For example, the Flix Standard Library definition of forward function
composition `>>`takes two functions `f` and `g`, and composes them: 

```flix
def >>(f: a -> b \ ef1, g: b -> c \ ef2): a -> c \ (ef1 + ef2) = x -> g(f(x))
```

The type and effect signature of `>>` states: If `map` is given two functions
`f` with effects `ef1` and `g` with effects `ef2` then it returns a new function
which has the union of effects `ef1 + ef2`. 

In Flix, the language of effects is based on set formulas:

- The *complement* of `ef` is written `~ef`.
- The *union* of `ef1` and `ef2` is written `ef1 + ef2`.
- The *intersection* of `ef1` and `ef2` is written `ef1 & ef2`.
- The *difference* of `ef1` and `ef2` is written `ef1 - ef2`.

By far the most common operation is to compute the union of effects.

It's important to understand that there can be several ways to write the same
effect set. For example, `ef1 + ef2` is equivalent to `ef2 + ef1`, as one would
expect. 

## Effect Exclusion

A novel feature of Flix is its support for [effect
exclusion](https://dl.acm.org/doi/abs/10.1145/3607846). In simple terms, effect
exclusion allows us to write higher-order functions that disallow specific
effects while allowing all other effects. 

For example, we can write an event listener registration function: 

```flix
def onClick(listener: KeyEvent -> Unit \ (ef - Block), ...): ... 
```

Here the `onClick` function takes an event listener that may have _any_ effect,
_except_ the `Block` effect. Hence listener can perform any action, except for
an action that would block the UI thread.

As another example, we can write an exception handler function:

```flix
def recoverWith(f: Unit -> a \ Throw, h: ErrMsg -> a \ (ef - Throw)): a = ... 
```

Here the `recoverWith` function takes two function arguments: the function `f`
that may throw an exception and a handler `h` which can handle the error.
Notably, the effect system enforces that `h` cannot itself throw an exception.

## Sub-Effecting

> **Note:** This feature is not yet enabled.

Flix supports _sub-effecting_ which allows an expression or a function to
_widen_ its effect set. 

For example, if we write:

```flix
if (???) { x -> x + 1 } else { x -> {println(x); x + 1}}
```

The first branch should have type `Int32 -> Int32 \ { }` (i.e. it is pure)
whereas the second branch has type `Int32 -> Int32 \ { IO }`. Without
sub-effecting these two types are incompatible because `{ } != { IO }`. However,
because of sub-effecting, Flix gives the first branch the type `Int32 -> Int32 \
ef` for some fresh effect variable `ef`. This allows type inference to _widen_
the effect of the first branch to `IO`. Hence the compiler is able to type check
the whole expression. 

As another example:

```flix
def handle(f: Unit -> a \ (ef + Throw)): a = ...
```

Here the `handle` function expects a function argument `f` with the `Throw`
effect. However, due to sub-effecting, we can still call the `handle` function
with a pure function, i.e.:

```flix
def handle(x -> Throw.throw(x))    // OK, has the `Throw` effect.
def handle(x -> x)                 // OK, because of sub-effecting.
def handle(x -> println(x))        // Not OK, handle does not permit `IO`.
```

Flix also allows sub-effect in instance declarations. 

For example, we can define the trait:

```flix
trait Foo[t] {
    def f(x: t): Bool \ { IO }
}
```

where `f` has the `IO` effect. We can implement it: 

```flix
instance Foo[Int32] {
    def f(x: Int32): Bool = x == 0 // Pure function
}
```

The declared effect of `f` is `IO`, but here the implementation of `f` is pure
(i.e., it has the empty effect set `{ }`). The program still type checks because
`{ }` can be widened to `IO`.

Flix, however, does not allow sub-effecting for top-level functions.

For example, if we declare the function:

```flix
def foo(): Bool \ IO = true
```

The Flix compiler emits the error message:

```
❌ -- Type Error ------------------------------

>> Expected type: 'IO' but found type: 'Pure'.

1 | def foo(): Bool \ IO = true
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    expression has unexpected type.
```

In summary, Flix allows effect widening in two cases: for (a) lambda expressions
and (b) instance definitions. We say that Flix supports _abstraction site
sub-effecting_ and _instance definition sub-effecting_. 
-->
