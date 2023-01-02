# Mutable Collections

The Flix standard library supports many immutable collections, including
options, lists, chains, sets, and maps. We strongly encourage their use.

In addition, the Flix standard library also offers several mutable collections:

- `MutList[t, r]`      : a contiguous growable/shrinkable array of elements of type `t`.
- `MutSet[t, r]`       : a mutable set of elements of type `t`.
- `MutMap[k, v, r]`    : a mutable map of keys of type `k` to values of type `v`.
- `MutDeque[t, r]`     : a mutable double-ended queue of elements of type `t`.

Recall that in Flix all mutable memory, which includes mutable collections,
belong to a region.

Here is a simple example of how to use `MutList[t]`:

```flix
def main(): Unit \ IO = 
    region rh {
        let fruits = MutList.new(rh);
        MutList.push!("Apple", fruits);
        MutList.push!("Pear", fruits);
        MutList.push!("Mango", fruits);
        MutList.forEach(println, fruits)
    }
```

which prints `Apple`, `Pear`, and `Mango`. Here the `MutList[String, rh]`
automatically expands (and shrinks) as elements are pushed (or popped) from it. 

We can write the program in a more _fluent-style_ using the `!>` pipeline
operator:

```flix
def main(): Unit \ IO = 
    region rh {
        let fruits = 
            MutList.new(rh) !> 
            MutList.push!("Apple") !> 
            MutList.push!("Pear") !>
            MutList.push!("Mango");
        MutList.forEach(println, fruits)
    }
```

