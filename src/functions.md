# 関数

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/functions.html)を参照してください。

関数と高階関数(Higher-order function)は、関数型プログラミング言語における重要な構成要素です。

Flix では、トップレベルの関数は `def` キーワードを使って定義します。例えば次のようになります：

```flix
def add(x: Int32, y: Int32): Int32 = x + y + 1
```

定義は、関数名に続いて引数リスト、戻り値の型、そして関数本体から構成されます。Flix は型推論をサポートしていますが、トップレベルの関数定義では引数の型と戻り値の型を宣言する必要があります。

Flix では、すべての関数の引数とローカル変数は使用されなければなりません。もし関数の引数が使用されない場合は、未使用であることを明示するためにアンダースコアを接頭辞として付ける必要があります。

## 高階関数

_高階関数(Higher-order function)_ とは、それ自体が関数であるパラメータを受け取る関数のことです。例えば次のようになります：

```flix
def twice(f: Int32 -> Int32, x: Int32): Int32 = f(f(x))
```

ここで `twice` 関数は、関数 `f` と整数 `x` という 2 つの引数を受け取り、`f` を `x` に 2 回適用します。

`twice` 関数にはラムダ式(Lambda expression)を渡すことができます：

```flix
twice(x -> x + 1, 42)
```

これは `42` が 2 回インクリメントされるため、`44` に評価されます。

また、2 つの引数を受け取る関数を必要とする高階関数を定義することもできます：

```flix
def twice(f: (Int32, Int32) -> Int32, x: Int32): Int32 =
    f(f(x, x), f(x, x))
```

これは次のように呼び出すことができます：

```flix
twice((x, y) -> x + y, 42)
```

高階関数は、次のようにトップレベルの関数を渡して呼び出すこともできます：

```flix
def inc(x: Int32): Int32 = x + 1

def twice(f: Int32 -> Int32, x: Int32): Int32 = f(f(x))

twice(inc, 42)
```

## 関数型の構文

関数の引数の数に応じて、関数型の構文は異なります：

```flix
Unit -> Int32                // 引数を取らない関数の場合
Int32 -> Int32               // 1 引数の関数の場合
(Int32, Int32, ...) -> Int32 // それ以外の場合
```

## 関数合成

Flix は、関数合成(Function composition)とパイプライン処理のためのいくつかの演算子をサポートしています：

```flix
let f = x -> x + 1;
let g = x -> x * 2;
let h = f >> g;     // x -> g(f(x)) と同等
```

ここで `>>` は前方関数合成(forward function composition)です。

また、パイプライン演算子(Pipeline operator)を使って関数適用を記述することもできます：

```flix
List.range(1, 100) |>
List.filter(x -> x `Int32.mod` 2 == 0) |>
List.map(x -> x * x) |>
println;
```

ここで `x |> f` は、関数適用 `f(x)` と同等です。

## デフォルトでカリー化

関数はデフォルトでカリー化(curried)されています。カリー化された関数は、宣言している引数の数より少ない引数で呼び出すことができ、残りの引数を受け取る新しい関数を返します。例えば次のようになります：

```flix
def sum(x: Int32, y: Int32): Int32 = x + y

def main(): Unit \ IO =
    let inc = sum(1);
    inc(42) |> println
```

ここで `sum` 関数は `x` と `y` という 2 つの引数を受け取りますが、`main` 内では 1 つの引数だけで呼び出されています。この呼び出しは、`sum` と似た新しい関数を返しますが、この関数では `x` が常に `1` に束縛されている点が異なります。したがって、`inc` を `42` で呼び出すと `43` が返されます。

カリー化は、多くのプログラミングパターンで役立ちます。例えば、`List.map` 関数を考えてみましょう。この関数は、型 `a -> b` の関数と型 `List[a]` のリストという 2 つの引数を受け取り、その関数をリストのすべての要素に適用して得られる `List[b]` を返します。さて、カリー化とパイプライン演算子 `|>` を組み合わせると、次のように書くことができます：

```flix
def main(): Unit \ IO =
    List.range(1, 100) |>
    List.map(x -> x + 1) |>
    println
```

ここで `List.map` の呼び出しには関数 `x -> x + 1` が渡されており、これはリスト引数を期待する新しい関数を _返します_。このリスト引数は、パイプライン演算子 `|>` によって供給されます。この場合、`|>` はリストと、リストを受け取る関数を期待しています。

## パイプライン

Flix はパイプライン演算子 `|>` をサポートしています。これは単に関数適用の前置版です（つまり、引数が関数より前に現れます）。

パイプライン演算子は、関数型のコードをより読みやすくするためにしばしば使うことができます。例えば次のようになります：

```flix
let l = 1 :: 2 :: 3 :: Nil;
l |>
List.map(x -> x * 2) |>
List.filter(x -> x < 4) |>
List.count(x -> x > 1)
```

もう一つの例を示します：

```flix
"Hello World" |> String.toUpperCase |> println
```

## 演算子

Flix には、いくつかの組み込みの単項演算子と中置演算子(Infix operator)があります。さらに Flix では、関数名をバッククォートで囲むことで中置関数適用(infix function application)をサポートしています。例えば次のようになります：

