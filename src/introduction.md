# Introduction to Flix

Flix is a principled functional, logic, and imperative programming language
developed at [Aarhus University](https://cs.au.dk/), at the [University of
Waterloo](https://uwaterloo.ca/), and by a community of [open source
contributors](https://github.com/flix/flix).

Flix is inspired by OCaml and Haskell with ideas from Rust and Scala. Flix looks
like Scala, but its type system is based on Hindley-Milner. Two unique features
of Flix are its polymorphic effect system and its support for first-class
Datalog constraints. Flix compiles to efficient JVM bytecode, runs on the Java
Virtual Machine, and supports full tail call elimination.

Here are a few Flix programs to illustrate the look and feel of the language:

This program illustrates the use of algebraic data types and pattern matching:

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
    case Circle(r)       => 3 * (r * r)
    case Square(w)       => w * w
    case Rectangle(h, w) => h * w
}

// Computes the area of a 2 by 4.
def main(): Unit \ IO =
    area(Rectangle(2, 4)) |> println
```

Here is a Flix program using polymorphic records:

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

and here is one using processes and channels:

```flix
/// A function that sends every element of a list
def sendAll(l: List[Int32], o: Sender[Int32]): Unit \ IO =
    match l {
        case Nil     => ()
        case x :: xs => Channel.send(x, o); sendAll(xs, o)
    }

/// A function that receives n elements
/// and collects them into a list.
def recvN(n: Int32, i: Receiver[Int32]): List[Int32] \ IO =
    match n {
        case 0 => Nil
        case _ => Channel.recv(i) :: recvN(n - 1, i)
    }

/// A function that calls receive and sends the result on d.
def wait(i: Receiver[Int32], n: Int32, d: Sender[List[Int32]]): Unit \ IO =
    Channel.send(recvN(n, i), d);
    ()

/// Spawn a process for send and wait, and print the result.
def main(): Unit \ IO =
    let l = 1 :: 2 :: 3 :: Nil;
    let (s1, r1) = Channel.buffered(100);
    let (s2, r2) = Channel.buffered(100);
    spawn sendAll(l, s1);
    spawn wait(r1, List.length(l), s2);
    println(Channel.recv(r2))
```
