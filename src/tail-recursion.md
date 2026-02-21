# Tail Recursion

In Flix, and in functional programming in general, iteration is expressed
through [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)).

For example, if we want to determine if a list contains an element, we can write
a recursive function:

```flix
def memberOf(x: a, l: List[a]): Bool with Eq[a] = 
    match l {
        case Nil     => false
        case y :: ys => if (x == y) true else memberOf(x, ys)
    }
```

The `memberOf` function pattern matches on the list `l`. If it is empty then it
returns `false`. Otherwise, we have an element `y` and the rest of the list is
`ys`. If `x == y` then we have found the element and we return `true`. Otherwise
we _recurse_ on the rest of the list `ys`. 

The recursive call to `memberOf` is in _tail position_, i.e. it is the last
thing to happen in the `memberOf` function. This has two important benefits: (a)
the Flix compiler is able to rewrite `memberOf` to use an ordinary loop (which
is more efficient than a function call) and more importantly (b) a call to
`memberOf` _cannot_ overflow the stack, because the call stack never increases
in height.

> **Tip**: Flix has support for [full tail
call](https://en.wikipedia.org/wiki/Tail_call) elimination which means that
recursive calls in tail position never increase the stack height and hence
cannot cause the stack to overflow!

We _remark_ that Flix has ___full___ tail call elimination, not just tail call
optimization. This means that the following program compiles and runs
successfully: 

```flix
def isOdd(n: Int32): Bool =
    if (n == 0) false else isEvn(n - 1)

def isEvn(n: Int32): Bool =
    if (n == 0) true else isOdd(n - 1)

def main(): Unit \ IO =
    isOdd(12345) |> println
```

which is not the case in many other programming languages.


## Non-Tail Calls and StackOverflows

While the Flix compiler _guarantees_ that tail calls cannot overflow the stack,
the same is not true for function calls in non-tail positions.

For example, the following implementation of the [factorial
function](https://en.wikipedia.org/wiki/Factorial) overflows the call stack: 

```flix
def factorial(n: Int32): Int32 = match n {
    case 0 => 1
    case _ => n * factorial(n - 1)
}
```

as this program shows:

```flix
def main(): Unit \ IO = 
    println(factorial(1_000_000))
```

which when compiled and run produces:

```
java : Exception in thread "main" java.lang.StackOverflowError
	at Cont%Int32.unwind(Cont%Int32)
	at Def%factorial.invoke(Unknown Source)
	at Cont%Int32.unwind(Cont%Int32)
	at Def%factorial.invoke(Unknown Source)
	at Cont%Int32.unwind(Cont%Int32)
    ... many more frames ...
```

A well-known technique is to rewrite `factorial` to use an accumulator:

```flix
def factorial(n: Int32): Int32 = 
    def visit(x, acc) = match x {
        case 0 => acc
        case _ => visit(x - 1, x * acc)
    };
    visit(n, 1)
```

Here the `visit` function is tail recursive, hence it cannot overflow the stack.

## The @TailRec Annotation

Flix provides the `@TailRec` annotation, which asks the compiler to verify that
every self-recursive call in a function is in tail position. The annotation is
optional and does not change runtime behavior — it serves as a documentation and
verification tool.

For example, an accumulator-style `sum` function is tail recursive:

```flix
@TailRec
def sum(l: List[Int32], acc: Int32): Int32 = match l {
    case Nil     => acc
    case x :: xs => sum(xs, acc + x)
}
```

The compiler accepts this because the recursive call to `sum` is the last
operation in the function — nothing further is done with its result.

In contrast, the following function is rejected:

```flix
@TailRec
def length(l: List[Int32]): Int32 = match l {
    case Nil     => 0
    case _ :: xs => length(xs) + 1
}
```

Here, the result of `length(xs)` is used in an addition (`+ 1`), so the
recursive call is _not_ in tail position. The compiler reports an error:

```
>> Non-tail recursive call in @TailRec function 'length'.

   ... length(xs) + 1
       ^^^^^^^^^^
       non-tail recursive call
```

To fix this, rewrite the function to use an accumulator, as shown above.

> **Tip:** The `@TailRec` annotation is purely a compile-time check. It does
> not affect code generation — Flix already performs full tail call elimination
> for any call in tail position, whether annotated or not. Use `@TailRec` when
> you want the compiler to guarantee that a function _remains_ tail recursive as
> the code evolves.
