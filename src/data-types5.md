# Recursive Types

Recursive types are used to define types that are
self-referential.

For example, we can define a binary tree of integers
as follows:

```flix
enum Tree {
    case Leaf(Int32),
    case Node(Tree, Tree)
}
```

A tree is either a `Leaf` with an `Int32` value or an
internal `Node` with a left and a right sub-tree.
Note that the definition of `Tree` refers to itself.

We can write a function, using pattern matching, to
compute the sum of all integers in such a tree:

```flix
def sum(t: Tree): Int32 = match t {
    case Leaf(x)    => x
    case Node(l, r) => sum(l) + sum(r)
}
```

The `sum` function pattern matches on a tree value.
If the tree is a leaf its value is simply returned.
Otherwise the function recurses on both subtrees and
adds their results.
