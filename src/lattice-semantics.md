## Using Flix to Solve Constraints on Lattices

Flix supports not only _constraints on relations_,
but also _constraints on lattices_.
To create such constraints, we must first define the
lattice operations (the partial order, the least
upper bound, and so on) as functions, associate them
with a type, and then declare the predicate symbols
that have lattice semantics.

We begin with the definition of the `Sign` data type:

```flix
enum Sign {
    case Top,
    case Neg,
    case Zer,
    case Pos,
    case Bot
}
```

We need to define the usual `Eq`, `Order`, and
`ToString` instances for this new type.
Note that the order instance is unrelated to the
partial order instance we will later define, and is
simply used to sort elements for pretty printing etc.

```flix
instance Eq[Sign] {
    pub def eq(x: Sign, y: Sign): Bool = match (x, y) {
        case (Bot, Bot) => true
        case (Neg, Neg) => true
        case (Zer, Zer) => true
        case (Pos, Pos) => true
        case (Top, Top) => true
        case _          => false
    }
}

instance Order[Sign] {
    pub def compare(x: Sign, y: Sign): Comparison =
        let num = w -> match w {
            case Bot => 0
            case Neg => 1
            case Zer => 2
            case Pos => 3
            case Top => 4
        };
        num(x) <=> num(y)
}

instance ToString[Sign] {
    pub def toString(x: Sign): String = match x {
        case Bot => "Bot"
        case Neg => "Neg"
        case Zer => "Zer"
        case Pos => "Pos"
        case Top => "Top"
    }
}
```

With these trait instances in place, we can now
define the lattice operations on `Sign`.

We define the bottom element and the partial order:

```flix
instance LowerBound[Sign] {
    pub def minValue(): Sign = Bot
}

instance PartialOrder[Sign] {
    pub def lessEqual(x: Sign, y: Sign): Bool =
        match (x, y) {
            case (Bot, _)   => true
            case (Neg, Neg) => true
            case (Zer, Zer) => true
            case (Pos, Pos) => true
            case (_, Top)   => true
            case _          => false
        }
}
```

Next, we define the least upper bound and greatest
lower bound:

```flix
instance JoinLattice[Sign] {
    pub def leastUpperBound(x: Sign, y: Sign): Sign =
        match (x, y) {
            case (Bot, _)   => y
            case (_, Bot)   => x
            case (Neg, Neg) => Neg
            case (Zer, Zer) => Zer
            case (Pos, Pos) => Pos
            case _          => Top
        }
}

instance MeetLattice[Sign] {
    pub def greatestLowerBound(x: Sign, y: Sign): Sign =
        match (x, y) {
            case (Top, _)   => y
            case (_, Top)   => x
            case (Neg, Neg) => Neg
            case (Zer, Zer) => Zer
            case (Pos, Pos) => Pos
            case _          => Bot
        }
}
```

With all of these definitions we are ready to write
Datalog constraints with lattice semantics.
But before we proceed, let us also write a single
monotone function:

```flix
def sum(x: Sign, y: Sign): Sign = match (x, y) {
    case (Bot, _)   => Bot
    case (_, Bot)   => Bot
    case (Neg, Zer) => Neg
    case (Zer, Neg) => Neg
    case (Zer, Zer) => Zer
    case (Zer, Pos) => Pos
    case (Pos, Zer) => Pos
    case (Pos, Pos) => Pos
    case _          => Top
}
```

We can now finally put everything to use:

```flix
pub def main(): Unit \ IO =
    let p = #{
        LocalVar("x"; Pos).
        LocalVar("y"; Zer).
        LocalVar("z"; Neg).
        AddStm("r1", "x", "y").
        AddStm("r2", "x", "y").
        AddStm("r2", "y", "z").
        LocalVar(r; sum(v1, v2)) :-
            AddStm(r, x, y), LocalVar(x; v1), LocalVar(y; v2).
    };
    query p select (r, v) from LocalVar(r; v) |> println
```

Note the careful use of `;` to designate lattice
semantics.

### Using Lattice Semantics to Compute Shortest Paths

We can also use lattice semantics to compute shortest paths.

The key is to define our own new data type `D` which is simple an `Int32` with
forms a lattice with the reverse order of the integers (e.g. the smallest
element is `Int32.maxValue()`).

```flix
pub enum D with Eq, Order, ToString {
    case D(Int32)
}

instance PartialOrder[D] {
    pub def lessEqual(x: D, y: D): Bool =
        let D(n1) = x;
        let D(n2) = y;
        n1 >= n2        // Note: Order reversed.
}

instance LowerBound[D] {
    // Note: Because the order is reversed, the largest value is the smallest.
    pub def minValue(): D = D(Int32.maxValue())
}

instance UpperBound[D] {
    // Note: Because the order is reversed, the smallest value is the largest.
    pub def maxValue(): D = D(Int32.minValue())
}

instance JoinLattice[D] {
    pub def leastUpperBound(x: D, y: D): D =
        let D(n1) = x;
        let D(n2) = y;
        D(Int32.min(n1, n2))        // Note: Order reversed.
}

instance MeetLattice[D] {
    pub def greatestLowerBound(x: D, y: D): D =
        let D(n1) = x;
        let D(n2) = y;
        D(Int32.max(n1, n2))        // Note: Order reversed.
}

def shortestPath(g: Set[(t, Int32, t)], o: t): Map[t, D] with Order[t] =
    let db = inject g into Edge/3;
    let pr = #{
        Dist(o; D(0)).
        Dist(y; add(d1 , D(d2))) :- Dist(x; d1), Edge(x, d2, y).
    };
    query db, pr select (x , d) from Dist(x; d) |> Vector.toMap

def add(x: D, y: D): D =
    let D(n1) = x;
    let D(n2) = y;
    D(n1 + n2)

def main(): Unit \ IO =
    let g = Set#{
        ("Aarhus", 200, "Flensburg"),
        ("Flensburg", 150, "Hamburg")
    };
    println(shortestPath(g, "Aarhus"))

```

Flix actually comes with a type like `D` built-in. It's called `Down` and simply
reverses the order on the underlying type. We can use it and write the program
as:

```flix
use Down.Down;

def shortestPaths(g: Set[(t, Int32, t)], o: t): Map[t, Down[Int32]] with Order[t] =
    let db = inject g into Edge/3;
    let pr = #{
        Dist(o; Down(0)).
        Dist(y; add(d1 , Down(d2))) :- Dist(x; d1), Edge(x, d2, y).
    };
    query db, pr select (x , d) from Dist(x; d) |> Vector.toMap

def add(x: Down[Int32], y: Down[Int32]): Down[Int32] =
    let Down(n1) = x;
    let Down(n2) = y;
    Down(n1 + n2)

def main(): Unit \ IO =
    let g = Set#{
        ("Aarhus", 200, "Flensburg"),
        ("Flensburg", 150, "Hamburg")
    };
    println(shortestPaths(g, "Aarhus"))

```
