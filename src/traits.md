# Traits

Traits are one of the ways to support a high
level of genericity in functional programming.
Flix's traits largely follow the style of type
classes in Haskell, with some additional principles.

## Essentials

The function `isSingleton` naively determines whether
a list has exactly one element.
However, it only works with lists.
Although checking the length of a collection like
this is possible for all standard collections, we
have to implement a separate `isSingleton` function
for each of them.

```flix
def isSingleton(l: List[a]): Bool =
    List.length(l) == 1
```

We can generalize this behavior by using a trait
constraint.
Rather than requiring the argument to be a list, we
use a type variable `a` and constrain it with to the
trait `Length`, which means that the function
`Length.length` can be applied to the argument.

```flix
def isSingleton(l: a): Bool with Length[a] =
    Length.length(l) == 1
```

The trait declaration `Length` specifies what
can be done with its members.
In this case, there is only one function:
`Length.length`, which takes the member type as an
argument and returns an integer.
The law `nonnegative` is also defined as part of the
trait.
Laws will be further explored below.

```flix
pub trait Length[a] {
    pub def length(x: a): Int32

    law nonnegative: forall(x: a) . Length.length(x) >= 0
}
```

If we try to use the new `isSingleton` function, we
will see that it fails to compile:

```flix
isSingleton(1 :: 2 :: Nil)
```

While we know that a list has a length, we haven't
told this to the compiler.
To do this, we introduce an `instance` of the trait
for the generic type `List[a]`.

```flix
instance Length[List[a]] {
    pub def length(x: List[a]): Int32 = List.length(x)
}
```

This instance simply states that in order to get the
length of the list, we just use the `List.length`
function from the standard library.
With this instance around, the call to the
`isSingleton` function will compile.
However, you may have noticed that our implementation
is inefficient.
While comparing the length to 1 is a correct solution
generally, for lists specifically the solution has a
greater runtime complexity than necessary.
In order to preserve the general solution while
allowing for optimizations where needed, we can use a
default implementation in the trait and an
override implementation in the instance.

```flix
pub trait Length[a] {

    pub def length(x: a): Int32

    pub def isSingleton(x: a): Bool = length(x) == 1

    law nonnegative: forall(x: a) . Length.length(x) >= 0

    law singletonMeansOne: forall(x: a) . Length.length(x) == 1 <==> Length.isSingleton(x)
}

instance Length[List[a]] {
    pub def length(x: List[a]): Int32 = List.length(x)
    override pub def isSingleton(x: List[a]): Bool = match x {
        case _ :: Nil => true
        case _ => false
    }
}
```

We have added the `isSingleton` function to the
`Length` trait, with a default implementation
that works in general.
(We also added a new law `singletonMeansOne`; see
section **Laws**.)
We have added an efficient `override` implementation
of `isSingleton` to the `Length` instance for
`List[a]`.
The advantage of the default implementation is that
if there's no special behavior needed for a type, the
default is assumed.
The function does not have to be implemented.

```flix
instance Length[String] {
    pub def length(x: String): Int32 = String.length(x)
}
```

The instance `Length[String]` simply uses the default
implementation of the `isSingleton` function.

## Laws

In addition to the functions forming part of their
contract, traits have laws that govern how the
functions may be implemented.

```flix
pub trait Length[a] {
    pub def length(x: a): Int32

    law nonnegative: forall(x: a) . Length.length(x) >= 0
}
```

The `nonnegative` law asserts that the length of
something can never be negative.

#### Planned Feature

We plan to implement a quickcheck framework to verify
that these laws hold.
For now, however, they only serve as a form of
documentation.

## Type Constraints

We've seen type constraints on on function
definitions, but constraints can appear on on
instances and traits themselves as well.

```flix
pub trait TreeSize[a] {
    /// Returns the number of nodes in the object graph of this object
    pub def size(x: a): Int32

    law positive: forall(x: a) . size(x) > 0
}

instance TreeSize[Int32] {
    pub def size(x: Int32): Int32 = 1
}

instance TreeSize[List[a]] with TreeSize[a] {
    pub def size(x: List[a]): Int32 = {
        // one node for each cons cell, one for the nil, and nodes for each node's value
        List.Length(x) + 1 + List.foldLeft((acc, y) -> acc + TreeSize.size(y), 0, x)
    }
}
```

## Sealed Traits

In general, a user can add an instance of a trait for
any type they define.
In some cases, however, it is useful to restrict
membership in a trait to a finite list of types,
defined by the author of the trait.
This is the purpose of a `sealed` trait, for which
instances outside the trait's namespace are not
permitted.

```flix
sealed trait Primitive[a]

instance Primitive[Bool]
instance Primitive[Int32]
instance Primitive[Float64]
// ... and so on
```
