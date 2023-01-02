# Mutable Collections

The Flix standard library supports many immutable collections, including
options, lists, chains, sets, and maps. We strongly encourage their use.

In addition, the Flix standard library also offers several mutable collections:

- `MutList[t, r]`      : a contiguous growable/shrinkable array of elements of type `t`.
- `MutSet[t, r]`       : a mutable set of elements of type `t`.
- `MutMap[k, v, r]`    : a mutable map of keys of type `k` to values of type `v`.
- `MutDeque[t, r]`     : a mutable double-ended queue of elements of type `t`.

Recall that in Flix all mutable memory, including mutable collections, belongs
to a region.

Here is an example of how to use `MutList[t]`:

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

We can write the above program in a more _fluent-style_ using the `!>` pipeline
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

We can split the above program into several functions as follows:

```flix
def main(): Unit \ IO = 
    region rh {
        let fruits = sweetFruits(rh);
        printFruits(fruits)
    }

def sweetFruits(rh: Region[r]): MutList[String, r] \ r = 
    MutList.new(rh) !> 
    MutList.push!("Apple") !> 
    MutList.push!("Pear") !>
    MutList.push!("Mango")

def printFruits(fruits: MutList[String, r]): Unit \ {r, IO} = 
    MutList.forEach(println, fruits)
```

Here the `main` function introduces a new region `rh`. We pass this region to
`sweetFruits` which creates and returns a new mutable list of fruits. Note that
`sweetFruits` has the effect `r` since it allocates mutable memory using `rh`.
The `printFruits` takes a mutable list of fruits and prints them. Note that this
function has effect `r` since it reads from mutable memory in `r` and it has
effect `IO` since it prints to the terminal. 
