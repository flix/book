## Higher-Kinded Types

Flix supports [higher-kinded
types](https://en.wikipedia.org/wiki/Kind_(type_theory)), hence traits can
abstract over _type constructors_. 

For example, we can write a trait that capture iteration over any
collection of the shape `t[a]` where `t` is a type constructor of kind
 `Type -> Type` and `a` is the element type of kind `Type`:

```flix
trait ForEach[t: Type -> Type] {
    pub def forEach(f: a -> Unit \ ef, x: t[a]): Unit \ ef
}
```

Note that to use higher-kinded types Flix _requires_ us to provide the kind
annotation (i.e. we had to write `t: Type -> Type` to inform Flix that `ForEach`
abstracts over type constructors.)

We can implement instances of the `ForEach` trait for type constructors
such as `Option`, and `List`, `Set`. For example:

```flix
instance ForEach[List] {
    pub def forEach(f: a -> Unit \ ef, l: List[a]): Unit \ ef = match l {
        case Nil     => ()
        case x :: xs => f(x); ForEach.forEach(f, xs)
    }
}
```

> **Note**: Flix does not have a `ForEach` trait, but instead has the much
> more powerful and versatile `Foldable` trait. 

### The Flix Kinds

Flix supports the following kinds:

- `Type`: The kind of Flix types.
    - e.g. `Int32`, `String`, and `List[Int32]`.
- `RecordRow`: The kind of rows used in records 
    - e.g. in `{x = Int32, y = Int32 | r}` the type variable `r` has kind `RecordRow`.
- `SchemaRow`: The kind of rows used in first-class Datalog constraints
    - e.g. in `#{P(Int32, Int32) | r}` the type variable `r` has kind `SchemaRow`.

Flix can usually infer kinds. For example, we can write:

```flix
def sum(r: {x = t, y = t | r}): t with Add[t] = r.x + r.y
```

and have the kinds of `t: Type` and `r: RecordRow` automatically inferred.

We can also explicitly specify them as follows:

```flix
def sum[t: Type, r: RecordRow](r: {x = t, y = t | r}): t with Add[t] = r.x + r.y
```

but this style is not considered idiomatic.

Flix requires explicit kind annotations in three situations:

- For non-Type kinds on enum type parameters.
- For non-Type kinds on traits.
- For non-Type type members in traits.

The most common scenario where you will need a kind annotation is when you want
a type parameter or type member to range over an effect. 

### Higher-Kinded Types vs. Associated Types

In practice higher-kinded types and associated types can be used to define
similar abstractions. For example, as we have seen, we can define the `ForEach`
trait in two different ways: 

With a higher-kinded type: 

```flix
trait ForEach[t: Type -> Type] {
    pub def forEach(f: a -> Unit \ ef, x: t[a]): Unit \ ef
}
```

and with an associated type:

```flix
trait ForEach[t] {
    type Elm
    pub def forEach(f: ForEach.Elm[t] -> Unit \ ef, x: t): Unit \ ef
}
```

In the case of `ForEach` the definition with the associated type is more
flexible, since we can define an instance for `String` with associated element
type `Char`. However, higher-kinded types are still useful. For example, the
Flix Standard Library defines the `Functor` trait as: 

```flix
trait Functor[m : Type -> Type] {
    pub def map(f: a -> b \ ef, x: m[a]): m[b] \ ef
}
```

Notably the kind of `m` ensures that evert `Functor` instance is structure
preserving. That is, we know that when we `map` over e.g. an `Option[a]` then we
get back and an `Option[b]`.

