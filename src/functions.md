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

## First-Class and Higher-Order Functions

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
List.filter(x -> x mod 2 == 0) |>
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

## Pure, Impure, and Effect Polymorphic Functions

In Flix every function is pure, impure, or effect
polymorphic.

The Flix type and effect system ensures that a pure
function always returns the same result when given
the same arguments and that it cannot have
(observable) side effects.

In Flix every function definition is _implicitly_
marked as `Pure`.
For example, the function definition:

```flix
def add(x: Int32, y: Int32): Int32 = x + y
```

is actually equivalent to:

```flix
def add(x: Int32, y: Int32): Int32 \ {} = x + y
```

A function that prints to the console is `Impure`
and must be marked as such:

```flix
def addAndPrint(x: Int32, y: Int32): Int32 \ IO =
    let r = x + y;
    println(r);
    r
```

since the type signature of the library function
`println` specifies that it is `Impure`.

The purity (or impurity) of a higher-order function
may depend on the purity of its argument(s).
For example, whether `List.map` is pure or impure
depends on whether function we map is pure or
impure.
Fortunately Flix can model such behavior using
_effect polymorphism_.
For example:

```flix
def map(f: a -> b \ ef, l: List[a]): List[b] \ ef = ???
```

Here the signature of `map` captures that if the
function argument `f` has type `a -> b` with effect
`ef` then the effect of `map` itself is `ef`.
This means that if `map` is called with a pure
(resp. impure) function argument then the overall
expression is pure (resp. impure).
For example:

```flix
List.map(x -> x + 123, l)    // pure
List.map(x -> println(x), l) // impure
```

#### Design Note

The Flix standard library enforces several program
invariants using purity.
For example, in Flix, the `Eq` and `Order` type
classes require that their operations are pure.
This ensures that collections, such as lists, sets,
and maps, do not leak internal implementation
details.
