# プリミティブエフェクト

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/primitive-effects.html)を参照してください。

> **Note:** このページは少しだけ更新されており、書き直しが予定されています。

Flix には、あらかじめ定義された一連のプリミティブエフェクト（primitive effect）が用意されています。代数エフェクト（algebraic effect）やヒープエフェクト（heap effect）とは異なり、プリミティブエフェクトはハンドルすることができず、スコープから外れることもありません。プリミティブエフェクトは、マシン上で発生する副作用を表します。それは取り消したり、再解釈したりすることはできません。

最も重要なプリミティブエフェクトは `IO` エフェクトです。

## `IO` エフェクト

`IO` エフェクトは、プログラムの外側の世界と相互作用するあらゆるアクションを表します。そのようなアクションには、コンソールへの出力、ファイルの作成・読み込み・書き込み、ネットワークへのアクセスなどが含まれます。`IO` は、外側の世界を _変更する_ アクション（例：ファイルの変更）だけでなく、外側の世界に単に _アクセスする_ アクション（例：現在時刻の取得）も表します。純粋関数とは異なり、`IO` エフェクトを持つ関数は、たとえ引数が同じであっても、呼び出されるたびに振る舞いが変わる可能性があります。たとえば、同じファイルを2回読み込んでも、2回のアクセスの間にファイルが変更されているかもしれないため、同じ結果が返るとは限りません。

`IO` エフェクト、そして他のすべてのプリミティブエフェクトは _伝播的（viral）_ です。ある関数がプリミティブエフェクトを持つ場合、その呼び出し元もすべて同じプリミティブエフェクトを持つことになります。つまり、いったん不純さに染まってしまうと、染まったままであり続けるのです。

## その他のプリミティブエフェクト

- **NonDet**: `NonDet` エフェクトは、ほぼ純粋な計算を表します。たとえば、コインを投げる関数は事実上純粋です。副作用を持ちません。しかし、同じ引数を与えられても、異なる結果を返す可能性があります。

<!--
# Primitive Effects

> **Note:** This page is slightly updated and pending a rewrite.

Flix comes with a collection of pre-defined primitive effects. Unlike algebraic
and heap effects, primitive effects cannot be handled and never go out of scope.
A primitive effect represents a side-effect that happens on the machine. It
cannot be undone or reinterpreted.

The most important primitive effect is the `IO` effect.

## The `IO` Effect

The `IO` effect represents any action that interacts with the world outside the
program. Such actions include printing to the console, creating, reading, and
writing files, accessing the network, and more. The `IO` represents actions that
_change_ the outside world (e.g., modifying a file) but also actions that merely
_access_ the outside world (e.g., retrieving the current time). Unlike a pure
function, a function with the `IO` effect may change behavior every time it is
called, even if its arguments are the same. For example, reading the same file
twice is not guaranteed to return the same result since the file may have
changed between the two accesses.

The `IO` effect, and all other primitive effects, are _viral_. If a function has
a primitive effect, all its callers will also have that primitive effect. That
is to say, once you have tainted yourself with impurity, you remain tainted. 

## The Other Primitive Effects

- **NonDet**: The `NonDet` effect represents an almost pure computation. For
  example, a function that flips a coin is virtually pure; it has no
  side-effects. Yet, it may return different results, even when given the same
  arguments.
-->
