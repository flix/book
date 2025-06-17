# Fixpoints

A unique feature of Flix is its built-in support for
fixpoint computations on _constraint on relations_
and _constraint on lattices_.

We assume that the reader is already familiar with
Datalog and focus on the Flix specific features.

## Using Flix to Solve Constraints on Relations

We can use Flix to solve a fixpoint computation
inside a function.

For example, given a set of edges `s`, a `src` node,
and `dst` node, compute if there is a path from `src`
to `dst`.
We can elegantly solve this problem as follows:

```flix
def isConnected(s: Set[(Int32, Int32)], src: Int32, dst: Int32): Bool =
    let rules = #{
        Path(x, y) :- Edge(x, y).
        Path(x, z) :- Path(x, y), Edge(y, z).
    };
    let edges = inject s into Edge/2;
    let paths = query edges, rules select true from Path(src, dst);
    not (paths |> Vector.isEmpty)

def main(): Unit \ IO =
    let s = Set#{(1, 2), (2, 3), (3, 4), (4, 5)};
    let src = 1;
    let dst = 5;
    if (isConnected(s, src, dst)) {
        println("Found a path between ${src} and ${dst}!")
    } else {
        println("Did not find a path between ${src} and ${dst}!")
    }
```

The `isConnected` function behaves like any other
function: We can call it with a set of edges
(`Int32`-pairs), an `Int32` source node, and
an `Int32` destination node.
What is interesting about `isConnected` is that its
implementation uses a small Datalog program to solve
the task at hand.

In the `isConnected` function, the local variable
`rules` holds a Datalog program fragment that
consists of two rules which define the `Path`
relation.
Note that the predicate symbols, `Edge` and `Path` do
not have to be explicitly introduced; they are simply
used.
The local variable `edges` holds a collection of edge
facts that are obtained by taking all the tuples in
the set `s` and turning them into `Edge` facts.
Next, the local variable `paths` holds the result of
computing the fixpoint of the facts and rules
(`edges` and `rules`) and selecting the Boolean
`true` _if_ there is a `Path(src, dst)` fact.
Note that here `src` and `dst` are the
lexically-bound function parameters.
Thus, `paths` is either an empty array (no paths were
found) or a one-element array (a path was found), and
we simply return this fact.

Flix is strongly typed.
Any attempt to use predicate symbol with terms of the
wrong type (or with the wrong arity) is caught by the
type checker.
Note also that Flix supports type inference, hence we
did not have to declare the type of `Edge` nor of
`Path`.

## Programming with First-class Constraints

A unique feature of Flix is its support for
_first-class constraints_.
A first-class constraint is a value that can be
constructed, passed around, composed with other
constraints, and ultimately solved.
The solution to a constraint system is another
constraint system which can be further composed.
For example:

```flix
def getParents(): #{ ParentOf(String, String) | r } = #{
    ParentOf("Pompey", "Strabo").
    ParentOf("Gnaeus", "Pompey").
    ParentOf("Pompeia", "Pompey").
    ParentOf("Sextus", "Pompey").
}

def getAdoptions(): #{ AdoptedBy(String, String) | r } = #{
    AdoptedBy("Augustus", "Caesar").
    AdoptedBy("Tiberius", "Augustus").
}

def withAncestors(): #{ ParentOf(String, String),
                        AncestorOf(String, String) | r } = #{
        AncestorOf(x, y) :- ParentOf(x, y).
        AncestorOf(x, z) :- AncestorOf(x, y), AncestorOf(y, z).
}

def withAdoptions(): #{ AdoptedBy(String, String),
                        AncestorOf(String, String) | r } = #{
    AncestorOf(x, y) :- AdoptedBy(x, y).
}

def main(): Unit \ IO =
    let c = false;
    if (c) {
        query getParents(), getAdoptions(), withAncestors()
            select (x, y) from AncestorOf(x, y) |> println
    } else {
        query getParents(), getAdoptions(), withAncestors(), withAdoptions()
            select (x, y) from AncestorOf(x, y) |> println
    }
```

The program uses three predicate symbols: `ParentOf`,
`AncestorOf`, and `AdoptedBy`.
The `getParents`function returns a collection of facts
that represent biological parents, whereas the
`getAdoptions` function returns a collection of facts
that represent adoptions.
The `withAncestors` function returns two constraints
that populate the `AncestorOf` relation using the
`ParentOf` relation.
The `withAdoptions` function returns a constraint
that populates the `ParentOf` relation using the
`AdoptedBy` relation.

In the `main` function the local variable `c`
controls whether we query a Datalog program that only
considers biological parents or if we include
adoptions.

As can be seen, the types the functions are
row-polymorphic.
For example, the signature of `getParents` is
`def getParents(): #{ ParentOf | r }` where `r`
is row polymorphic type variable that represent the
rest of the predicates that the result of the
function can be composed with.

