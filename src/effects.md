# Effect System

The Flix type and effect system separates pure and
impure expressions.
A pure expression is guaranteed to be referentially
transparent.
A pure function always returns the same value when
given the same argument(s) and cannot have any
(observable) side-effects.

For example, the following expression is of type
`Int32` and is `Pure`:

```flix
1 + 2 : Int32 & Pure
```

whereas the following expression is `Impure`:

```flix
println("Hello World") : Unit & Impure
```

A higher-order function can specify that a function
argument must be pure, impure, or that it is effect
polymorphic.

For example, the definition of `Set.exists` requires
that its function argument `f` is pure:

```flix
// The syntax a -> Bool is short-hand for a -> Bool & Pure
def exists(f: a -> Bool, s: Set[a]): Bool = ???
```

The requirement that `f` must be pure ensures that
implementation details do not leak.
For example, since `f` is pure it cannot be used to
determine in what order the elements of the set are
traversed.
If `f` was impure such details could leak, e.g. by
passing a function that also prints the current
element, revealing the internal element order inside
the set.

The type and effect system is sound, but not
complete.
That is, if a function is pure then it cannot cause
an effect, whereas if a function is impure then it
may, but does not necessarily, cause an effect.
For example, the following expression is impure even
though it cannot produce an effect at run-time:

```flix
if (1 == 2) println("Hello World!") else ()
```

A higher-order function can also be effect
polymorphic: its effect(s) can depend on its
argument(s).

For example, the standard library definition of
`List.map` is effect polymorphic:

```flix
def map(f: a -> b & ef, xs: List[a]): List[b] & ef
```

The `List.map` function takes a function `f` from
elements of type `a` to `b` with effect `ef`.
The effect of the function itself is `ef`.
Consequently, if `List.map` is invoked with a pure
function then the entire expression is pure whereas
if it is invoked with an impure function then the
entire expression is impure.

A higher-order function that takes multiple function
arguments may combine their effects.

For example, the standard library definition of
forward function composition `>>` is pure if both its
function arguments are pure:

```flix
def >>(f: a -> b & ef1, g: b -> c & ef2): a -> c & (ef1 and ef2) = x -> g(f(x))
```

The type and effect signature can be understood as
follows: The `>>` function takes two function
arguments: `f` with effect `ef1` and `g` with
effect `ef2`.
The effect of `>>` is effect polymorphic in the
conjunction of `ef1` and `ef2`.
If both are pure (their effect is `true`) then the
overall expression is pure (`true`).
Otherwise it is impure.

The type and effect system allows arbitrary boolean
expressions to control the purity of function
arguments.

For example, it is possible to express a higher-order
function `h` that accepts two function arguments `f`
and `g` of which at most one is impure:

```flix
def h(f: a -> b & ef1, g: b -> c & (not ef1 or ef2)): Unit
```

Note that here `ef1` and `ef2` are arbitrary boolean
variables which are not directly associated with the
effect of `f` or `g` (like it was the case in the
simpler example above).
In general, the possible effects for argument
functions and the to-be-defined function are described
by arbitrary boolean expressions.
Here the possible effects of `g` (whether it can be
pure or impure) are specified by the boolean
`not ef1 or ef2`.
For a specific combination of pure and impure to be
accepted, there must be an assignment of the boolean
variables `ef1` and `ef2` to true and false such that
the boolean expressions for *pure* arguments evaluate
to `true` and those for *impure* arguments evaluate to
`false`.

If in this example `h` is called with a function
argument `f` which is impure, then the variable `ef1`
must be false and thus the second argument must be
pure (because `not ef1 or ef2` will always be true,
no matter how we choose `ef2`).
Conversely, if `f` is pure, then `ef1` must be true
and `g` may be pure (`ef2 = true`) or impure
(`ef2 = false`).
It is a compile-time error to call `h` with two impure
functions.

The type and effect system can be used to ensure that
statement expressions are useful, i.e. that if an
expression or function is evaluated and its result is
discarded then it must have a side-effect.
For example, compiling the program fragment below:

```flix
List.map(x -> x + 1, 1 :: 2 :: Nil);
123
```

causes a compiler error:

```flix
-- Redundancy Error -------------------------------------------------- ???

>> Useless expression: It has no side-effect(s) and its result is discarded.

2 |     List.map(x -> x + 1, 1 :: 2 :: Nil);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
useless expression.


Possible fixes:

(1)  Use the result computed by the expression.
(2)  Remove the expression statement.
(3)  Introduce a let-binding with a wildcard name.
```

because it is non-sensical to evaluate the pure
expression
`List.map(x -> 2 * x, 1 :: 2 :: Nil)` and then to
discard its result.
Most likely the programmer wanted to use the result
(or alternatively the expression is redundant and
could be deleted).
Consequently, Flix rejects such programs.

In summary, Flix function types are of the form:



| Function Type                                                                                                                        | Syntax                   | Short Hand |
|:------------------------------------------------------------------------------------------------------------------------------------:|:------------------------:|:----------:|
| The type of a *pure* function from `a` to `b`.                                                                                       | `a -> b & Pure`          | `a -> b`   |
| The type of an *effect polymorphic* function from `a` to `b` with effect `ef`.                                                       | `a -> b & ef`            | n/a        |
| The type of an *effect polymorphic* function from `a` to `b` with effect `ef1 and ef2` (i.e. pure if both `ef1` and `ef2` are true.) | `a -> b & (ef1 and ef2)` | n/a        |

