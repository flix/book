# Tips & Tricks

This page documents a few features that make Flix
code easier to read and write.

## Main

The entry point of any Flix program is the `main`
function which *must* have the signature:

```flix
def main(): Unit & Impure
```

That is, the `main` function

1. must return `Unit`, and
2. must be `Impure`.

The signature of `main` does not specify any
arguments, but the command line arguments passed to
the program can be accessed by calling
`Environment.getArgs()`.

```flix
def main(): Unit & Impure=
    let args = Environment.getArgs();
    ...
```

Flix requires main to be `Impure`.
If main was pure there would be no reason to run the
program.
Typically the impurity requirement is satisfied
because main prints to the console or has another
side-effect.

## Printing to Standard Out

The Flix prelude defines two impure functions:
`print` and `println` that can be used to print a
string to standard out.
For example:

```flix
println("Hello World")
```


The `println` function prints with a newline after the string.
The `print` function can be used to print without this newline.
For example:


```flix

let name = "Lucky Luke";
print("Hello");
print(" ");
println(name)

```


which prints `Hello Lucky Luke` on one line.



The `print` and `println` functions can print any value whose type
implements `ToString` type class and consequently can be converted to
a `String`. For example:


```flix

let o = Some(123);
let l = 1 :: 2 :: 3 :: Nil;
println(o);
println(l)

```


The `print` and `println` functions are rightfully `Impure`.
Consequently they cannot be called from a pure context. This can sometimes hinder debugging of a
pure function where you want to log some intermediate computation.
A solution is to cast the `print` and `println` functions as
`Pure`. Here is an example:


```flix

def sum(x: Int32, y: Int32): Int32 = 
let _ = println(x) as & Pure;
let _ = println(y) as & Pure;
x + y

```


Note that `sum` remains a pure function despite the two calls
to `println`. Moreover, since the call `println(x)` is pure
we must introduce a let-binding with an unused variable to prevent Flix from rejecting the
program due to a redundant pure computation.




## String Interpolation


Flix strings support interpolation. Inside a string the
form `{"${e}"}` evaluates `e` to a value and converts it to a string using
the `ToString` type class. For example:


```flix

let fstName = "Lucky";
let lstName = "Luke";
"Hello Mr. \${lstName}. Do you feel \${fstName}, punk?"

```


String interpolation works for any types that implements a `ToString` instance. For
example:


```flix

let i = 123;
let o = Some(123);
let l = 1 :: 2 :: 3 :: Nil;
"i = \${i}, o = \${o}, l = \${l}"

```


String interpolations may contain arbitrary expressions. For example:


```flix

let x = 1;
let y = 2;
"\${x + y + 1}"

```


String interpolation is the preferred way to concatenate two strings:


```flix

let x = "Hello";
let y = "World";
"\${x}\${y}" // equivalent to x + y

```


String interpolation is the preferred way to convert a value to a string:


```flix

let o = Some(123);
"\${o}"

```


which is equivalent to an explicit use of the `toString` function from
the `ToString` type class:


```flix

ToString.toString(o)

```


String interpolators may nest, but this is strongly discouraged.




## Pipelines


Flix supports the pipeline operator `|>` which is simply a prefix version of function
application (i.e. the argument appears before the function).



The pipeline operator can often be used to make functional code more readable. For example:


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



## Shorthand for Enum Declarations


A typical enum may look like:


```flix
enum Weekday {
case Monday,
case Tuesday,
case Wednesday,
case Thursday,
case Friday,
case Saturday,
case Sunday
}
```


The same enum can also be declared as:


```flix
enum Weekday {
case Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
}
```


This shorthand syntax is always available, but should only be used for simple enums.




## Let Pattern Match


In addition to the pattern `match` construct, a let-binding can be used to destruct a
value. For example:


```flix
let (x, y, z) = (1, 2, 3)
```


Binds the variables `x`, `y`, and `z` to the
values `1`, `2`, and `3`, respectively.



Any exhaustive pattern may be used in a let-binding. For example:


```flix
let (x, Foo(y, z)) = (1, Foo(2, 3))
```


is legal provided that the `Foo` constructor belongs to a type where it is the only
constructor.



The following let-bindings are *illegal* because they are not exhaustive:


```flix

let (1, 2, z) = ...
let Some(x) = ...

```


