## References

Flix supports mutable _scoped_ references. A reference is a box whose value can
change over time. The three key reference operations are:

- Creating a new reference `Ref.fresh(rc, e)`.
- Dereferencing a reference `Ref.get(e)`.
- Assigning to a reference `Ref.put(e, e)`.

In Flix, the type of a reference is `Ref[t, r]` where `t` is the type of the
element and `r` is its region. Like all mutable memory in Flix, every reference
must belong to some region. Reading from and writing to a reference are
_effectful_ operations. For example, reading the value of a reference `Ref[t, r]`
has effect `r`.

The `Ref.fresh(rc, e)` operation allocates a reference cell in a region of the heap
and returns its location, the `Ref.get` operation dereferences a location and
returns the content of a reference cell, and the assignment `Ref.put` operation
changes the value of a reference cell. Informally, a reference cell can be
thought of as an "object" with a single field that can be changed.

### Allocating References

A reference cell is allocated with the `Ref.fresh(rc, e)` function. For example:

```flix
region rc {
    let c = Ref.fresh(rc, 42);
    println(Ref.get(c))
}
```

Here we introduce a region named `rc`. Inside the region, we create a reference
cell called `c` with the value `42` which we then dereference and print.

### Dereferencing References

A reference cell is accessed (dereferenced) with the `Ref.get` function. For example:

```flix
region rc {
    let c = Ref.fresh(rc, 42);
    let x = Ref.get(c);
    let y = Ref.get(c);
    println(x + y)
}
```

Here the program prints `42 + 42 = 84`.

### Assignment

We can update the value of a reference cell. For example:

```flix
region rc {
    let c = Ref.fresh(rc, 0);
    Ref.put(Ref.get(c) + 1, c);
    Ref.put(Ref.get(c) + 1, c);
    Ref.put(Ref.get(c) + 1, c);
    println(Ref.get(c))
}
```

Here the program creates a reference cell `c` with the value `0`. We dereference
the cell and increment its value three times. Hence the program prints `3`.

### Example: A Simple Counter

We can use references to implement a simple counter:

```flix
enum Counter[r: Region] { // The Region here is a type-kind
    case Counter(Ref[Int32, r])
}

def newCounter(rc: Region[r]): Counter[r] \ r = Counter.Counter(Ref.fresh(rc, 0))

def getCount(c: Counter[r]): Int32 \ r =
    let Counter.Counter(l) = c;
    Ref.get(l)

def increment(c: Counter[r]): Unit \ r =
    let Counter.Counter(l) = c;
    Ref.put(Ref.get(l) + 1, l)

def main(): Unit \ IO =
    region rc {
        let c = newCounter(rc);
        increment(c);
        increment(c);
        increment(c);
        getCount(c) |> println
    }
```

Here the `Counter` data type has a region type parameter. This is required since
the counter internally uses a reference that requires a region. Hence `Counter`s
are also scoped. Note that the `newCounter` function requires a region handle to
create a new `Counter`. Moreover, note that the functions `getCount` and
`increment` both have the `r` effect.

### Aliasing and References to References

References naturally support aliasing since that is their purpose. For example:

```flix
region rc {
    let l1 = Ref.fresh(rc, 42);
    let l2 = l1;
    Ref.put(84, l2);
    println(Ref.get(l1))
}
```

Prints `84` because the reference cell that `l1` points to is modified through
the alias `l2`.

References can also point to references as the following example illustrates:

```flix
region rc {
    let l1 = Ref.fresh(rc, 42);
    let l2 = Ref.fresh(rc, l1);
    let rs = Ref.get(Ref.get(l2));
    println(rs)
}
```

Here the type of `l2` is `Ref[Ref[Int32, rc], rc]`.

### Mutable Tuples and Records

Flix tuples and records are _immutable_. However, tuples and records may contain
mutable references.

For example, here is a pair that contains two mutable references:

```flix
region rc {
    let p = (Ref.fresh(rc, 1), Ref.fresh(rc, 2));
    Ref.put(123, fst(p))
};
```

The type of the pair is `(Ref[Int32, rc], Ref[Int32, rc])`. The assignment does
not change the pair but instead changes the value of the reference cell in the
first component.

Similarly, here is a record that contains two mutable references:

```flix
region rc {
    let r = { fstName = Ref.fresh(rc, "Lucky"), lstName = Ref.fresh(rc, "Luke") };
    Ref.put("Unlucky", r#fstName)
};
```

The type of the record is `{ fstName = Ref[String, rc], lstName = Ref[String, rc] }`.
Again, the assignment does not change the record, but instead changes
the value of the reference cell corresponding to the `fstName` label.
