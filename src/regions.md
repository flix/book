# Regions

> **Note:** This documentation is relevant for Flix version 0.35.0 or higher.

Flix supports _scoped_ mutable memory. In Flix, all mutable memory belongs to a
_region_ that is tied to its lexical scope. Once execution leaves the lexical
scope of a region, all memory in that region becomes unreachable. 

<!-- 

Regions are helpful because they allow us to implement *pure functions* which internally use *mutation*.

We will illustrate this powerful idea with several real-world examples, but let us first discuss how to use a region:

We introduce a new region scope with the `region` construct:

```flix
region rh { // region starts.
  ...       // the region handle `rh` is in scope.
}           // region ends and all data associated with rh is no longer in scope.
```


We can use regions to implement a pure `sort` function that internally uses mutation:

```flix
def sort(l: List[a]): List[a] with Order[a] =
    region rh {
        let arr = List.toArray(r, l);  // effectful, has effect 'r'.
        Array.sort!(arr);              // effectful, has effect 'r'.
        Array.toList(arr)              // effectful, has effect 'r'.
    } // scope of r ends, the entire expression is pure.
```

Here we introduce a region named `rh`. We use the function `Array.toArray` to
convert the list `l` to a mutable array `arr` associated with the region `rh`.
We then sort `arr` using `Array.sort!` which uses an efficient in-place sorting
algorithm. Finally, we convert the array back to a list and return it.
-->