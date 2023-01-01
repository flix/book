# Using Flix to Solve Constraints on Lattices

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
instance Boxable[Sign]

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

With these type class instances in place, we can now
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
