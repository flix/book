## Regions

> **Note:** This documentation is relevant for Flix version 0.35.0 or higher.

Flix supports _scoped_ mutable memory. In Flix, all mutable memory belongs to a
_region_ that is tied to its lexical scope. When execution leaves the lexical
scope of a region, all memory in that region becomes unreachable. 

Regions are useful because they enable us to implement _pure functions_ that
internally uses _mutation_. We will illustrate this powerful idea with several
real-world examples, but let us first discuss how to use a region:

We introduce a new region scope with the `region` construct:

```flix
region rc { // region starts.
  ...       // the region handle `rc` is in scope.
}           // region ends and all data associated with `rc` is no longer in scope.
```

We can use regions to implement a pure `sort` function that internally uses mutation:

```flix
def sort(l: List[a]): List[a] with Order[a] =
    region rc {
        let arr = List.toArray(rc, l);
        Array.sort!(arr);
        Array.toList(arr)
    }
```

Here we introduce a region named `rc`. We use the function `Array.toArray` to
convert the list `l` to a mutable array `arr` associated with the region `rc`.
We then sort `arr` using `Array.sort!` which uses an efficient in-place sorting
algorithm. Finally, we convert the sorted array back to a list and return it.
The `sort` function is pure, even though it internally uses mutation.

As another example, we can implement a `toString` function for `List[a]` which
is pure but internally uses a mutable `StringBuilder`:

```flix
def toString(l: List[a]): String with ToString[a] =
    region rc {
        let sb = new StringBuilder(rc);
        List.forEach(x -> StringBuilder.appendString!("${x} :: ", sb), l);
        StringBuilder.appendString!("Nil", sb);
        StringBuilder.toString(sb)
    } // scope of rc ends, the entire expression is pure.
```

The programming pattern is the same: We open a new region, allocate a
`StringBuilder` in the region, fill the builder with strings, and convert it
into one string.

We can use regions to implement certain _functional operations_ more
efficiently. For example, here is a fast implementation of `List.flatMap`:

```flix
def flatMap(f: a -> List[b] \ ef, l: List[a]): List[b] \ ef =
    region rc {
        let ml = MutList.new(rc);
        l |> List.forEach(x -> MutList.append!(f(x), ml));
        MutList.toList(ml)
    }
```

### Regions are Values

A region (or region handle) is a _value_ that can be passed as a function
argument. This is useful, for example, when we want to write a reusable function
that allocates and returns a mutable data structure.

For example, here is the `List.toMutDeque` function:

```flix
def toMutDeque(rc: Region[r], l: List[a]): MutDeque[a, rc] \ rc =
    let d = new MutDeque(rc);
    forEach(x -> MutDeque.pushBack(x, d), l);
    d
```

The function takes a region handle `rc`, allocates a new mutable deque
(`MutDeq`) in the given region, inserts all elements of the list `l` in the
deque, and returns it. 

### Regions are Scoped

Regions and all memory associated with them cannot outline their lexical scope. 

Consider the following program:

```flix
def main(): Unit \ IO = 
    let escaped = region rc {
        Array#{1, 2, 3} @ rc
    };
    println(escaped)
```

Here we allocate the `Array#{1, 2, 3}` in the region `rc` and try to return it
outside of its enclosing scope. The Flix compiler detects such escape violations
and reports an error:

```
❌ -- Type Error ----------------------------

>> The region variable 'rc' escapes its scope.

2 |>     let escaped = region rc {
3 |>         Array#{1, 2, 3} @ rc
4 |>     };

region variable escapes.
```
