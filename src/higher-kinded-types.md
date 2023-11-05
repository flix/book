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

Flix requires explicit kind annotations in two situations:

- For non-Type kinds on enum type parameters.
- For non-Type kinds on traits.

In other words, if you are only using types of kind `Type`, no annotations are
necessary. But if you want an enum declaration or trait to abstract over a
non-Type kind then you must explicitly write its kind. 
