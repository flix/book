## Foreach-Yield

> **Note:** This feature is not yet available.

Flix supports a special `foreach-yield` construct which is used to build
collections from other collections. The `foreach-yield` construct is related to
the `foreach` construct, but should not be confused with it. The `foreach`
construct is for effectful iteration through collections whereas the
`foreach-yield` construct is for building new collections. 

We can use the `foreach-yield` construct to build a new collection from existing
collections. For example:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    let result: Set[(String, String)] =
        foreach(fruit <- fruits; cream <- creams)
            yield (fruit, cream);
    println(result)
```

Here we construct a `Set[(String, String)]` from two `List[String]`. The type of
the resulting collection is typically inferred, but in this case we have placed
an explicit type annotation on the `result` local variable to specify it. 

We can use the `foreach-yield` construct with several different types of
collections. For example: 

```flix
def main(): Unit \ IO = 
    let c1 = Some(1);
    let c2 = Set#{1, 2, 3};
    let c3 = List#{1, 2, 3};
    let result: Set[Int32] =
        foreach(x <- c1; y <- c2; z <- c3)
            yield x + y + z;
    println(result)
```

Here we iterate through three collections `c1`, `c2`, and `c3` and return a set
of the sums of their pairwise combinations. 

### The Collectable Type Class 

The workhorse behind the `foreach-yield` construct is the `Iterable` type class
(discussed in the previous section) and the `Collectable` type class. 

```flix
pub class Collectable[m: Type -> Type] {
    ///
    /// Run an Iterator collecting the results.
    ///
    pub def collect(iter: Iterator[a, r]): m[a] \ r with Order[a]
}
```

Without going into details, the `Collectable` type class is implemented by all
kinds of collections that can be constructed from an iterator. Notably, this
includes the `List`, `Chain`, and `Set` data types. 

> **Note:** We cannot collect into a non-empty chain (`Nec`) or non-empty list
> (`Nel`) since we cannot guarantee that an `Iterator` is non-empty.

> **Note:** The `foreach-yield` construct can only collect into immutable
> collections. If we want to build a mutable collection, we should explicitly
> introduce its region, allocate the mutable collection, and add each element
> using a regular `foreach`-loop.
