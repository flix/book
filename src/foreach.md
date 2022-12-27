# For-Each

> **Note:** This feature is experimental and not yet intended for use.

In Flix, as in other functional programming languages, most iteration is
expressed with recursion or combinators (e.g., `map` or `foldLeft`).

That said, Flix has syntactic sugar for two common types of loops: _for-each_ and _for yield_.

## For Each

The _for-each_ construct is useful for iterating over a collection
and apply some transformation to each element and works particularly
well with mutable collections.
This is due to the fact that the _for-each_ loop is actually just
syntactic sugar for a call to `Iterable.foreach` which has return
type `Unit`.
Thus, for the loop to be useful the body of the loop should have an effect.
However, before going any further an example is in order.

To use the _for-each_ loop an instance of `Iterable` on the collection is required.
For this example we will use a `MutList`.

```flix
def main(): Unit & Impure = region r {
    use MutList.push!;

    let l = new MutList(r)
        !> push!(1)
        !> push!(2)
        !> push!(3);

    foreach (x <- l)
        println(x)
}
```
