# Foreach

Flix supports a traditional _foreach_ construct that enables imperative
iteration through collections. 

We typically use the _foreach_ construct when we want to iterate through one or
more collections and execute an effectful operation for each of their elements.

For example, the program:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    foreach (fruit <- fruits) 
        println(fruit)
```

Prints the strings `Apple`, `Pear`, and `Mango`.

We can also iterate through multiple collections:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach (fruit <- fruits) 
        foreach (cream <- creams)
            println("Would you like some ${fruit} with ${cream} icecream?")
```

The same loop can also be written:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach (fruit <- fruits; cream <- creams) 
        println("Would you like some ${fruit} with ${cream} icecream?")
```

We can also write loops with a filter. For example:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach (fruit <- fruits; if isExcotic(fruit); cream <- creams) 
        println("Would you like some ${fruit} with ${cream} icecream?")

def isExcotic(fruit: String): Bool = match fruit {
    case "Mango" => true
    case _       => false
}
```

## Adding Optional Braces for Visual Clarity

We can sometimes improve the visual clarity of a `foreach` expression by adding
braces:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach (fruit <- fruits) {
        foreach (cream <- creams) {
            println("Would you like some ${fruit} with ${cream} icecream?")
        }
    }
```

The braces have no impact on the meaning of the `foreach` loop; they are purely
stylistic. 

## The ForEach Trait

We can use the `foreach` syntax to iterate through any collection type that
implements the `ForEach` trait. In particular, the `ForEach` trait
defines a single signature:

```flix
///
/// A trait for data structures that support a forEach operation.
///
trait ForEach[t] {

    ///
    /// The type of elements in the data structure.
    ///
    type Elm: Type

    ///
    /// The effect of `forEach`.
    ///
    type Aef: Eff = {}

    ///
    /// Applies `f` to each element in the data structure.
    ///
    pub def forEach(f: ForEach.Elm[t] -> Unit \ ef, t: t): Unit \ (ef + ForEach.Aef[t])

}
```

> **Note:** Flix expects the expression body of a `foreach` to have type `Unit`.

## ForEach Combinators

The `ForEach` module provides four combinators that transform how a collection is
iterated: `withIndex`, `withFilter`, `withMap`, and `withZip`. Each combinator
wraps a collection and returns a new `ForEach`-compatible value that can be used
directly with the `foreach` syntax.

### Iterating with an Index

The `withIndex` combinator pairs each element with its zero-based index:

```flix
use ForEach.withIndex;
def main(): Unit \ IO =
    let langs = List#{"Flix", "Haskell", "Scala"};
    foreach ((i, lang) <- withIndex(langs)) {
        println("${i}: ${lang}")
    }
```

This prints:

```
0: Flix
1: Haskell
2: Scala
```

### Filtering Elements

The `withFilter` combinator skips elements that do not satisfy a predicate:

```flix
use ForEach.withFilter;
def main(): Unit \ IO =
    let numbers = List#{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    foreach (x <- withFilter(x -> x `Int32.modulo` 2 == 0, numbers)) {
        println("${x}")
    }
```

This prints only the even numbers: `2`, `4`, `6`, `8`, `10`.

### Mapping Elements

The `withMap` combinator applies a transformation to each element before it is
yielded:

```flix
use ForEach.withMap;
def main(): Unit \ IO =
    let numbers = List#{1, 2, 3, 4, 5};
    foreach (x <- withMap(x -> x * 10, numbers)) {
        println("${x}")
    }
```

This prints `10`, `20`, `30`, `40`, `50`.

### Zipping Two Collections

The `withZip` combinator zips two collections element-wise, producing pairs. The
iteration stops when the shorter collection is exhausted:

```flix
use ForEach.withZip;
def main(): Unit \ IO =
    let names = List#{"Alice", "Bob", "Carol"};
    let ages = List#{30, 25, 40};
    foreach ((name, age) <- withZip(names, ages)) {
        println("${name} is ${age} years old")
    }
```

> **Note:** `withZip` requires both collections to implement the `Iterable`
> trait (not just `ForEach`).
