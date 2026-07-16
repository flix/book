# エフェクトシステム

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/effect-system.html)を参照してください。

Flix は、言語に完全に統合された最先端の型およびエフェクトシステム
（type and effect system）を備えています。Flix のエフェクトシステムは
強力かつ広範であり、effect polymorphism（エフェクト多相）、
sub-effecting（サブエフェクティング）、effect exclusion（エフェクト排他）、
purity reflection（純粋性リフレクション）、associated effects（関連エフェクト）を
サポートしています。

これらの新しく刺激的な機能については、以降のページで探っていきます。

エフェクトシステムにはどのような利点があるのでしょうか。利点は数多くあります。

- **（純粋性 / Purity）** 型およびエフェクトシステムは、純粋（pure）な関数と
  純粋でない（impure）関数を分離します。Flix では、純粋な関数は一切の副作用を
  持つことができず、同じ引数を与えられたときには同じ値を返さなければなりません。
  とはいえ、純粋な関数であっても、mutable なデータ構造を使って命令型スタイルで
  実装することは可能です。ただし、それらのデータ構造が関数の終了時にスコープから
  外れる場合に限ります。

- **（推論 / Reasoning）** 型およびエフェクトシステムは、すべての関数に対して
  引数と戻り値の型、そして関数の副作用を明示することを求めることで、プログラマが
  自分のプログラムの動作を理解する助けになります。

- **（モジュール性 / Modularity）** 型およびエフェクトシステムは、プログラムの
  どこでどの副作用が許可されるかをプログラマに検討させることで、モジュール性を
  強制します。さらに、エフェクトは &mdash; 型と同じように &mdash; コンパイラに
  よって検査されるドキュメントとしての役割を果たします。

- **（エフェクトとハンドラ / Effects and Handlers）** 型およびエフェクトシステムは、
  代数的エフェクト（algebraic effects）とハンドラ（handler）の基盤となります。
  これらによって、プログラマは例外（exception）、async/await、協調的マルチタスク
  （cooperative multitasking）といった独自の制御構造を実装できるようになります。

- **（セキュリティ / Security）** 型およびエフェクトシステムは、関数の振る舞いに
  ついて鉄壁の保証を提供し、プログラマが未知のコードへの信頼を高められるように
  します。たとえば、ある関数が純粋であれば、その関数は一切の副作用を持つことが
  できません。すなわち、ファイルシステムやネットワークなどにアクセスできません。
  具体的な利点として、プログラムがサプライチェーン攻撃（supply chain attack）に
  対してより強くなります。

- **（純粋性リフレクション / Purity Reflection）** Flix 標準ライブラリ（および
  それを拡張する他のライブラリの作者）は、[purity reflection](./purity-reflection.md)
  を使って、高階関数に渡される関数引数の純粋性を検査できます。この情報を活用すれば、
  プログラムの本来の意味論を保ちながら、自動並列化を実装できます。たとえば Flix では、
  `Set.count` 関数は、(a) 集合が十分に大きく、かつ (b) 渡された述語関数が純粋である
  場合に、並列評価を使います。

- **（最適化 / Optimizations）** Flix コンパイラは、純粋性の情報を活用して、
  積極的なデッドコード除去（dead code elimination）とインライン化（inlining）を
  行います。

Flix の型およびエフェクトシステムはかなり洗練されており、効果的に使うには
ある程度の予備知識が必要です。次のいくつかの節では、型およびエフェクトシステムの
機能を順を追って紹介し、その使用例をいくつか示します。

先に進む前に、Flix には 3 種類のエフェクトがあることを理解しておくことが重要です。

- [primitive effects](./primitive-effects.md)
- [algebraic effects](./effects-and-handlers.md)
- [heap effects](./mutable-data.md)

トレイト（trait）とエフェクトがどのように相互作用するかについては、[Associated
Effects](./associated-effects.md) の節で説明します。

## ダイレクトスタイル

