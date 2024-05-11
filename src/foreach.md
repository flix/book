## Foreach

Flix supports a traditional _foreach_ construct that enables imperative
iteration through collections. 

We typically use the _foreach_ construct when we want to iterate through one or
more collections and execute an effectful operation for each of their elements.

For example, the program:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    foreach(fruit <- fruits) 
        println(fruit)
```

Prints the strings `Apple`, `Pear`, and `Mango`.

We can also iterate through multiple collections:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach(fruit <- fruits) 
        foreach(cream <- creams)
            println("Would you like some ${fruit} with ${cream} icecream?")
```

The same loop can also be written:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach(fruit <- fruits; cream <- creams) 
        println("Would you like some ${fruit} with ${cream} icecream?")
```

We can also write loops with a filter. For example:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach(fruit <- fruits; if isExcotic(fruit); cream <- creams) 
        println("Would you like some ${fruit} with ${cream} icecream?")

def isExcotic(fruit: String): Bool = match fruit {
    case "Mango" => true
    case _       => false
}
```

### Adding Optional Braces for Visual Clarity

We can sometimes improve the visual clarity of a `foreach` expression by adding
braces:

```flix
foreach(fruit <- fruits) {
    foreach(cream <- creams) {
        println("Would you like some ${fruit} with ${cream} icecream?")
    }
}
```

The braces have no impact on the meaning of the `foreach` loop; they are purely
stylistic. 

### The Iterable Trait

We can use the `foreach` syntax to iterate through any collection type that
implements the `Iterable` trait. In particular, the `Iterable` trait
defines a single signature: 

```flix
///
/// A trait for immutable data structures that can be iterated.
///
pub trait Iterable[t] {
     ///
    /// The element type of the Iterable.
    ///
    type Elm[t]: Type

    ///
    /// Returns an iterator over `t`.
    ///
    pub def iterator(rc: Region[r], t: t): Iterator[Iterable.Elm[t], r + aef, r] \ (r + aef) where Iterable.Aef[t] ~ aef
}
```

> **Note:** Flix expects the expression body of a `foreach` to have type `Unit`.
> If you want to return a value from the loop body, you should use the
> `foreach-yield` construct. 
