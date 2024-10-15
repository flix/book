## Effect Polymorphism

<div style="color:gray">

> **Note:** The following text applies to Flix 0.54.0 or later.

In Flix, we can express that a function is pure (i.e. has no side-effects): 

```flix
def inc(x: Int32): Int32 \ { } = x + 1
                        // ^^^ empty effect set
```

Here the `inc` function is _pure_ because its effect set is empty. In Flix, a
pure functions is referentially transparent. In other words, given the same
arguments is always returns the same value. When a function is pure, we do not
have to explicitly write the empty effect set `{ }`, instead we can write: 

```flix
def inc(x: Int32): Int32 = x + 1
```

In Flix, we can also express that a function has an effect:

```flix
def incAndPrint(x: Int32): Int32 \ {IO} = 
    let result = x + 1;         // ^^^^ singleton effect set
    println(result);
    result
```

Here the `incAndPrint` function has the _foundational_ `IO` effect. 

In Flix, we can also express that a function has multiple effects:

```flix
def copyFile(src: String, dst: String): Unit \ {FileRead, FileWrite} = ...
                                            // ^^^^^^^^^^^^^^^^^^^^^ multiple effects
```

Here the `copyFile` function has two foundational effects: `FileRead` and
`FileWrite`. 

In Flix, we can have a function that has a heap effect:

```flix
def nth(i: Int32, a: Array[t, r]): Option[a] \ {r} = ....
                                            // ^^^ heap effect
```

Here the `nth` function has a _heap effect_ in the region `r`.

In Flix, we can also write functions that mix different effects:

```flix
def strange(a: Array[t, r]): Unit \ {r, FileRead, Net, Clock} 
                                 // ^^^^^^^^^^^^^^^^^^^^^^^^^ a mixture of effects
```

This function has a heap effect `r`, two foundational effects: `FileRead` and
`Net`, and an algebraic effect `Clock`. 

### Higher-Order Functions

When we write higher-order functions, we must think about their effect behavior. 

For example, we can write a higher-order function `List.exists`:

```flix
def exists(f: a -> Bool \ { }, s: Set[a]): Bool = ...
                          ^^^
```

which enforces that the predicate function `f` is pure. Why would we do this?
For at least two reasons: (a) it allows us to hide the iteration inside the set
and (b) it allows us to safely perform the counting in parallel. 

Nevertheless, requring function arguments to be pure is goes against the spirit
of Flix, and should only be used sparingly. 

More common, and more appropriate, is to write _effect polymorphic_ functions.
That is higher-order functions whose effect(s) depend on the effect(s) of their
function arguments. 

For example, we can write an effect polymorphic map function:

```flix
def map(f: a -> b \ ef, l: List[a]): List[b] \ ef = ...
                    ^^ // effect variable      ^^ effect variable
```

The type and effect signature of `map` essentialy says: If `map` is given a
function `f` with effect(s) `ef` then calling `map` has the effect(s) `ef`. That
is, if `f` is pure (i.e. has no effects) then the call to `map` will be pure. If
`f` has the `IO` effect then the call to `map` will have the `IO` effect: 


```flix
List.map(x -> x + 1, l)               // is pure
List.map(x -> {println(x); x + 1}, l) // has IO effect
```

A higher-order function that takes multiple function arguments may combine their
effects.

For example, the standard library definition of
forward function composition `>>` is pure if both its
function arguments are pure:

```flix
def >>(f: a -> b \ ef1, g: b -> c \ ef2): a -> c \ (ef1 + ef2) = x -> g(f(x))
```

Here we should read `ef1 + ef2` has the union of the two effects of `f` and `g`.

<div style="color: black">

### Effect Exclusion

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

### Sub-Effecting

> **Note:** This feature is not yet enabled by default.

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
def handle(x -> do Throw.throw(x)) // OK, has the `Throw` effect.
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