Flix は、伝統的な型およびエフェクトシステムを備えた、いわゆる
_ダイレクトスタイル（direct-style）_ のプログラミング言語です。これは、
[Cats Effect](https://typelevel.org/cats-effect/)、[Kyo](https://getkyo.io/#/)、
[ZIO](https://zio.dev/) のような、いわゆる _関数型エフェクトシステム
（functional effect systems）_ とは対照的です。これらのシステムは、ライブラリ
レベルのエフェクトシステム、本質的にはカスタムの `IO` モナドを提供します。
このアプローチにはいくつかの利点がありますが、欠点も少なくとも 2 つあります。
(a) 伝統的な型およびエフェクトシステムが提供する保証（たとえば、ある関数が
いつ純粋であるかを知ること）が一切得られないこと、そして (b) プログラムを
モナディックスタイル（monadic-style）で書かなければならず、これは煩雑である
ことです。

<!--
# Effect System

Flix features a state-of-the-art type and effect system fully integrated into
the language. The Flix effect system is powerful and extensive, supporting
effect polymorphism, sub-effecting, effect exclusion, purity reflection, and
associated effects.

We will explore these new and exciting features over the coming pages.

What are the benefits of an effect system? There are many:

- **(Purity)** A type and effect system separates pure and impure functions. In
  Flix, a pure function cannot have any side-effects and must return the same
  value when given the same arguments. Nevertheless, a pure function can still
  be implemented in an imperative style using mutable data structures as long as
  those data structures leave scope when the function ends.

- **(Reasoning)** A type and effect system helps programmers understand how
  their programs work by requiring every function to specify its argument and
  return types, as well as the side-effects of the function.

- **(Modularity)**  A type and effect system enforces modularity by forcing
  programmers to consider what side effects are allowed where in the program.
  Moreover, effects &mdash; like types &mdash; serve as compiler checked
  documentation.

- **(Effects and Handlers)** A type and effect system is the foundation for
  algebraic effects and handlers. These allow programmers to implement their own
  control structures, such as exceptions, async/await, and cooperative
  multitasking.

- **(Security)** A type and effect system offers iron-clad guarantees about the
  behavior of functions, allowing programmers to increase their trust in unknown
  code. For example, if a function is pure, it cannot have any side-effects: it
  cannot access the file system, the network, etc. A specific benefit is that
  programs become more resistant to supply chain attacks.

- **(Purity Reflection)** The Flix Standard Library (and other library authors
  in extension) can use [purity reflection](./purity-reflection.md) to inspect
  the purity of function arguments passed to higher-order functions. We can
  exploit this information to implement automatic parallelization while
  preserving the original semantics of the program. For example, in Flix, the
  `Set.count` function uses parallel evaluation if (a) the set is sufficiently
  large and (b) the passed predicate function is pure. 

- **(Optimizations)** The Flix compiler exploits purity information for
  aggressive dead code elimination and inlining.

The Flix type and effect system is quite sophisticated and requires some
background knowledge to use effectively. In the next couple of sections, we
gradually introduce the features of the type and effect system and give several
examples of its use. 

Before we continue, it is important to understand that Flix has three types of effects: 

- [primitive effects](./primitive-effects.md)
- [algebraic effects](./effects-and-handlers.md)
- [heap effects](./mutable-data.md)

We describe how traits and effects interact in the section on [Associated
Effects](./associated-effects.md).

## Direct Style

Flix is a so-called _direct-style_ programming language with a traditional type
and effect system. This is in contrast to so-called _functional effect systems_
like [Cats Effect](https://typelevel.org/cats-effect/),
[Kyo](https://getkyo.io/#/), and [ZIO](https://zio.dev/). These systems offer a
library-level effect system, essentially a custom `IO` monad. While this
approach has some advantages, the downsides are at least twofold (a) we do not
get any of the guarantees offered by a traditional type and effect system (e.g.,
we cannot know when a function is pure), and (b) we must write our program in a
monadic-style, which is burdensome.
-->
