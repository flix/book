# Introduction to Flix

Flix is a principled functional, logic, and imperative programming language
developed at [Aarhus University](https://cs.au.dk/) and by a community of [open
source contributors](https://github.com/flix/flix) in collaboration with
researchers from the [University of Waterloo](https://uwaterloo.ca/), from the
[University of Tubingen](https://uni-tuebingen.de/), and from the [University of
Copenhagen](https://di.ku.dk/).

Flix is inspired by OCaml and Haskell with ideas from Rust and Scala. Flix looks
like Scala, but its type system is based on Hindley-Milner which supports
complete type inference. Flix aims to offer a unique combination of features
that no other programming language offers, including:

-   algebraic data types and pattern matching.
-   type classes with higher-kinded types.
-   structured concurrency based on channels and light-weight processes.

In addtion, Flix has several new powerful and unique features:

-   A polymorphic type and effect system with region-based local mutation.
-   Datalog constraints as first-class program values.
-   Function overloading based on purity reflection.

Flix compiles to efficient JVM bytecode, runs on the Java Virtual Machine, and
supports full tail call elimination. Flix has interoperability with Java and can
use JVM classes and methods. Hence the entire Java ecosystem is available from
within Flix.

Flix aims to have world-class Visual Studio Code support. The [Flix Visual
Studio Code extension](./vscode.md) uses the real Flix compiler hence there is
always a 1:1 correspondence between the Flix language and what is reported in
the editor. The advantages are many: (a) diagnostics are always exact, (b) code
navigation "just works", and (c) refactorings are always correct.

## Look'n Feel

Here are a few programs to illustrate the look and feel of Flix:

This program illustrates the use of **algebraic data types and pattern matching**:

```flix
/// An algebraic data type for shapes.
enum Shape {
    case Circle(Int32),          // circle radius
    case Square(Int32),          // side length
    case Rectangle(Int32, Int32) // height and width
}

/// Computes the area of the given shape using
/// pattern matching and basic arithmetic.
def area(s: Shape): Int32 = match s {
    case Shape.Circle(r)       => 3 * (r * r)
    case Shape.Square(w)       => w * w
    case Shape.Rectangle(h, w) => h * w
}

// Computes the area of a 2 by 4.
def main(): Unit \ IO =
    area(Shape.Rectangle(2, 4)) |> println
```

Here is an example that uses **polymorphic records**:

```flix
/// Returns the area of the polymorphic record `r`.
/// Note that the use of the type variable `a` permits the record `r`
/// to have labels other than `x` and `y`.
def polyArea[a : RecordRow](r: {x = Int32, y = Int32 | a}): Int32 = r.x * r.y

/// Computes the area of various rectangle records.
/// Note that some records have additional fields.
def polyAreas(): List[Int32] =
    polyArea({x = 1, y = 2}) ::
    polyArea({x = 2, y = 3, z = 4}) :: Nil

def main(): Unit \ IO =
    polyAreas() |> println
```

Here is an example that uses **region-based local mutation**:

```flix
///
/// We can define pure functions that use
/// internal mutability (impurity) with regions.
/// Regions encapsulate mutability to its declared scope.
///
def deduplicate(l: List[a]): List[a] with Order[a] =
    /// Declare a new region `rc`.
    region rc {

        /// Create a new `MutSet` at region `r`.
        /// This will be used to keep track of
        /// unique elements in `l`.
        let s = MutSet.new(rc);

        /// The lambda used in the call to `filter`
        /// would be impure without a region.
        List.filter(x -> {
            if (MutSet.memberOf(x, s))
                false // `x` has already been seen.
            else {
                MutSet.add!(x, s);
                true
            }
        }, l)
    }
```

Here is an example that uses **first-class Datalog constraints**:

```flix
def reachable(edges: List[(Int32, Int32)], src: Int32, dst: Int32): Bool =
    let db = inject edges into Edge;
    let pr = #{
        Path(x, y) :- Edge(x, y).
        Path(x, z) :- Path(x, y), Edge(y, z).
        Reachable() :- Path(src, dst).
    };
    let result = query db, pr select () from Reachable();
    not List.isEmpty(result)
```

And finally here is an example that uses **structured concurrency with channels
and processes**:

```flix
/// A function that sends every element of a list
def sendAll(l: List[Int32], tx: Sender[Int32, r]): Unit \ IO =
    match l {
        case Nil     => ()
        case x :: xs => Channel.send(x, tx); sendAll(xs, tx)
    }

/// A function that receives n elements
/// and collects them into a list.
def recvN(n: Int32, rx: Receiver[Int32, r]): List[Int32] \ IO =
    match n {
        case 0 => Nil
        case _ => Channel.recv(rx) :: recvN(n - 1, rx)
    }

/// A function that calls receive and sends the result on d.
def wait(rx: Receiver[Int32, r], n: Int32, tx: Sender[List[Int32], r]): Unit \ IO =
    Channel.send(recvN(n, rx), tx);
    ()

/// Spawn a process for send and wait, and print the result.
def main(): Unit \ IO = region rc {
    let l = 1 :: 2 :: 3 :: Nil;
    let (tx1, rx1) = Channel.buffered(rc, 100);
    let (tx2, rx2) = Channel.buffered(rc, 100);
    spawn sendAll(l, tx1) @ rc;
    spawn wait(rx1, List.length(l), tx2) @ rc;
    println(Channel.recv(rx2))
}
```

Additional examples can be found in these pages and in the [examples folder on
GitHub](https://github.com/flix/flix/tree/master/examples).
