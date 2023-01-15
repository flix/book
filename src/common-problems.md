# Common Problems

- [ToString is not defined on 'a'](#tostring-is-not-defined-on-a)
- [No instance of the 'Boxable' class for the type 't'](#no-instance-of-the-boxable-class-for-the-type-t)
- [Records and Complex Instances](#records-and-complex-instances)
- [Expected kind 'Bool or Effect' here, but kind 'Type' is used](#expected-kind-bool-or-effect-here-but-kind-type-is-used)

## ToString is not defined on 'a'

Given the program:

```flix
def main(): Unit \ IO = 
    let l = Nil;
    println(l)
```

The Flix compiler reports:

```
❌ -- Type Error ---------------------

>> ToString is not defined on a. [...]

3 |     println(l)
        ^^^^^^^^^^
        missing ToString instance
```

The issue is that the empty list has the polymorphic type: `List[a]` for any
`a`. This means that Flix cannot select the appropriate `ToString` type class
instance. 

The solution is to specify the type of the empty list. For example, we can write:

```flix
def main(): Unit \ IO = 
    let l: List[Int32] = Nil;
    println(l)
```

which solves the problem because Flix can find an instance of `ToString` type
class for the concrete type `List[Int32]`.

## No instance of the 'Boxable' class for the type 't'

Given the program:

```flix
def connected(l: List[(t, t)]): List[(t, t)] = 
    let db = inject l into Edge;
    let pr = #{
        Path(x, y) :- Edge(x, y).
        Path(x, z) :- Path(x, y), Edge(y, z).
    };
    query db, pr select (x, y) from Path(x, y)
```

which uses _polymorphic_ Datalog program values, the Flix compiler reports:

```
❌ -- Type Error ----------------------------------------

>> No instance of the 'Boxable' class for the type 't'.

7 |     query db, pr select (x, y) from Path(x, y)
                                        ^^^^^^^^^^
                                        missing instance
```

This is because Flix requires values used in Datalog constraints to be
`Boxable`. Any type can be made `Boxable` by implementing the `Eq` and `Order`
type classes. 

In the above case, the solution is to change the signature of `connected` to:

```flix
def connected(l: List[(t, t)]): List[(t, t)] with Boxable[t] = 
```

which captures the `Boxable` type class constraint.

## Records and Complex Instances

Given the program:

```flix
instance Eq[{fstName = String, lstName = String}]
```

The Flix compiler reports:

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

and then we can implement `Eq` for the `Person` type:

```flix
instance Eq[Person] {
    pub def eq(x: Person, y: Person): Bool = 
        let Person(r1) = x;
        let Person(r2) = y;
        r1.fstName == r2.fstName and r1.lstName == r2.lstName
}
```

## Expected kind 'Bool or Effect' here, but kind 'Type' is used

Given the program:

```flix
enum A[a, b, ef] {
    case A(a -> b \ ef)
}
```

The Flix compiler reports:

```
❌ -- Kind Error -----------------------------------------------

>> Expected kind 'Bool or Effect' here, but kind 'Type' is used.

2 |     case A(a -> b \ ef)
                        ^^
                        unexpected kind.

Expected kind: Bool or Effect
Actual kind:   Type
```

This is because Flix assumes every un-annotated type variable to have kind
`Type`. However, in the above case `a` and `b` should have kind `Type`, but `ef`
should have kind `Bool`. We can make this explicit like so:

```flix
enum A[a: Type, b: Type, ef: Bool] {
    case A(a -> b \ ef)
}
```
