# Modules

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

## Using Multiple Declarations from a Module

If we have multiple declarations in a module:

```flix
mod Math {
    pub def sum(x: Int32, y: Int32): Int32 = x + y
    pub def mul(x: Int32, y: Int32): Int32 = x * y
}
```

We can, of course, `use` each declaration:

```flix
use Math.sum;
use Math.mul;

def main(): Unit \ IO =
    mul(42, 84) |> sum(21) |> println
```

but a shorter way is to group the `use`s together into one:

```flix
use Math.{sum, mul};

def main(): Unit \ IO =
    mul(42, 84) |> sum(21) |> println
```

> **Note:** Flix does not support wildcard uses since they can lead to subtle
> bugs.

## Avoiding Name Clashes with Renaming

We can use renaming to avoid name clashes between identically named declarations.

For example, if we have two modules:

```flix
mod A {
    pub def concat(x: String, y: String): String = x + y
}

mod B {
    pub def concat(xs: List[Int32], ys: List[Int32]): List[Int32] = xs ::: ys
}
```

We can then `use` each `concat` function under a unique name. For example:

```flix
use A.{concat => concatStrings}
use B.{concat => concatLists}

def main(): Unit \ IO =
    concatStrings("Hello", " World!") |> println
```

While this feature is powerful, in many cases using a fully-qualified might be
more appropriate.

## Modules and Enums

We can define an enum inside a module. For example:

```flix
mod Zoo {
    pub enum Animal {
        case Cat,
        case Dog,
        case Fox
    }
}
```

Here the `Zoo` module contains an enum type named `Animal` which has three
cases: `Cat`, `Dog`, and `Fox`. 

We can access the type and the cases using their fully-qualified names:

```flix
def says(a: Zoo.Animal): String = match a {
    case Zoo.Animal.Cat => "Meow"
    case Zoo.Animal.Dog => "Woof"
    case Zoo.Animal.Fox => "Roar"
}

def main(): Unit \ IO = 
    println("A cat says ${says(Zoo.Animal.Cat)}!")
```

Alternatively, we can `use` both the `Animal` type and its cases:

```flix
use Zoo.Animal
use Zoo.Animal.Cat
use Zoo.Animal.Dog
use Zoo.Animal.Fox

def says(a: Animal): String = match a {
    case Animal.Cat => "Meow"
    case Animal.Dog => "Woof"
    case Animal.Fox => "Roar"
}

def main(): Unit \ IO = 
    println("A cat says ${says(Cat)}!")
```

Note that `use Zoo.Animal` brings the `Animal` _type_ into scope, whereas `use
Zoo.Animal.Cat` brings the `Cat` _case_ into scope.

## Modules and Type Classes

We can also define a type class inside a module. The mechanism is similar to
enums inside modules. 

For example, we can write:

```flix
mod Zoo {
    pub class Speakable[t] {
        pub def say(x: t): String
    }
}

enum Animal with ToString {
    case Cat,
    case Dog,
    case Fox
}

instance Zoo.Speakable[Animal] {
    pub def say(a: Animal): String = match a {
        case Cat => "Meow"
        case Dog => "Woof"
        case Fox => "Roar"
    }
}
```

We can use fully-qualified names to write:

```flix
def speak(x: t): Unit \ IO with Zoo.Speakable[t], ToString[t] = 
    println("A ${x} says ${Zoo.Speakable.say(x)}!")

def main(): Unit \ IO = 
    speak(Animal.Cat)
```

Or we can `use` the `Zoo.Speakable` type class and the `Zoo.Speakable.say`
function: 

```flix
use Zoo.Speakable
use Zoo.Speakable.say

def speak(x: t): Unit \ IO with Speakable[t], ToString[t] = 
    println("A ${x} says ${say(x)}!")
```
