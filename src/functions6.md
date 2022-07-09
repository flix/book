# Pure, Impure, and Effect Polymorphic Functions

In Flix every function is pure, impure, or effect
polymorphic.

The Flix type and effect system ensures that a pure
function always returns the same result when given
the same arguments and that it cannot have
(observable) side effects.

In Flix every function definition is *implicitly*
marked as `Pure`.
For example, the function definition:

```flix
def add(x: Int32, y: Int32): Int32 = x + y
```

is actually equivalent to:

```flix
def add(x: Int32, y: Int32): Int32 & Pure = x + y
```

A function that prints to the console is `Impure`
and must be marked as such:

```flix
def addAndPrint(x: Int32, y: Int32): Int32 & Impure =
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
*effect polymorphism*.
For example:

```flix
def map(f: a -> b & ef, l: List[a]): List[b] & ef = ???
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