> **Design Note**
>
> The row polymorphic types are best understood as an
> over-approximation of the predicates that may occur
> in a constraint system.
> For example, if a constraint system has type
> `#{ A(String), B(Int32, Int32) }` that doesn't
> necessarily mean that it will contain facts or rules
> that use the predicate symbols `A` or `B`, but it
> does guarantee that it will not contain any fact or
> rule that refer to a predicate symbol `C`.

## Polymorphic First-class Constraints

Another unique feature of Flix is its support for
first-class _polymorphic_ constraints.
That is, constraints where one or more constraints
are polymorphic in their term types.
For example:

```flix
def edgesWithNumbers(): #{ LabelledEdge(String, Int32 , String) | r } = #{
    LabelledEdge("a", 1, "b").
    LabelledEdge("b", 1, "c").
    LabelledEdge("c", 2, "d").
}

def edgesWithColor(): #{ LabelledEdge(String, String, String) | r } = #{
    LabelledEdge("a", "red", "b").
    LabelledEdge("b", "red", "c").
    LabelledEdge("c", "blu", "d").
}

def closure(): #{ LabelledEdge(String, l, String),
                  LabelledPath(String, l, String) } with Order[l] = #{
    LabelledPath(x, l, y) :- LabelledEdge(x, l, y).
    LabelledPath(x, l, z) :- LabelledPath(x, l, y), LabelledPath(y, l, z).
}

def main(): Unit \ IO =
    query edgesWithNumbers(), closure()
        select (x, l, z) from LabelledPath(x, l, z) |> println;
    query edgesWithColor(), closure()
        select (x, l, z) from LabelledPath(x, l, z) |> println
```

Here we use two predicate symbols: `LabelledEdge` and
`LabelledPath`.
Each predicate has a type parameter named `l` and is
polymorphic in the "label" type associated with the
edge/path.
Note how `edgesWithNumbers` returns a collection of
edge facts where the labels are integers, whereas
`edgesWithColor` returns a collection of facts where
the labels are strings.
The `closure` function is polymorphic and returns two
rules that compute the transitive closure of edges
that have the same label.

The Flix type system ensures that we cannot
accidentally mix edges (or paths) with different
types of labels.

## Injecting Facts into Datalog

Flix provides a flexible mechanism that allows
functional data structures (such as lists, sets,
and maps) to be converted into Datalog facts.

For example, given a Flix list of pairs we can
convert it to a collection of Datalog facts:

```flix
let l = (1, 2) :: (2, 3) :: Nil;
let p = inject l into Edge/2;
```

where `l` has type `List[(Int32, Int32)]`.
The `inject` expression converts `l` into a Datalog
constraint set `p` of type
`#{ Edge(Int32, Int32) | ... }`.
Note that predicate's arity is included in the
expression in `Edge/2`.
The general form is `Predicate/Arity`.

The `inject` expression works with any type that
implements the `Foldable` trait.
Consequently, it can be used with lists, sets, maps,
and so forth.

The `inject` expression can operate on multiple
collections simultaneously.
For example:

```flix
let names = "Lucky Luke" :: "Luke Skywalker" :: Nil;
let jedis = "Luke Skywalker" :: Nil;
let p = inject names, jedis into Name/1, Jedi/1;
```

where `p` has type
`#{ Name(String), Jedi(String) | ... }`.

## Pipelines of Fixpoint Computations

The solution (i.e. fixpoint) of a constraint system
is another constraint system.
We can use this to construct _pipelines_ of fixpoint
computations, i.e. to feed the result of one fixpoint
computation into another fixpoint computation.
For example:

```flix
def main(): Unit \ IO =
    let f1 = #{
        ColorEdge(1, "blue", 2).
        ColorEdge(2, "blue", 3).
        ColorEdge(3, "red", 4).
    };
    let r1 = #{
        ColorPath(x, c, y) :- ColorEdge(x, c, y).
        ColorPath(x, c, z) :- ColorPath(x, c, y), ColorEdge(y, c, z).
    };
    let r2 = #{
        ColorlessPath(x, y) :- ColorPath(x, _, y).
    };
    let m = solve f1, r1 project ColorPath;
    query m, r2 select (x, y) from ColorlessPath(x, y) |> println
```

The program uses three predicates: `ColorEdge`,
`ColorPath`, and `ColorlessPath`.
Our goal is to compute the transitive closure of the
colored edges and then afterwards construct a graph
where the edges have no color.

The program first computes the fixpoint of `f1` and
`r1` and injects out the `ColorPath` fact.
The result is stored in `m`. Next, the program
queries `m` and `r2`, and selects all `ColorlessPath`
facts.

