## Arrays

> **Note:** This documentation is relevant for Flix version 0.35.0 or higher.

Flix supports mutable _scoped_ arrays. An array is a fixed-length mutable
sequence of elements that share the same type. Arrays are laid out consecutively
in memory. Arrays are mutable; hence their elements can change over time.
However, once created, the length of an array cannot be changed.

In Flix, the type of an array is `Array[t, r]` where `t` is the type of its
elements and `r` is its region. Like all mutable memory in Flix, every array
must belong to some region. Reading from and writing to arrays are _effectful_
operations. For example, reading an element from an array of type `Array[t, r]`
has the effect `r`. Likewise, creating an array in a region is also an effectful
operation. 

Arrays are _always_ unboxed. For example, an array of type `Array[Int32, r]` is
represented as a sequence of primitive 32-bit integers, i.e., in JVM
terminology, the array is represented as `int[]`. Flix will never box primitive
integers as `java.lang.Integer` objects but still permits primitives in generic
collections and functions. The same is true for other types of primitives and
arrays of primitives. 

Arrays are low-level data structures typically used to implement higher-level
data structures. Therefore, unless implementing such data structures, we
recommend that arrays are used sparingly. Instead, we recommend using the
`MutList`, `MutDeque`, `MutSet`, and `MutMap` data structures.

> **Hint:** Use `MutList` if you need a _growable_ mutable sequence of elements.

### Array Literals

The syntax of an array literal is of the form `Array#{e1, e2, e3, ...} @ r`
where `e1`, `e2`, and so forth are _element expressions_, and `r` is the _region
expression_. For example:

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    println(fruits)
}
```

Here we introduce a region named `rc`. Inside the region, we create an array of
`fruits` that contain the three strings `"Apple"`, `"Pear"`, and `"Mango"`. The
type of `fruits` is `Array[String, rc]`. For more information about regions, we
refer to the chapter on [Regions](regions.md).

Running the program prints `Array#{"Apple", "Pear", "Mango"}`.

### Allocating Arrays

We can allocate an array of size `n` filled with the same element using the
`Array.repeat` function. For example: 

```flix
region rc {
    let arr = Array.repeat(rc, 1_000, 42);
    println(arr)
}
```

Here we create an array `arr` of length `1_000` where each array element has the
value `42`. Note that we must pass the region `rc` as an argument to
`Array.repeat` because the function must know to which region the returned array
should belong.

We can also create an array filled with all integers from zero to ninety-nine:

```flix
region rc {
    let arr = Array.range(rc, 0, 100);
    println(arr)
}
```

Moreover, we can convert most data structures to arrays. For example:

```flix
region rc {
    let fruitList = List#{"Apple", "Pear", "Mango"};
    let fruitArray = List.toArray(rc, fruitList);
}
```

Note that we must pass the region `rc` as an argument to `List.toArray` since
the function must know to which region the returned array should belong.

### Allocating Arrays with Uninitialized Elements

We can use the `Array.new` function to create an array of a given length where
the content of the array is uninitialized. For example:

```flix
region rc {
    let arr: Array[String, rc] = Array.new(rc, 100);
    // ... initialize `arr` here ...
}
```

Here we create an array of length `100` of type `Array[String, rc]`. We use an
explicit type annotation `: Array[String, rc]` to inform Flix of the expected
type of the array.

> **Warning:** It is dangerous to use arrays that have uninitialized elements. 

What are the elements of an uninitialized array? Flix follows Java (and the JVM)
which defines a _default value_ for every primitive-- and reference type. So,
for example, the default values for `Bool` and `Int32` are `false` and `0`,
respectively. The default value for reference types are `null`. So be careful!
Flix does not have a `null` value, but one can be indirectly introduced by
reading from improperly initialized arrays which can lead to
`NullPointerException`s. 

### Reading from and Writing to Arrays

We can retrieve or update the element at a specific position in an array using
`Array.get` and `Array.put`, respectively. For example: 

```flix
region rc {
    let strings = Array.new(rc, 2);
    Array.put("Hello", 0, strings);
    Array.put("World", 1, strings);
    let s1 = Array.get(0, strings);
    let s2 = Array.get(1, strings);
    println("${s1} ${s2}")
}
```

Here we create an empty array of length of two. We then store the string
`"Hello"` at position zero and the string `"World"` at position one. Next, we
retrieve the two strings, and print them. Thus the program, when compiled and
run, prints `Hello World`. 

We can also write part of the program in a more _fluent-style_ using the `!>`
pipeline operator: 

```flix
let strings = 
    Array.new(rc, 2) !>
    Array.put("Hello", 0) !>
    Array.put("World", 1);
```

### Slicing Arrays

We can slice arrays using `Array.slice`. A slice of an array is a new (shallow)
copy of a sub-range of the original array. For example

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    println(Array.slice(rc, 1, 2, fruits))
}
```

which prints `Array#{"Pear"}` when run.

### Taking the Length of an Array

We can compute the length of an array using the `Array.length` function. For
example

```flix
region rc {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rc;
    println(Array.length(fruits))
}
```

which prints `3` when run.

> **Note**: We advise against indexed-based iteration through arrays. Instead,
> we recommend to use functions such as `Array.count`, `Array.forEach`, and
> `Array.transform!`.

### Additional Array Operations

The `Array` module offers an extensive collection of functions for working with
arrays. For example, `Array.append`, `Array.copyOfRange`, `Array.findLeft`,
`Array.findRight`, `Array.sortWith!`, and `Array.sortBy!` to name a few. In
total, the module offers more than 100 functions ready for use.
