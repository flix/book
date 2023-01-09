# Common Problems

- [ToString is not defined on 'a'](#tostring-is-not-defined-on-a)
- [No instance of the 'Boxable' class for the type 't'](#no-instance-of-the-boxable-class-for-the-type-t)
- [Records and Complex Instances](#records-and-complex-instances)
- [Expected kind 'Bool or Effect' here, but kind 'Type' is used](#expected-kind-bool-or-effect-here-but-kind-type-is-used)

## ToString is not defined on 'a'

Given a program like:

```flix
def main(): Unit \ IO = 
    let l = Nil;
    println(l)
```

Flix may report:

```
❌ -- Type Error ---------------------

>> ToString is not defined on a. [...]

3 |     println(l)
        ^^^^^^^^^^
        missing ToString instance
```

The issue is that the empty list has the polymorphic type: `List[a]` for any
`a`. This means that Flix cannot select the appropriate `ToString` type class
instance (even though any would work). 

The solution is to specify the type of the empty list. For example, we can write:

```flix
def main(): Unit \ IO = 
    let l: List[Int32] = Nil;
    println(l)
```

which solves the problem because Flix can find an instance of `ToString` for the
type `List[Int32]`.

## No instance of the 'Boxable' class for the type 't'

Given a program like:

```flix
def connected(l: List[(t, t)]): List[(t, t)] = 
    let db = inject l into Edge;
    let pr = #{
        Path(x, y) :- Edge(x, y).
        Path(x, z) :- Path(x, y), Edge(y, z).
    };
    query db, pr select (x, y) from Path(x, y)
```

which uses _polymorphic_ Datalog program values, Flix may report:

```
❌ -- Type Error ----------------------------------------

>> No instance of the 'Boxable' class for the type 't'.

7 |     query db, pr select (x, y) from Path(x, y)
                                        ^^^^^^^^^^
                                        missing instance
```

This is because Flix requires values used in Datalog constraints to be
`Boxable`. A type can be made boxable if it implements `Eq` and `Order`. 

In the above case, the solution is to change the signature of `connected` to:

```flix
def connected(l: List[(t, t)]): List[(t, t)] with Boxable[t] = 
```

## Records and Complex Instances

Given a program like:

```flix
instance Eq[{fstName = String, lstName = String}]
```

Flix reports:

```
❌ -- Instance Error --------------------------------------------------

>> Complex instance type '{ fstName = String, lstName = String }' in 'Eq'.

1 | instance Eq[{fstName = String, lstName = String}]
             ^^
             complex instance type
```

This is because, at least for the moment, it is not possible type define type
class instances on records (or Datalog schema rows). This may change in the
future. Until then, it is necessary to wrap the record in an algebraic data
type. For example:

```flix
enum Person({fstName = String, lstName = String})
```

and then we can define an implementation of `Eq` for the `Person` type:

```flix
instance Eq[Person] {
    pub def eq(x: Person, y: Person): Bool = 
        let Person(r1) = x;
        let Person(r2) = y;
        r1.fstName == r2.fstName and r1.lstName == r2.lstName
}
```

## Expected kind 'Bool or Effect' here, but kind 'Type' is used

In Flix the kind of every type variable is either inferred or assumed to be
`Type`. In some cases, this can lead to kind errors. 

For example, if we want to have an enum that wraps an effectful function we
might write: 

```flix
enum A[a, b, ef] {
    case A(a -> b \ ef)
}
```

but this gives the error:

```
❌ -- Kind Error -----------------------------------------------

>> Expected kind 'Bool or Effect' here, but kind 'Type' is used.

2 |     case A(a -> b \ ef)
                        ^^
                        unexpected kind.

Expected kind: Bool or Effect
Actual kind:   Type
```

The solution is to explicitly annotate the type variables `a`, `b`, and `ef`
with their kinds: 

```
enum A[a: Type, b: Type, ef: Bool] {
    case A(a -> b \ ef)
}
```

