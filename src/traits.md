# Traits

Traits (also known as _type classes_) support abstraction and overloading. At a
first-glance, the trait system in Flix is similar to that of Haskell and Rust,
with some more important differences. Flix traits support associated types,
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
equality? Enter traits. 

We can define an `Equatable` trait:

```flix
trait Equatable[t] {
    pub def equals(x: t, y: t): Bool
}
```

which has a single `equals` _signature_. The trait is polymorphic over the type
parameter `t` which means that we can implement `Equatable` for both `Option[t]`
and `List[t]`: 

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
compute whether two `Option[Int32]` are equal. But we can compute if two
`Option[List[Option[Int32]]]` types are equal! This demonstrates the power of
abstraction: We have implemented instances for `Option[t]` and `List[t]` and we
can now reuse these everywhere. 

We can use our newly defined `Equatable` trait to write polymorphic functions.

For example, we can define a function to compute if an element occurs in a list:

```flix
def memberOf(x: t, l: List[t]): Bool with Equatable[t] = 
    match l {
        case Nil     => false
        case y :: ys => Equatable.equals(x, y) or memberOf(x, ys)
    }
```

What is important is that we can use `memberOf` with a list of any type! We can
use it for `List[Int32]`, `List[String]`, and so forth, provided that the
element type implements `Equatable`.

> **Note:** In the Flix Standard Library the `Equatable` trait is called `Eq`.
