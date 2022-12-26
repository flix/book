# Arrays

> **Note:** This feature requires Flix version 0.35.0 or higher.

Flix supports _mutable_ arrays. In Flix, like in most languages, an array is a
sequence of elements that share the same type and are laid out consecutively in
memory. Arrays are mutable; hence you can change the elements of an array during
its lifetime. However, the length of an array is fixed at its creation. 

In Flix, the type of an array is `Array[t, r]` where `t` is the type of its
elements and `r` is its region. In other words, like all mutable memory, every
array belongs to some region. Reading from and writing to arrays are _effectful_
operations. For example, reading an element from an array of type `Array[t, r]`
has the effect `r`. Likewise, creating an array in a region is also an effectful
operation. 

Arrays are _always_ unboxed. For example, at run-time an array of type
`Array[Int32, r]` is represented as a sequence of primitive 32-bit integers. On
the JVM, this array is represented as the Java type `int[]`. Moreover, these
integers are never converted to `java.lang.Integer` objects. The same is true
for other types of primitive arrays. 

Arrays are a low-level mutable data structure typically used to implement
higher-level data structures. Therefore, we recommend you not use arrays
directly in your code. Instead, we recommend using immutable data structures or
high-level mutable data structures such as `MutList`, `MutDeque`, `MutSet`, or
`MutMap`. 

While Flix has special syntax for array literals, all other operations on arrays
are available as ordinary functions in the `Array` module. 

## Array Literals

The syntax of an array literal is of the form `Array#{e1, e2, e3, ...} @ r`
where `e1`, `e2`, and so forth are _element_ expressions, and `r` is the region
expression. For example:

```flix
region rh {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rh;
    println(fruits)
}
```

Here we introduce a region named `rh` inside of which we create an array of
`fruits` that contain the three strings `"Apple"`, `"Pear"`, and `"Mango"`. The
local variable `fruits` has type `Array[String, rh]` and belong to the region
`rh`. For more information about regions, we refer to the chapter on
[Regions](regions.md).

If we compile and run the program, it prints `Array#{"Apple", "Pear", "Mango"}`.

## Allocating Arrays

We can allocate an array of size `n` filled with the same element using the
`Array.repeat` function. For example: 

```flix
region rh {
    let arr = Array.repeat(rh, 1_000, 42);
    println(arr)
}
```

Here we create an array `arr` of length `1_000` where each array element has the
value `42`. Note that we must pass the region `rh` as an argument to
`Array.repeat` because the function must know to which region the returned array
belongs.

We can also create an array filled with all integers from zero to ninety-nine:

```flix
region rh {
    let arr = Array.range(rh, 0, 100);
    println(arr)
}
```

And finally, we can often convert other data structures into mutable arrays.
Most immutable data structures, including `List`, `Chain`, `Nec`, have a
`toArray` function. Here is an example:

```flix
region rh {
    let fruitList = List#{"Apple", "Pear", "Mango"};
    let fruitArray = List.toArray(rh, fruitList);
}
```

Note that we must pass the region `rh` as an argument to `List.toArray` because
the function must know to which region the returned array belongs.

## Allocating Arrays with Uninitialized Values

We can use the `Array.new` function when we want to create an array of a
specific length where its elements are uninitialized. For example:

```flix
region rh {
    let arr: Array[String, rh] = Array.new(rh, 100);
    // ... initialize `arr` here ...
}
```

Here we create a new array of length `100` of type `Array[String, rh]`. Note
that we have used an explicit type annotation since there is nothing in the
program to inform Flix of the array type. 

> **Warning:** It is dangerous to use arrays that have uninitialized values. 

But what are the elements of an uninitialized array? Here Flix follows Java which
defines a _default value_ for every primitive type and reference type. So, for
example, the default values for `Bool` and `Int32` are `false` and `0`,
respectively. The default value for reference types are `null`. So be careful!
Even though Flix does not have a `null` value, one can indirectly be introduced
via uninitialized arrays leading to `NullPointerException`s. 

<!---

## Reading and Writing from Arrays

Arrays can be accessed and updated using standard
syntax.
For example:

```flix
let a = [0; 10];
a[0] = 21;
a[1] = 42;
a[0] + a[1]
```

evaluates to `63`, as expected.

-->

## Array Slicing

We can slice arrays using `Array.slice`. A slice of an array is a new (shallow)
copy of a sub-range of the original array. For example:

```flix
region rh {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rh;
    println(Array.slice(rh, 1, 2, fruits))
}
```

Here the program prints `Array#{"Pear"}` when compiled and run.

## Array Length

We can compute the length of an array using the `Array.length` function. For
example: 

```flix
region rh {
    let fruits = Array#{"Apple", "Pear", "Mango"} @ rh;
    println(Array.length(fruits))
}
```

This program prints `3` when compiled and run. 

> **Note**: We advise against indexed-based iteration through arrays. Instead,
> we recommend to use functions such as `Array.count`, `Array.forEach`, and
> `Array.transform!`.

## Other Array Operations

The `Array` module offers an extensive collection of functions for working with
arrays. For example, `Array.append`, `Array.copyOfRange`, `Array.findLeft`,
`Array.findRight`, `Array.sortWith!`, and `Array.sortBy!` to name a few of the
more than 100 functions. 
