# Termination Checking

Flix supports the `@Terminates` annotation, which asks the compiler to verify
that a function is _structurally recursive_ — meaning it is guaranteed to
terminate on all inputs. A function annotated with `@Terminates` must make
recursive calls only on strict substructures of its formal parameters. The
compiler checks this at compile time and reports an error if the function does
not satisfy the structural recursion requirement.

## Structural Recursion

The core idea behind `@Terminates` is _structural recursion_: every recursive
call must pass an argument that was obtained by pattern matching on a formal
parameter and extracting a component from inside a constructor. This component is
strictly smaller than the original, so the recursion must eventually reach a base
case.

For example, here is a structurally recursive `length` function on a custom list
type:

```flix
enum MyList[a] {
    case Nil
    case Cons(a, MyList[a])
}

@Terminates
def length(l: MyList[Int32]): Int32 = match l {
    case MyList.Nil         => 0
    case MyList.Cons(_, xs) => 1 + length(xs)
}
```

The recursive call passes `xs`, which is bound inside the `Cons` constructor of
`l`. Since `xs` is strictly smaller than `l`, the compiler accepts this function.

## Tree Recursion

Structural recursion works on any algebraic data type, not just lists. A function
may make multiple recursive calls in the same branch, as long as each call
receives a strict substructure of a formal parameter.

For example, here is a `size` function on a binary tree:

```flix
enum MyTree[a] {
    case Leaf(a)
    case Node(MyTree[a], MyTree[a])
}

@Terminates
def size(t: MyTree[Int32]): Int32 = match t {
    case MyTree.Leaf(_)    => 1
    case MyTree.Node(l, r) => size(l) + size(r)
}
```

Both `l` and `r` are bound inside the `Node` constructor of `t`, so both
recursive calls are valid.

## Multiple Parameters

When a function has multiple parameters, only _one_ parameter needs to decrease
per recursive call. The other parameters may be passed unchanged.

For example, `append` recurses on `l1` while passing `l2` unchanged:

```flix
enum MyList[a] {
    case Nil
    case Cons(a, MyList[a])
}

@Terminates
def append(l1: MyList[Int32], l2: MyList[Int32]): MyList[Int32] = match l1 {
    case MyList.Nil         => l2
    case MyList.Cons(x, xs) => MyList.Cons(x, append(xs, l2))
}
```

The compiler sees that `xs` is a strict substructure of `l1`, which is
sufficient. The fact that `l2` does not decrease is fine.

> **Warning:** `@Terminates` guarantees that a function terminates, but it does
> _not_ guarantee that it is tail recursive. For example, the `append` function
> above is structurally recursive but _not_ tail recursive — the recursive call
> is wrapped in `MyList.Cons(x, ...)`. This means it can overflow the stack on
> very long lists. See the [Tail Recursion](./tail-recursion.md) section for how
> to write stack-safe recursive functions.

## Local Definitions

Local definitions inside a `@Terminates` function are checked independently.
A local function may recurse on its own parameters:

```flix
enum MyList[a] {
    case Nil
    case Cons(a, MyList[a])
}

@Terminates
def length(l: MyList[Int32]): Int32 =
    def loop(ll: MyList[Int32], acc: Int32): Int32 = match ll {
        case MyList.Nil         => acc
        case MyList.Cons(_, xs) => loop(xs, acc + 1)
    };
    loop(l, 0)
```

Here `loop` recurses on its own parameter `ll`, passing `xs` which is a strict
substructure. The outer function `length` is non-recursive, so it is
trivially terminating.

## Higher-Order Functions

A `@Terminates` function may apply closures that come from its formal parameters.
This allows higher-order patterns like `map`:

```flix
enum MyList[a] {
    case Nil
    case Cons(a, MyList[a])
}

@Terminates
def map(f: Int32 -> Int32, l: MyList[Int32]): MyList[Int32] = match l {
    case MyList.Nil         => MyList.Nil
    case MyList.Cons(x, xs) => MyList.Cons(f(x), map(f, xs))
}
```

The application `f(x)` is allowed because `f` is a formal parameter of
`map`. The compiler tracks that `f` originates from a parameter and permits
the call.

However, applying a _locally-constructed_ closure is forbidden:

```flix
@Terminates
def bad(x: Int32): Int32 =
    let c = y -> y + 1;
    c(x)
```

This is rejected because `c` is not a formal parameter — it is a locally
defined closure that could, in general, hide arbitrary computation.

> **Warning:** `@Terminates` guarantees that `map` terminates _assuming_ its
> function argument `f` also terminates. If `f` is a non-terminating function,
> then `map` may not terminate either. The annotation only verifies the
> structural recursion of `map` itself — it does not check the behavior of `f`.

## Calling Other Functions

A `@Terminates` function may only call other functions that are also annotated
with `@Terminates`. Calling a function without the annotation is an error.

For example, the following is rejected:

```flix
def g(x: Int32): Int32 = x * 2

@Terminates
def f(x: Int32): Int32 = g(x)
```

The compiler reports:

```
>> Call to non-@Terminates function 'g' in @Terminates function 'f'.

   ... g(x)
       ^^^^^^^^^
       non-terminating call
```

The fix is to annotate the callee:

```flix
@Terminates
def g(x: Int32): Int32 = x * 2

@Terminates
def f(x: Int32): Int32 = g(x)
```

## Strict Positivity

Enum types used for structural recursion must be _strictly positive_. A type is
strictly positive if it does not contain a recursive occurrence to the left of
an arrow in any constructor.

For example, the following enum is **not** strictly positive because `Bad`
appears to the left of `->` in the argument to `MkBad`:

```flix
enum Bad {
    case MkBad(Bad -> Int32)
}

@Terminates
def f(x: Bad): Int32 = match x {
    case Bad.MkBad(_) => 0
}
```

The compiler rejects this with:

```
>> Non-strictly positive type in 'f'.

   ... case MkBad(Bad -> Int32)
                  ^^^^^^^^^^^^
                  negative occurrence
```

A _double negation_ is fine, because two negatives make a positive:

```flix
enum Good {
    case MkGood((Good -> Int32) -> Int32)
}

@Terminates
def useGood(x: Good): Int32 = match x {
    case Good.MkGood(_) => 0
}
```

Here, `Good` appears to the left of an arrow that is itself to the left of
another arrow, placing it in a positive position overall. The compiler accepts
this.

## Common Errors

The most common mistake is passing the original parameter instead of a
substructure obtained from pattern matching:

```flix
enum MyList[a] {
    case Nil
    case Cons(a, MyList[a])
}

@Terminates
def f(x: MyList[Int32]): Int32 = match x {
    case MyList.Nil         => 0
    case MyList.Cons(_, xs) => f(x)
}
```

Notice that the recursive call passes `x` (the original parameter) instead of
`xs` (the tail extracted from the pattern). The compiler reports:

```
>> Non-structural recursion in 'f'.

   ... f(x)
       ^^^^
       non-structural recursive call

   Parameter   Argument   Status
   x           x          alias of 'x' (not destructured)
```

The diagnostic table shows which arguments are problematic. The fix is to pass
`xs` instead of `x`:

```flix
case MyList.Cons(_, xs) => f(xs)
```

