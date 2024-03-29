# Traits

Traits, also known as [type classes](https://en.wikipedia.org/wiki/Type_class),
support abstraction and modularity. The Flix trait system is similar to that of
Haskell and Rust, but not identical. Traits in Flix support associated types,
associated effects, and higher-kinded types. 

We illustrate traits with an example.

We can define equality on `Option[Int32]` as follows:

```flix
def equals(x: Option[Int32], y: Option[Int32]): Bool = 
    match (x, y) {
        case (None, None)         => true
        case (Some(v1), Some(v2)) => v1 == v2
        case _                    => false
    }
```

We can also define equality on `List[Int32]` as follows:

```flix
def equals(x: List[Int32], y: List[Int32]): Bool = 
    match (x, y) {
        case (Nil, Nil)           => true
        case (v1 :: xs, v2 :: ys) => v1 == v2 and equals(xs, ys)
        case _                    => false
    }
```

But what if we wanted a common abstraction for data types which support
equality? 

Here we can use traits. We can define an `Equatable` trait:

```flix
trait Equatable[t] {
    pub def equals(x: t, y: t): Bool
}
```

which has a single `equals` _trait signature_. The trait is polymorphic over the
type parameter `t` which means that we can implement `Equatable` for both
`Option[t]` and `List[t]`: 

```flix
instance Equatable[Option[t]] with Equatable[t] {
    pub def equals(x: Option[t], y: Option[t]): Bool = 
        match (x, y) {
            case (None, None)         => true
            case (Some(v1), Some(v2)) => Equatable.equals(v1, v2)
            case _                    => false
        }
}
```

Notice that we did not implement `Equatable` for `Option[Int32]`, but instead
for _any_ `Option[t]` as long as `t` itself is equatable. Moreover, instead of
comparing `v1` and `v2` directly using `==`, we call `Equatable.equals` on them. 

We can also implement `Equatable` for `List[t]`:

```flix
instance Equatable[List[t]] with Equatable[t] {
    pub def equals(x: List[t], y: List[t]): Bool = 
        use Equatable.equals;
        match (x, y) {
            case (Nil, Nil)           => true
            case (v1 :: xs, v2 :: ys) => equals(v1, v2) and equals(xs, ys)
            case _                    => false
        }
}
```

Assuming we also implement `Equatable` for `Int32`, we can use `Equatable` to
compute whether two `Option[Int32]` values are equal. But we can also compute if
two `Option[List[Int32]]` values are equal! This demonstrates the power of
abstraction: We have implemented instances for `Option[t]` and `List[t]` and we
can now reuse these instances everywhere. 

We can use our newly defined `Equatable` trait to write polymorphic functions.

For example, we can define a function to compute if an element occurs in a list:

```flix
def memberOf(x: t, l: List[t]): Bool with Equatable[t] = 
    match l {
        case Nil     => false
        case y :: ys => Equatable.equals(x, y) or memberOf(x, ys)
    }
```

We can use `memberOf` for a list of any type, as the element type implements
`Equatable`.

> **Note:** In the Flix Standard Library the `Equatable` trait is called `Eq`.
> Moreover, the `==` operator is syntactic sugar for the trait signature
> `Eq.eq`.

## Sealed Traits

We can declare a trait as `sealed` to restrict who can implement the trait.

For example:

```flix
mod Zoo {
    sealed trait Animal[a] {
        pub def isMammal(x: a): Bool
    }

    instance Animal[Giraffe] {
        pub def isMammal(_: Giraffe): Bool = true
    }

    instance Animal[Penguin] {
        pub def isMammal(_: Penguin): Bool = true
    }

    pub enum Giraffe
    pub enum Penguin
}
```

Here we can implement instances for `Animal` and `Giraffe` because they occur in
the same module as the `Animal` trait. But we cannot implement `Animal` from
outside the `Zoo` module. If we try: 

```flix
mod Lake {
    pub enum Swan

    instance Zoo.Animal[Swan] {
        pub def isMammal(_: Swan): Bool = false
    }
}
```

then Flix reports:

```
❌ -- Resolution Error -------------------------------------------------- 

>> Class 'Zoo.Animal' is sealed from the module 'Lake'.

21 |     instance Zoo.Animal[Swan] {
                  ^^^^^^^^^^
                  sealed class.
```


## Well-formed Traits

A trait is _not_ a C\# or Java-style interface. Specifically:

- every trait must have exactly one type parameter, and
- every signature must mention that type parameter.

For example, the following trait is incorrect:

```flix
trait Animal[a] {
    pub def isMammal(x: a): Bool      // OK     -- mentions a.
    pub def numberOfGiraffes(): Int32 // NOT OK -- does not mention a.
}
```

and Flix reports:

```
❌ -- Resolution Error -------------------------------------------------- 

>> Unexpected signature 'numberOfGiraffes' which does not mention the type 
>> variable of the trait.

7 |     pub def numberOfGiraffes(): Int32 
                ^^^^^^^^^^^
                unexpected signature.
```

The problem is that the signature for `numberOfGiraffes` does not mention the
type parameter `a`. 
