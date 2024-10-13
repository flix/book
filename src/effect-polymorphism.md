## Effect Polymorphism

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

### Effect Exclusion

A novel feature of Flix is its support for [polymorphic effect
exclusion](https://dl.acm.org/doi/abs/10.1145/3607846). In simple terms, effect
exclusion allows us to write a higher-order function that disallows a specific
set of effects while allowing all other effects. 

For example, we can write a listener registration function: 

```flix
def onClick(listener: KeyEvent -> Unit \ {ef - Block}, ...): ... 
```

Here `onClick` takes a function listener that can have _any_ effect, _except_
the `Block` effect. Hence a key listener can perform any action, except for an
action that would block the UI thread.



### Sub-Effecting