The Flix compiler will reject such non-exhaustive patterns.




## Match Lambdas


Pattern matches can also be used with lambda expressions.
For example:


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


Here `f` is a function that expects *three* `Int32` arguments,
whereas `g` is a function that expects *one* three tuple `(Int32, Int32,
Int32)` argument.




## Infix Application


Flix supports infix function application by enclosing the function name in backticks.
For example:


```flix
123 \`sum\` 456
```


is equivalent to the normal function call:


```flix
sum(123, 456)
```



## Built-in Literals

Flix has built-in syntactic sugar for lists, sets, and maps.

### List Literals


A list literal is written using the infix `::` constructor.
For example:


```flix
1 :: 2 :: 3 :: Nil
```


which is syntactic sugar for:


```flix
Cons(1, Cons(2, Cons(3, Nil)))
```



### Set Literals


A set literal is written using the notation `
Set#{v1, v2, ...}
`.
For example:


```flix
Set#{1, 2, 3}
```


which is syntactic sugar for:


```flix
Set.insert(1, Set.insert(2, Set.insert(3, Set.empty())))
```



### Map Literals


A map literal is written using the notion `
Map#{k1 => v1, k2 => v2, ...}
`.
For example:


```flix
Map#{1 => "Hello", 2 => "World"}
```


which is syntactic sugar for:


```flix
Map.insert(1, "Hello", Map.insert(2, "World", Map.empty()))
```





## Let* (Do-notation)


Flix supports a feature similar to *do-notation* in Haskell
and *for-comprehensions* in Scala.



The following monadic code:


```flix
use Option.flatMap;
let o1 = Some(21);
let o2 = Some(42);
flatMap(x -> flatMap(y -> Some(x + y), o2), o1)
```


May be expressed more concisely as:


```flix
use Option.flatMap;
let* o1 = Some(21);
let* o2 = Some(42);
Some(x + y) 
```


where each `let*` corresponds to a `flatMap` use.


#### DesignNote

This feature is experimental and subject to change.




## Anonymous and Named Holes


During development, Flix encourages the use of holes for incomplete code.
For example:


```flix
def sum(x: Int32, y: Int32): Int32 = ???
```


The triple question marks `???` represents an anonymous hole and can be used wherever
an expression is expected. In the above code, `???` represents a missing function
body, but it can also be used inside an expression. For example:


```flix
def length(l: List[a]): Int32 = match l {
case Nil     => 0
case x :: xs => ???
}
```


When a program has multiple holes, it can be useful to name them. For example:


```flix
def length(l: List[a]): Int32 = match l {
case Nil     => ?base
case x :: xs => ?step
}
```


Flix requires that each named hole has a unique name.




## bug! and unreachable!


Flix supports two special "functions": `bug!` and `unreachable!` that can
be used to indicate when an internal program invariant is broken and execute should abort.



For example:


```flix
match o {
case Some(x) => ...
case None    => bug!("The value of \`o\` cannot be empty.")
}
```


As another example:


```flix
match k {
case n if n == 0 => ...
case n if n >= 0 => ...
case n if n <= 0 => ...
case n           =>  unreachable!()
}
```


Use of `bug!` and `unreachable!` should be avoided whenever possible.




## Type Ascriptions


While Flix supports local type inference, it can sometimes be useful to annotate an
expression or a let-binding with its type. We call such annotations for *type
ascriptions*. A type ascription cannot change the type of an expression nor can it be
used to violate type safety.



A type ascription can be placed after an expression:


```flix
("Hello" :: "World" :: Nil) : List[String]
```


and it can also be placed on a let-binding:


```flix
let l: List[String] = "Hello" :: "World" :: Nil
```



### Type Casts


A cast subverts the type system by changing the type of an expression. Casts are by their
nature dangerous and should be used with caution.



The following cast changes the type of an expression and triggers
a `ClassCastException` at run-time:


```flix
(123, 456) as String
```


A cast can also change the effect of an expression. Such casts are safer, but should
still be used with caution.



For example, we can cast an impure expression to a pure expression:


```flix
println("Hello World") as Unit & Pure
```


As a short-hand, we can simply write:


```flix
println("Hello World") as & Pure
```


Casting an impure expression to a pure expression is safe if the expression respects
equational reasoning.
