# エフェクトとハンドラ

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/effects-and-handlers.html)を参照してください。

Flix は、[Eff](https://www.eff-lang.org/) や [Koka](https://koka-lang.github.io/) のスタイルで、代数的エフェクト(algebraic effects)とハンドラ(handlers)をサポートしています。

Flix のエフェクトハンドラは、動的スコープ(dynamic scope)、ディープハンドラ(deep handlers)を用い、複数回の再開(multiple resumptions)をサポートしています。

このセクションではエフェクトとハンドラを紹介しますが、あわせて次の資料にも目を通すことをおすすめします。

- [An Introduction to Algebraic Effects and Handlers](https://www.eff-lang.org/handlers-tutorial.pdf) &mdash; Matija Pretnar

まずは、ほとんどのプログラマになじみのある種類のエフェクト、すなわち *例外(exceptions)* から始めましょう。

## 再開不可能なエフェクト: 例外

エフェクトとハンドラを使って例外を実装できます。たとえば次のようになります。

```flix
eff DivByZero {
    def divByZero(): Void
}

def divide(x: Int32, y: Int32): Int32 \ DivByZero = 
    if (y == 0) {
        DivByZero.divByZero()
    } else {
        x / y
    }

def main(): Unit \ IO = 
    run {
        println(divide(3, 2));
        println(divide(3, 0))
    } with handler DivByZero {
        def divByZero(_resume) = println("Oops: Division by Zero!")
    }
```

ここでは `DivByZero` エフェクトを宣言し、`divide` 関数の中でそれを使っています。そのため `divide` 関数は `DivByZero` エフェクトを持ちます。`main` では2つの除算を行います。1つ目は成功して `1` を出力します。2つ目は失敗してエラーメッセージを出力します。継続(continuation)である `_resume` は使われておらず、その引数の型が `Void` であるため使うこともできません。`main` 関数はハンドラの中で `println` を使っているため `IO` エフェクトを持ちますが、`DivByZero` エフェクトは処理済みであるため、それは持ち _ません_。

例外が再開不可能(non-resumable)であるのは、いったん例外が送出されると、例外が投げられた場所から実行を再開できないからです。できるのは、例外を処理して別のことを行うことだけです。`DivByZero` が例外であると分かるのは、そのエフェクト操作が `Void` の戻り値型を持つからです。

> **注意:** `Void` 型は、Flix に組み込まれた空の型、すなわち値を持たない(uninhabited)型です。戻り値型が `Void` の関数は正常に返ることができず、異常な形で（たとえば例外を投げることで）のみ返ります。同様に、`Void` 型の引数を取る関数は呼び出すことができません。

Flix は[エフェクト多相(effect polymorphism)](./effect-polymorphism.md)をサポートしていることを思い出してください。そのため、次のコードは問題なく動作します。

```flix
def main(): Unit \ IO = 
    let l = List#{1, 2, 0, 3};
    run {
        List.map(x -> println(divide(42, x)), l);
        ()
    } with handler DivByZero {
        def divByZero(_) = println("Oops: Division by Zero!")
    }
```

このプログラムは次を出力します。

```
42
21
Oops: Division by Zero!
```

これは、`divide` の最初の2回の呼び出しは成功する一方で、最後の呼び出しが `DivByZero` 例外を送出するからです。特筆すべきは、Flix の型およびエフェクトシステムが、`List.map` へのエフェクト多相な呼び出しを通じて例外エフェクトを追跡できるという点です。

## 再開可能なエフェクト

Flix は再開可能(resumable)なエフェクトもサポートしています。たとえば次のようになります。

```flix
import java.time.LocalDateTime

eff HourOfDay {
    def getCurrentHour(): Int32
}

def greeting(): String \ {HourOfDay} = 
    let h = HourOfDay.getCurrentHour();
    if (h <= 12) 
        "Good morning"
    else if (h <= 18)
        "Good afternoon"
    else 
        "Good evening"

def main(): Unit \ IO = 
    run {
        println(greeting())
    } with handler HourOfDay {
        def getCurrentHour(_, resume) = 
            let dt = LocalDateTime.now();
            resume(dt.getHour())
    }
```

ここでは、その日の現在の時刻を返す1つの操作を持つエフェクト `HourOfDay` を宣言しています。次に、`HourOfDay` エフェクトを使って現在時刻に応じた挨拶を返す `greeting` 関数を定義します。最後に `main` で `greeting` を呼び出し、その結果を出力します。特に、`HourOfDay` のハンドラは Java 相互運用を使って現在の時刻を取得しています。

重要なのは、エフェクト `getHourOfDay` が呼び出されると、Flix が現在の継続をキャプチャし、（`main` にある）もっとも近いハンドラを見つけ、そのハンドラがシステムクロックから取得したその日の現在時刻を使って `greeting` の内部から計算を **再開(resume)** するという点です。

## 複数のエフェクトとハンドラ

複数のエフェクトを使う関数を書くことができます。

```flix
eff Ask {
    def ask(): String
}

eff Say {
    def say(s: String): Unit
}

def greeting(): Unit \ {Ask, Say} = 
    let name = Ask.ask();
    Say.say("Hello Mr. ${name}")

def main(): Unit \ IO = 
    run {
        greeting()
    } with handler Ask {
        def ask(_, resume) = resume("Bond, James Bond")
    } with handler Say {
        def say(s, resume) = { println(s); resume() }
    }
```

ここでは `Ask` と `Say` という2つのエフェクトを宣言しています。`Ask` エフェクトは消費者(consumer)です。すなわち、環境から文字列を必要とします。`Say` エフェクトは生産者(producer)です。すなわち、環境へ文字列を渡します。`greeting` ではこの両方のエフェクトを使っています。`main` では `greeting` を呼び出し、それぞれのエフェクトを処理します。`Ask` エフェクトは、常に文字列 `"Bond, James Bond"` で継続を再開することによって処理します。`Say` エフェクトは、コンソールに出力してから継続を再開することによって処理します。

## 複数回の再開

Flix は、複数回の再開を伴う代数的エフェクトをサポートしています。このようなエフェクトを使うと、async/await、バックトラッキング探索、協調的マルチタスクなどを実装できます。

次は簡単な例です。

```flix
eff Amb {
    def flip(): Bool
}

eff Exc {
    def raise(m: String): Void
}

def drunkFlip(): String \ {Amb, Exc} = {
    if (Amb.flip()) {
        let heads = Amb.flip();
        if (heads) "heads" else "tails"
    } else {
        Exc.raise("too drunk to flip")
    }
}

def handleAmb(f: a -> b \ ef): a -> List[b] \ ef - Amb =  
    x -> run {
        f(x) :: Nil
    } with handler Amb {
        def flip(_, resume) = resume(true) ::: resume(false)
    }

def handleExc(f: a -> b \ ef): a -> Option[b] \ ef - Exc = 
    x -> run {
        Some(f(x))
    } with handler Exc {
        def raise(_, _) = None
    }


def main(): Unit \ IO = {
    // 出力: Some(heads) :: Some(tails) :: None :: Nil
    handleAmb(handleExc(drunkFlip))() |> println;

    // 出力: None
    handleExc(handleAmb(drunkFlip))() |> println
}
```

ここでは `Amb`（ambiguous の略）と `Exc`（exception の略）という2つのエフェクトを宣言しています。次に `drunkFlip` 関数を定義します。これは、コインを投げようとする酔っ払いをモデル化するというアイデアです。**第1に**、その男がコインを投げられるか、それとも落としてしまうかを決めるためにコインを投げます。**第2に**、コイン投げが成功した場合、表(heads)か裏(tails)かを得るためにもう一度コインを投げます。重要なのは、`drunkFlip` が概念的に「heads」「tails」「too drunk」という3つの結果を持つという点です。

次に、`handleAmb` と `handleExc` という2つのエフェクトハンドラを定義します。後者から見ていくと、`Exc` ハンドラは例外を捕捉して `None` を返します。例外が送出されなければ、計算された値の `Some(x)` を返します。`Amb` ハンドラは、`true` と `false` で継続を **2回** 呼び出し、その結果をリストに収集することで `flip` エフェクトを処理します。言い換えると、`Amb` ハンドラはコイン投げの **両方** の結果を探索します。

`main` ではこの2つのエフェクトハンドラを使います。特筆すべきは、*ハンドラのネストの順序が重要である* という点です！ `Exc` エフェクトを先に処理すると、リスト `Some(heads) :: Some(tails) :: None :: Nil` が得られます。一方、`Exc` を最後に処理すると、計算全体が `None` で失敗します。

## 代数的エフェクトとモナド

Flix は、代数的エフェクトハンドラと[モナド(monads)](./monadic-for-yield.md)の両方をサポートしています。これは、両方のプログラミングスタイルをサポートしたいからです。

- エフェクトハンドラを使ってプログラミングしたければ、そうできます。

- ファンクタ(functors)、アプリカティブファンクタ(applicative functors)、モナドを使ってプログラミングしたければ、そうできます。

Flix は（まだ）`IO` モナドを定義していませんが、自分で作ることはできます。

Flix の標準ライブラリは、ハイブリッドな方法に偏っています。外界とのやり取りをモデル化するには代数的エフェクトを使いますが、単純なエラー処理には `Option` や `Result` データ型を好みます。`Option` や `Result` を扱うのは、[モナド構文(monadic syntax)](./monadic-for-yield.md)を使うとより快適になります。

## 制限: 多相エフェクト

Flix の型およびエフェクトシステムは、多相エフェクト(polymorphic effects)をまだサポートしていません。[^1]

たとえば、多相的な `Throw[a]` エフェクトを宣言することは *できません*。

```flix
eff Throw[a] {
    def throw(x: a): Void
}
```

Flix コンパイラは次のエラーメッセージを出力します。

```
❌ -- Syntax Error --

>> Unexpected effect type parameters.

1 | eff Throw[a] {
              ^
              unexpected effect type parameters
```

残念ながら、異なる型の値を投げる必要がある場合は、別々のエフェクトを宣言しなければなりません。

たとえば次のようになります。

```flix
eff ThrowBool {
    def throw(x: Bool): Void
}

eff ThrowInt32 {
    def throw(x: Int32): Void
}
```

## new object 式と spawn 式における未処理のエフェクト

Flix は、new object 式でも spawn 式でも、未処理のエフェクトを許可しません。

たとえば、次のように書くと、

```flix
eff Ask {
    def ask(): String
}

def main(): Unit \ IO = 
    region rc {
        spawn Ask.ask() @ rc
    }
```

Flix コンパイラは次のエラーメッセージを出力します。

```
-- Safety Error -------------------------------------------------- 

>> Illegal spawn effect: 'Ask'. 

>> A spawn expression must be pure or have a primitive effect.

7 |         spawn do Ask.ask() @ rc
                  ^^^^^^^^^^^^
                  illegal effect.
```

[^1]: この制限を取り除く方法を、現在調査中です。

<!--
# Effects and Handlers

Flix supports algebraic effects and handlers in the style of
[Eff](https://www.eff-lang.org/) and [Koka](https://koka-lang.github.io/). 

Flix effect handlers use dynamic scope, deep handlers, and support multiple
resumptions.

In this section, we introduce effects and handlers, but we also recommend the
reader take a look at: 

- [An Introduction to Algebraic Effects and Handlers](https://www.eff-lang.org/handlers-tutorial.pdf) &mdash; Matija Pretnar

We begin a type of effect most programmers are familiar with: *exceptions*.

## Non-Resumable Effects: Exceptions

We can use effects and handlers to implement exceptions. For example:

```flix
eff DivByZero {
    def divByZero(): Void
}

def divide(x: Int32, y: Int32): Int32 \ DivByZero = 
    if (y == 0) {
        DivByZero.divByZero()
    } else {
        x / y
    }

def main(): Unit \ IO = 
    run {
        println(divide(3, 2));
        println(divide(3, 0))
    } with handler DivByZero {
        def divByZero(_resume) = println("Oops: Division by Zero!")
    }
```

Here we declare the effect `DivByZero` and use it inside the `divide` function.
Hence the `divide` function has the `DivByZero` effect. In `main` we perform two
divisions. The first succeeds and prints `1`. The second fails and prints an
error message. The continuation, `_resume`, is unused and cannot be used because
its argument type is `Void`. The `main` function has the `IO` effect since we
use `println` in the handler, but it does _not_ have the `DivByZero` effect
since that has been handled.

Exceptions are non-resumable because once an exception has been raised, we
cannot resume execution from where the exception was thrown. We can only handle
the exception and do something else. We know that `DivByZero` is an exception
because its effect operation has the `Void` return type. 

> **Note:** The `Void` type is an empty, i.e., uninhabited, type built into
> Flix. A function with the return type `Void` cannot return normally; it only
> returns abnormally (e.g., by throwing an exception). Similarly, a function
> that takes an argument of type `Void` cannot be called. 

Recall that Flix supports [effect polymorphism](./effect-polymorphism.md), hence
the following works without issue:

```flix
def main(): Unit \ IO = 
    let l = List#{1, 2, 0, 3};
    run {
        List.map(x -> println(divide(42, x)), l);
        ()
    } with handler DivByZero {
        def divByZero(_) = println("Oops: Division by Zero!")
    }
```

This program will print:

```
42
21
Oops: Division by Zero!
```

Because the first two calls to `divide` succeed, whereas the last call will
raise a `DivByZero` exception. Notably, the Flix type and effect system can
track the exception effect through the effect polymorphic call to `List.map`.

## Resumable Effects

Flix also supports resumable effects. For example:

```flix
import java.time.LocalDateTime

eff HourOfDay {
    def getCurrentHour(): Int32
}

def greeting(): String \ {HourOfDay} = 
    let h = HourOfDay.getCurrentHour();
    if (h <= 12) 
        "Good morning"
    else if (h <= 18)
        "Good afternoon"
    else 
        "Good evening"

def main(): Unit \ IO = 
    run {
        println(greeting())
    } with handler HourOfDay {
        def getCurrentHour(_, resume) = 
            let dt = LocalDateTime.now();
            resume(dt.getHour())
    }
```

Here we declare an effect `HourOfDay` with a single operation that returns the
current hour of the day. Next, we define the `greeting` function, which uses the
`HourOfDay` effect to return a greeting appropriate for the current time.
Lastly, in `main`, we call `greeting` and print its result. In particular, the
handler for `HourOfDay` uses Java interoperability to obtain the current hour.

What is important is that when the effect `getHourOfDay` is called, Flix
captures the current continuation and finds the closest handler (in `main`),
which **resumes** the computation from within `greeting` using the current hour
of the day, as obtained from system clock. 

## Multiple Effects and Handlers

We can write functions that use multiple effects:

```flix
eff Ask {
    def ask(): String
}

eff Say {
    def say(s: String): Unit
}

def greeting(): Unit \ {Ask, Say} = 
    let name = Ask.ask();
    Say.say("Hello Mr. ${name}")

def main(): Unit \ IO = 
    run {
        greeting()
    } with handler Ask {
        def ask(_, resume) = resume("Bond, James Bond")
    } with handler Say {
        def say(s, resume) = { println(s); resume() }
    }
```

Here we declare two effects: `Ask` and `Say`. The `Ask` effect is a consumer: it
needs a string from the environment. The `Say` effect is a producer: it passes a
string to the environment. We use both effects in `greeting`. In `main`, we call
`greeting` and handle each effect. We handle the `Ask` effect by always resuming
the continuation with the string `"Bond, James Bond"`. We handle the `Say`
effect by printing to the console and resuming the continuation.

## Multiple Resumptions

Flix supports algebraic effects with multiple resumptions. We can use such
effects to implement async/await, backtracking search, cooperative
multi-tasking, and more. 

Here is a simple example:

```flix
eff Amb {
    def flip(): Bool
}

eff Exc {
    def raise(m: String): Void
}

def drunkFlip(): String \ {Amb, Exc} = {
    if (Amb.flip()) {
        let heads = Amb.flip();
        if (heads) "heads" else "tails"
    } else {
        Exc.raise("too drunk to flip")
    }
}

def handleAmb(f: a -> b \ ef): a -> List[b] \ ef - Amb =  
    x -> run {
        f(x) :: Nil
    } with handler Amb {
        def flip(_, resume) = resume(true) ::: resume(false)
    }

def handleExc(f: a -> b \ ef): a -> Option[b] \ ef - Exc = 
    x -> run {
        Some(f(x))
    } with handler Exc {
        def raise(_, _) = None
    }


def main(): Unit \ IO = {
    // Prints: Some(heads) :: Some(tails) :: None :: Nil
    handleAmb(handleExc(drunkFlip))() |> println;

    // Prints: None
    handleExc(handleAmb(drunkFlip))() |> println
}
```

Here we declare two effects: `Amb` (short for ambiguous) and `Exc` (short for
exception). We then define the `drunkFlip` function. The idea is to model a
drunk man trying to flip a coin. **First**, we flip a coin to determine if the
man can flip the coin or if he drops it. **Second**, if the flip was successful,
we flip the coin again to obtain either heads or tails. What is important is
that `drunkFlip` conceptually has three outcomes: "heads", "tails", or "too
drunk". 

Next, we define two effect handlers: `handleAmb` and `handleExc`. Starting with
the latter, the `Exc` handler catches the exception and returns `None`. If no
exception is raised, it returns `Some(x)` of the computed value. The `Amb`
handler handles the `flip` effect by calling the continuation **twice** with
`true` and `false`, and collecting the result in a list. In other words, the
`Amb` handler explores **both** outcomes of flipping a coin. 

In `main`, we use the two effect handlers. Notably, the *nesting order of
handlers matters*! If we handle the `Exc` effect first then we obtain the list
`Some(heads) :: Some(tails) :: None :: Nil`. If, on the other hand, we handle
`Exc` last then the whole computation fails with `None`.

## Algebraic Effects and Monads

Flix supports algebraic effect handlers and [monads](./monadic-for-yield.md)
because we want to support both styles of programming: 

- If you want to program with effect handlers, you can do that. 

- If you want to program with functors, applicative functors, and monads, you can do that.

Flix does not (yet) define an `IO` monad, but you can roll your own.

The Flix Standard Library is biased towards a hybrid. We use algebraic effects
to model interaction with the outside world but prefer the `Option` and `Result`
data types for simple error handling. Working with `Option`s and `Result`s is
more pleasant with [monadic syntax](./monadic-for-yield.md).

## Limitation: Polymorphic Effects

The Flix type and effect system does not yet support polymorphic effects.[^1] 

For example, we *cannot* declare a polymorphic `Throw[a]` effect:

```flix
eff Throw[a] {
    def throw(x: a): Void
}
```

The Flix compiler emits the error message:

```
❌ -- Syntax Error --

>> Unexpected effect type parameters.

1 | eff Throw[a] {
              ^
              unexpected effect type parameters
```

Unfortunately, if we need to throw values of different types, we have to declare
different effects. 

For example:

```flix
eff ThrowBool {
    def throw(x: Bool): Void
}

eff ThrowInt32 {
    def throw(x: Int32): Void
}
```

## Unhandled Effects in New Object and Spawn Expressions

Flix does not permit unhandled effects in new object expressions nor in spawn
expressions. 

For example, if we write:

```flix
eff Ask {
    def ask(): String
}

def main(): Unit \ IO = 
    region rc {
        spawn Ask.ask() @ rc
    }
```

The Flix compiler emits the error message:

```
-- Safety Error -------------------------------------------------- 

>> Illegal spawn effect: 'Ask'. 

>> A spawn expression must be pure or have a primitive effect.

7 |         spawn do Ask.ask() @ rc
                  ^^^^^^^^^^^^
                  illegal effect.
```

[^1]: We are currently investigating how to lift this restriction.
-->
