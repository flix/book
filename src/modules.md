# Modules

> This section is work in progress.

Flix supports hierarchical modules as known from many other programming
languages.

## Declaring and Using Modules

We declare modules using the `mod` keyword followed by the namespace and name of
the module. 

For example, we can declare a module:

```flix
mod Math {
    pub def sum(x: Int32, y: Int32): Int32 = x + y
}
```

Here we have declared a module called `Math` with a function called `sum` inside
it. We can refer to the `sum` function, from outside of its module, using its
fully-qualified name:

```flix
def main(): Unit \ IO = 
    let result = Math.sum(123, 456);
    println(result)
```

Alternatively, we can bring the `sum` function into local scope with `use`:

```flix
def main(): Unit \ IO = 
    use Math.sum;
    let result = sum(123, 456);
    println(result)
```

## Declaring Modules



<!--
Namespaces are hierarchical, so we can declare a
deeper namespace:

```flix
namespace Core/Math {
    def sum(x: Int32, y32: Int): Int32 = x + y
}
```

Note that the fragments of a namespace are separated
by `/`.

We can freely nest namespaces.
For example:

```flix
namespace Core {
    namespace Math {

        def sum(x: Int32, y: Int32): Int32 = x + y

        namespace Stats {
            def median(xs: List[Int32]): Int32 = ???
        }
    }
}
```

## Using Definitions from a Namespace

We can refer to definitions from a namespace by their
fully-qualified name.
For example:

```flix
namespace Core/Math {
    pub def sum(x: Int32, y: Int32): Int32 = x + y
}

def main(): Unit \ IO =
    Core/Math.sum(21, 42) |> println
```

Note that we must declare `sum` as public (`pub`) to
allow access to it from outside its own namespace.

It can quickly get tedious to refer to definitions by
their fully-qualified name.

The `use` construct allows us to "import" definitions
from another namespace:

```flix
namespace Core/Math {
    pub def sum(x: Int32, y: Int32): Int32 = x + y
}

def main(): Unit \ IO =
    use Core/Math.sum;
    sum(21, 42) |> println
```

Here the `use` is local to the `main` function.
A `use` can also appear at the top of a file:

```flix
use Core/Math.sum;

def main(): Unit \ IO =
    sum(21, 42) |> println

namespace Core/Math {
    pub def sum(x: Int32, y: Int32): Int32 = x + y
}
```

## Using Multiple Definitions from a Namespaces

We can also use multiple definitions from a namespace:

```flix
use Core/Math.sum;
use Core/Math.mul;

def main(): Unit \ IO =
    mul(42, 84) |> sum(21) |> println

namespace Core/Math {
    pub def sum(x: Int32, y: Int32): Int32 = x + y
    pub def mul(x: Int32, y: Int32): Int32 = x * y
}
```

Multiple such uses can be grouped together:

```flix
use Core/Math.{sum, mul};

def main(): Unit \ IO =
    mul(42, 84) |> sum(21) |> println

namespace Core/Math {
    pub def sum(x: Int32, y: Int32): Int32 = x + y
    pub def mul(x: Int32, y: Int32): Int32 = x * y
}
```

> **Design Note**
>
> Flix does not support _wildcard_ uses because they
> are inherently ambiguous and may lead to subtle
> errors during refactoring.

## Avoiding Name Clashes with Renaming

We can use renaming to avoid name clashes between
identically named definitions.
For example:

```flix
use A.{concat => stringConcat};
use B.{concat => listConcat};

def main(): Unit \ IO =
    stringConcat("Hello", " World!") |> println

namespace A {
    pub def concat(x: String, y: String): String = x + y
}

namespace B {
    pub def concat(xs: List[Int32], ys: List[Int32]): List[Int32] = xs ::: ys
}
```

In many cases a better approach is to use a _local_
`use` to avoid the problem in the first place.

## Using Types from a Namespace

We can use types from a namespace in the same way as
definitions.
For example:

```flix
use A/B.Color;

def redColor(): Color = Color.Red

namespace A/B {
    pub enum Color {
        case Red, Blue
    }
}
```

We can also use _type aliases_ in the same way:

```flix
use A/B.Color;
use A/B.Hue;

def blueColor(): Hue = Color.Blue

namespace A/B {
    pub enum Color {
        case Red, Blue
    }
    pub type alias Hue = Color
}
```

## Using Enums from a Namespace

We can use enumerated types from a namespace.
For example:

```flix
def blueIsRed(): Bool =
    use A/B.Color.{Blue, Red};
    Blue != Red

namespace A/B {
    pub enum Color with Eq {
        case Red, Blue
    }
}
```

Note that `A/B.Color` is the fully-qualified name of
a _type_ whereas `A/B.Color.Red` is the
fully-qualified name of a _tag_ inside an enumerated
type.
That is, a fully-qualified definition is of the
form `A/B/C.d`, a fully-qualified type is of the
form `A/B/C.D`, and finally a fully-qualified tag is
of the form `A/B/C.D.T`.

-->
