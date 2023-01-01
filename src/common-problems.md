# Common Problems

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

