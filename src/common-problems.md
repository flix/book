# Common Problems

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

