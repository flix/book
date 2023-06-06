## Type-Level Programming

> **Note:** This feature is experimental. Do not use in production.

### Type-Level Booleans

Flix supports Booleans and Boolean formulas at the type-level.

We can use such formulas to capture and statically enforce invariants of a
program. For example:

> **Note:** The following example may confuse vampire and zombie mythology. 

```flix
///
/// We can use a phantom type-level Booleans to capture
/// whether a person is alive or undead (i.e. a vampire).
///
enum Person[_isAlive: Bool] {
    case Person({name = String, age = Int32})
}

/// 
/// We interpret `true` as Alive and `false` as Undead.
///
type alias Alive  = true
type alias Undead = false

///
/// A person who is born is alive. 
/// See later for a natural birth with parents.
///
def born(name: String): Person[Alive] =
    Person.Person({name = name, age = 0})

///
/// A person who is alive and is bitten becomes a vampire.
///
def bitten(p: Person[Alive]): Person[Undead] = match p {
    case Person.Person(r) => Person.Person(r)
}

///
/// Two persons can be married, but only if they are both alive.
///
/// (The church does not recognize vampire marriages yet.)
///
def marry(_p1: Person[Alive], _p2: Person[Alive]): Unit = ()

///
/// In our lore, a person who is undead can be resurrected.
///
def resurrect(p: Person[Undead]): Person[Alive] = match p {
    case Person.Person(r) => Person.Person(r)
}

///
/// If two persons have a child then that child is a vampire 
/// if one of them is. At least that is how it works in Dawn
/// of the Dead. Hm, but those are Zombies, I digress.
///
/// Note the type-level computation of `isAlive1 and isAlive2`.
///
def offspring(p1: Person[isAlive1], p2: Person[isAlive2]): Person[isAlive1 and isAlive2] = match (p1, p2) {
    case (Person.Person(r1), Person.Person(r2)) => 
        Person.Person({name = "Son/Daughter of ${r1.name} and ${r2.name}", age = 0})
}

///
/// A person can age-- no matter if they are alive or not.
///
/// Note that this function preserves the `isAlive` parameter.
///
def birthday(p: Person[isAlive]): Person[isAlive] = match p {
    case Person.Person(r) => Person.Person({name = r.name, age = r.age + 1})
}
```

The Flix type system prevents us from misusing `Person`.

For example, if we try:

```flix
let p = birthday(bitten(born("Dracula")));
bitten(p);
```

then the Flix compiler emits a compiler error:

```
❌ -- Type Error -------------------------------------------------- 

>> Expected argument of type 'Person[Alive]', but got 'Person[false]'.

69 |     bitten(p);
                ^
                expected: 'Person[Alive]'

The function 'bitten' expects its 1st argument to be of type 'Person[Alive]'.
```

Here we have to recall that false means `Undead`.