```flix
123 `sum` 456
```

これは、通常の関数呼び出しと同等です：

```flix
sum(123, 456)
```

さらに、演算子名（`+`、`-`、`*`、`<`、`>`、`=`、`!`、`&`、`|`、`^`、`$` の組み合わせ）で名付けられた関数も、中置記法で使うことができます。例えば次のようになります：

```flix
def <*>(x: Int32, y: Int32): Int32 = ???
```

これは次のように使うことができます：

```flix
1 <*> 2
```

<!--
# Functions

Functions and higher-order functions are the key
building block of a functional programming language.

In Flix, top-level functions are defined with the
`def` keyword.
For example:

```flix
def add(x: Int32, y: Int32): Int32 = x + y + 1
```

A definition consists of the function name followed
by an argument list, the return type, and the
function body.
Although Flix supports type
inference, top-level function definitions must
declare the type of their arguments and their return
type.

In Flix, all function arguments and local variables
must be used.
If a function argument is not used it must be
prefixed with an underscore to explicitly mark it as
unused.

## Higher-Order Functions

A _higher-order function_ is a function that takes a
parameter which is itself a function.
For example:

```flix
def twice(f: Int32 -> Int32, x: Int32): Int32 = f(f(x))
```

Here the `twice` function takes two arguments, a
function `f` and an integer `x`, and applies `f` to
`x` two times.

We can pass a lambda expression to the `twice`
function:

```flix
twice(x -> x + 1, 42)
```

which evaluates to `44` since `42` is incremented
twice.

We can also define a higher-order function that
requires a function which takes two arguments:

```flix
def twice(f: (Int32, Int32) -> Int32, x: Int32): Int32 =
    f(f(x, x), f(x, x))
```

which can be called as follows:

```flix
twice((x, y) -> x + y, 42)
```

We can call a higher-order function with a top-level
function as follows:

```flix
def inc(x: Int32): Int32 = x + 1

def twice(f: Int32 -> Int32, x: Int32): Int32 = f(f(x))

twice(inc, 42)
```

## Function Type Syntax

Depending on the number of arguments to a function,
the syntax for the function type differs:

```flix
Unit -> Int32                // For nullary functions
Int32 -> Int32               // For unary functions
(Int32, Int32, ...) -> Int32 // For the rest
```

## Function Composition

Flix supports several operators for function
composition and pipelining:

```flix
let f = x -> x + 1;
let g = x -> x * 2;
let h = f >> g;     // equivalent to x -> g(f(x))
```

Here `>>` is forward function composition.

We can also write function applications using the
pipeline operator:

```flix
List.range(1, 100) |>
List.filter(x -> x `Int32.mod` 2 == 0) |>
List.map(x -> x * x) |>
println;
```

Here `x |> f` is equivalent to the function
application `f(x)`.

## Curried by Default

Functions are curried by default.
A curried function can be called with fewer
arguments than it declares returning a new function
that takes the remainder of the arguments.
For example:

```flix
def sum(x: Int32, y: Int32): Int32 = x + y

def main(): Unit \ IO =
    let inc = sum(1);
    inc(42) |> println
```

Here the `sum` function takes two arguments, `x` and
`y`, but it is only called with one argument inside
`main`.
This call returns a new function which is
similar to `sum`, except that in this function `x`
is always bound to `1`.
Hence when `inc` is called with `42` it returns `43`.

Currying is useful in many programming patterns.
For example, consider the `List.map` function.
This function takes two arguments, a function of
type `a -> b` and a list of type `List[a]`, and
returns a `List[b]` obtained by applying the
function to every element of the list.
Now, if we combine currying with the pipeline
operator `|>` we are able to write:

```flix
def main(): Unit \ IO =
    List.range(1, 100) |>
    List.map(x -> x + 1) |>
    println
```

Here the call to `List.map` passes the function
`x -> x + 1` which _returns_ a new function that
expects a list argument.
This list argument is then supplied by the pipeline
operator `|>` which, in this case, expects a list
and a function that takes a list.

## Pipelines

Flix supports the pipeline operator `|>` which is
simply a prefix version of function application (i.e.
the argument appears before the function).

The pipeline operator can often be used to make
functional code more readable.
For example:

```flix
let l = 1 :: 2 :: 3 :: Nil;
l |>
List.map(x -> x * 2) |>
List.filter(x -> x < 4) |>
List.count(x -> x > 1)
```

Here is another example:

```flix
"Hello World" |> String.toUpperCase |> println
```

## Operators

Flix has a number of built-in unary and infix operators.
In addition Flix supports infix function application by enclosing
the function name in backticks. For example:

```flix
123 `sum` 456
```

is equivalent to the normal function call:

```flix
sum(123, 456)
```

In addition, a function named with an operator name (some combination of `+`, `-`, `*`, `<`, `>`, `=`, `!`, `&`, `|`, `^`, and `$`) can also be used infix. For example:

```flix
def <*>(x: Int32, y: Int32): Int32 = ???
```

can be used as follows:

```flix
1 <*> 2
```
-->
