# For-Each

> **Note:** This feature is under development.

In Flix, as in other functional programming languages, most iteration is
expressed with recursion or combinators (e.g., `map` or `foldLeft`).

## For Each

The _for-each_ construct is useful for iterating over a collection
and apply some transformation to each element and works particularly
well with mutable collections.
This is due to the fact that the _for-each_ loop is actually just
syntactic sugar for a call to `Iterable.forEach` which has return
type `Unit`.
Thus, for the loop to be useful the body of the loop should have an effect.
However, before going any further an example is in order.

To use the _for-each_ loop an instance of `Iterable` on the collection is
required. For this example we will use a `MutList`.

```flix
def main(): Unit \ IO = 
    region rh {
        let l = new MutList(rh)
            !> MutList.push!(1)
            !> MutList.push!(2)
            !> MutList.push!(3);

        foreach (x <- l)
            println(x)
    }
```
