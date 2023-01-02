# Local Predicates

Flix supports an abstract mechanism called _local predicates_. A local
predicate, like a local variable, is not visible to the outside. 

To understand local predicates, consider the following example: We can a write a
function that returns a Datalog program value which computes whether a graph has
a cycle: 

```flix
def cyclic(): #{Edge(Int32, Int32), Path(Int32, Int32), Cyclic()} = #{
    Path(x, y) :- Edge(x, y).
    Path(x, z) :- Path(x, y), Edge(y, z).
    Cyclic() :- Path(x, x).
}

def main(): Unit \ IO = 
    let db = #{
        Edge(1, 2).
        Edge(2, 3).
        Edge(3, 1).
    };
    query db, cyclic() select true from Cyclic() |> println
```

Here the `cyclic` function returns a _Datalog program value_ which consists of
three rules that compute the transitive closure of a graph of edges and whether
there is path from a vertex to itself. We use the `cyclic` function inside
`main` to determine if a small graph, given by `db`, has a cyclic. The program
prints `true :: Nil` when compiled and run. 

Returning to `cyclic`, we see that its type is:

```flix
def cyclic(): #{Edge(Int32, Int32), Path(Int32, Int32), Cyclic()} = ...
```

This is sensible because the Datalog program value uses the predicate symbols
`Edge`, `Path` and `Cyclic` with their given types. However, if we think more
about it, we can realize that the `Path` predicate is really local to the
computation: We are not meant to see it from the outside; it is an
implementation detail! What we really want is that `Edge(Int32, Int32)` should
be an _input_ and `Cyclic()` should be an _output_. More importantly,
`Path(Int32, Int32)` should not be visible from the outside nor part of the
type. We can achieve this with _predicate abstraction_:

```flix
def cyclic(): #{Edge(Int32, Int32), Cyclic()} = 
    #(Edge, Cyclic) -> #{
        Path(x, y) :- Edge(x, y).
        Path(x, z) :- Path(x, y), Edge(y, z).
        Cyclic() :- Path(x, x).
    }
```

Here we use the syntax `#(Edge, Cyclic) -> v` to specific that _only_ the
predicates `Edge` and `Cyclic` from within `v` should be visible to the outside.
Thus we can omit `Path(Int32, Int32)` from the return type of `cyclic`.
Moreover, the Datalog program value no longer contains a `Path` predicate symbol
that can be referenced. We can evidence this by observing that the program:

```flix
def main(): Unit \ IO = 
    let db = #{
        Edge(1, 2).
        Edge(2, 3).
        Edge(3, 1).
    };
    query db, cyclic() select (x, y) from Path(x, y) |> println
```

prints the empty list `Nil` since `Path` has been made local by the predicate
abstraction.
