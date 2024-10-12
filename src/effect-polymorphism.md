## Effect Polymorphism

<div style="color:gray">


### Pure, Impure, and Effect Polymorphic Functions

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

Note the annotation for `Pure` is `\ {}`.

A function that prints to the console is `Impure`
and must be marked with `\ IO`:

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

> **Design Note**
>
> The Flix standard library enforces several program
> invariants using purity.
> For example, in Flix, the `Eq` and `Order` traits
> require that their operations are pure.
> This ensures that collections, such as lists, sets,
> and maps, do not leak internal implementation
> details.


A higher-order function can specify that a function
argument must be pure, impure, or that it is effect
polymorphic.

For example, the definition of `Set.exists` requires
that its function argument `f` is pure:

```flix
// The syntax a -> Bool is short-hand for a -> Bool \ {}
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
def map(f: a -> b \ ef, xs: List[a]): List[b] \ ef
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
def >>(f: a -> b \ ef1, g: b -> c \ ef2): a -> c \ { ef1, ef2 } = x -> g(f(x))
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
def h(f: a -> b \ ef1, g: b -> c \ { (not ef1) or ef2 }): Unit
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
the boolean expressions for _pure_ arguments evaluate
to `true` and those for _impure_ arguments evaluate to
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

```
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

|                                                            Function Type                                                             |         Syntax          | Short Hand |
| :----------------------------------------------------------------------------------------------------------------------------------: | :---------------------: | :--------: |
|                                            The type of a _pure_ function from `a` to `b`.                                            |      `a -> b \ {}`      |  `a -> b`  |
|                            The type of an _effect polymorphic_ function from `a` to `b` with effect `ef`.                            |      `a -> b \ ef`      |    n/a     |
| The type of an _effect polymorphic_ function from `a` to `b` with effect `ef1 and ef2` (i.e. pure if both `ef1` and `ef2` are true.) | `a -> b \ { ef1, ef2 }` |    n/a     |

TODO: Subeffecting

### Effect Exclusion

### Sub-Effecting

</div>