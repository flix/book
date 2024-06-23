## Type-Level Programming

> **Note:** This feature is experimental. Do not use in production.

This section assumes prior familiarity with type-level programming and phantom
types.

### Type-Level Booleans

A unique Flix feature is its support for _type-level Boolean formulas_. This
means `true` and `false` are types, but also that formulas such as `x and (not
y)` are types. A type-level Boolean formulas has kind `Bool`. Two type-level
Boolean formulas are equal if the formulas are equivalent (i.e. have the same
truth tables). For example, the two types `true` and `x or not x` are _the same
type_.

While type-level Boolean formulas are not as expressive as general refinement
types or dependent types they support complete type inference and parametric
polymorphism. This means that they are very ergonomic to work with.

We can use type-level Boolean formulas to statically enforce program invariants.

We illustrate with a few examples:

#### Humans and Vampires

```flix
///
/// We can use a phantom type-level Boolean to model whether a person is alive
/// or is undead (i.e. a vampire).
///
enum Person[_isAlive: Bool] {
    /// A person has a name, an age, and is modelled as a record.
    case P({name = String, age = Int32})
}

///
/// We interpret the Boolean `true` is alive and the Boolean `false` as undead
/// (i.e. a vampire).
///
type alias Alive  = true
type alias Undead = false

///
/// A person who is born is alive.
///
def born(name: String): Person[Alive] =
    Person.P({name = name, age = 0})

///
/// A person who is alive and is bitten becomes a vampire.
///
/// Note that the type system enforces that an already undead (i.e. a vampire)
/// cannot be bitten again.
///
def bite(p: Person[Alive]): Person[Undead] = match p {
    /// The implementation is not important; it simply restructs the person.
    case Person.P(r) => Person.P(r)
}

///
/// Two persons can be married, but only if they are both alive or both undead.
///
/// (The church does not yet recognize human-vampire marriages.)
///
/// Note that the type system enforces that both arguments have the same type.
///
def marry(_p1: Person[isAlive], _p2: Person[isAlive]): Unit = ()

///
/// We can implement a more sophisticated version of born.
///
/// If two persons have a child then that child is a vampire if one of them is.
///
/// Note that here we use the type-level computation `isAlive1 and isAlive2`
/// to compute whether the result is alive or undead.
///
def offspring(p1: Person[isAlive1], p2: Person[isAlive2]): Person[isAlive1 and isAlive2] =
    match (p1, p2) {
        case (Person.P(r1), Person.P(r2)) =>
            Person.P({name = "Spawn of ${r1#name} and ${r2#name}", age = 0})
}

///
/// A person can age-- no matter if they are alive or undead.
///
/// Note that this function preserves the `isAlive` parameter. That is, if a
/// person is alive they stay alive.
///
def birthday(p: Person[isAlive]): Person[isAlive] = match p {
    case Person.P(r) => Person.P({name = r#name, age = r#age + 1})
}
```

We can now illustrate how the type system enforces certain invariants.

For example, the type system ensures that person cannot be bitten twice:

```flix
let p = birthday(bite(born("Dracula")));
bite(p);
```

If we compile this program then the Flix compiler emits a compiler error:

```
❌ -- Type Error --------------------------------------------------

>> Expected argument of type 'Person[true]', but got 'Person[false]'.

69 |     bite(p);
              ^
              expected: 'Person[true]'

The function 'bite' expects its 1st argument to be of type 'Person[true]'.
```

Here we have to recall that `true` means `Alive` and `false` means `Undead`.
