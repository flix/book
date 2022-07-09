# Introduction to Flix

Flix is a principled functional, logic, and
imperative programming language developed at
[Aarhus University](https://cs.au.dk/), at the
[University of Waterloo](https://uwaterloo.ca/), and
by a community of
[open source contributors](https://github.com/flix/flix).

Flix is inspired by OCaml and Haskell with ideas from
Rust and Scala.
Flix looks like Scala, but its type system is based
on Hindley-Milner.
Two unique features of Flix are its polymorphic
effect system and its support for first-class Datalog
constraints.
Flix compiles to efficient JVM bytecode, runs on the
Java Virtual Machine, and supports full tail call
elimination.

Here are a few Flix programs to illustrate the look
and feel of the language:

This program illustrates the use of algebraic data
types and pattern matching:

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
def main(): Unit & Impure =
    area(Rectangle(2, 4)) |> println
```

Here is a Flix program using polymorphic records:

```flix
/// Returns the area of the polymorphic record `r`.
/// Note that the use of the type variable `a` permits the record `r`
/// to have labels other than `x` and `y`.
def polyArea[a : RecordRow](r: {x:: Int32, y:: Int32 | a}): Int32 = r.x * r.y

/// Computes the area of various rectangle records.
/// Note that some records have additional fields.
def polyAreas(): List[Int32] =
    polyArea({x = 1, y = 2}) ::
    polyArea({x = 2, y = 3, z = 4}) :: Nil

def main(): Unit & Impure =
    polyAreas() |> println
```

and here is one using processes and channels:

```flix
/// A function that sends every element of a list
def send(o: Channel[Int32], l: List[Int32]): Unit & Impure =
    match l {
        case Nil     => ()
        case x :: xs => o <- x; send(o, xs)
    }

/// A function that receives n elements
/// and collects them into a list.
def recv(i: Channel[Int32], n: Int32): List[Int32] & Impure =
    match n {
        case 0 => Nil
        case _ => (<- i) :: recv(i, n - 1)
    }

/// A function that calls receive and sends the result on d.
def wait(i: Channel[Int32], n: Int32, d: Channel[List[Int32]]): Unit & Impure =
    d <- recv(i, n);
    ()

/// Spawn a process for send and wait, and print the result.
def main(): Unit & Impure =
    let l = 1 :: 2 :: 3 :: Nil;
    let c = chan Int32 100;
    let d = chan List[Int32] 100;
    spawn send(c, l);
    spawn wait(c, List.length(l), d);
    println(<- d)
```

