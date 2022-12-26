# Arrays

> **Note:** This feature requires Flix version 0.35.0 or higher.

Flix supports _mutable_ arrays. In Flix, like in most languages, an array is a
sequence of elements that share the same type and are laid out consecutively in
memory. Flix arrays are mutable; hence you can change the elements of an array
during its lifetime. 

In Flix, the type of an array is `Array[t, r]` where `t` is the type of its
elements and `r` is its regions. In other words, like all mutable memory, every
array belongs to some region.

Reading and writing from/to arrays are _effectful_ operations. For example,
reading an element from an array of type `Array[t, r]` has the `r` effect.
Likewise, creating an array in a region is also an effectful operation. 

Arrays are _always_ unboxed. For example, at run-time an array of type
`Array[Int32, r]` is represented as a sequence of primitive 32-bit integers. The
integers are _not_ converted to `java.lang.Integer` objects. The same is true
for other types of primitive arrays. 

Arrays are a low-level mutable data structure typically used to implement
higher-level data structures. Therefore, we recommend you not use arrays
directly in your code. Instead, we recommend using immutable data structures or
high-level mutable data structures such as `MutList`, `MutDeque`, `MutSet`, or
`MutMap`. 



## Array Literals

Flix supports  `Array#{e1, e2, e3, ...} @ r` where `e1`, `e2`, and so
forth are expressions. 

```flix
[1, 2, 3, 4]
```

evaluates to an array with the four elements:
`1, 2, 3, 4`.

In some cases it is useful to allocate a large array
filled with the same value.
The expression:

```flix
["Hello World"; 100]
```

evaluates to an array of length 100 where every entry
contains the string `"Hello World"`.

> **Design Note**
>
> Flix does not allow the allocation of an array
> without assigning a "default value" to each entry in
> the array.

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

## Array Slicing

Arrays can be sliced.
Slicing an array (shallowly) copies a subrange of the
array.
For example:

```flix
let a = [1, 2, 3, 4, 5];
a[2..4]
```

evaluates to the array `[3, 4]`.

The start or end index may be omitted.
For example:

```flix
let a = [1, 2, 3, 4, 5];
let a1 = a[2..]; // evaluates to [3, 4, 5]
let a2 = a[..4]  // evaluates to [1, 2, 3, 4]
```

If both the start and end index are omitted the
entire array is copied.
For example:

```flix
let a = [1, 2, 3, 4, 5];
a[..]
```

evaluates to the (copied) array `[1, 2, 3, 4, 5]`.

> **Design Note**
>
> Slicing an array using the same start and end index
> returns the empty array.
> For example, `[0, 1, 2, 3][2..2]` evaluates to `[]`.

> **Warning**
>
> Slicing with negative indices is undefined and
> results in runtime errors.
<!---
## Array Length

The length of an array is accessed as follows

```flix
let a = [1, 2, 3, 4, 5];
a.length
```

which evaluates to `5`.

-->
