## Associated Types

> **Warning:** Associated types are an experimental feature. 

> **Warning:** Associated types have not yet been released and are only
> available on nightly builds. 

An associated type is a type member of a trait that is specified by each trait
instance. Associated types are often considered a more natural alternative to
[multi-parameter type classes](https://en.wikipedia.org/wiki/Type_class#Multi-parameter_type_classes). 

We illustrate associated types with an example. 

We can define a trait for types that can be added:

```flix
trait Addable[t] {
    pub def add(x: t, y: t): t
}
```

We can implement multiple instances of the `Addable` trait for types such as
floating-point numbers, integers, and strings. For example, here is the instance
for `Int32`:

```flix
instance Addable[Int32] {
    pub def add(x: Int32, y: Int32): Int32 = x + y
}
```

and here is one for `String`:

```flix
instance Addable[String] {
    pub def add(x: String, y: String): String = "${x}${y}"
}
```

But what if we wanted to add an element to a set?

Intuitively, we would like to write:

```flix
instance Addable[Set[a]] with Order[a] {
    pub def add(s: Set[a], x: a): Set[a] = Set.insert(x, s)
}
```

But the signature of `add` does not match the signature declared in `Addable`.

We can overcome this problem and increase the flexibility of `Addable` with an
associated type: 

```flix
trait Addable[t] {
    type Rhs
    pub def add(x: t, y: Addable.Rhs[t]): t
}
```

The `Addable` trait now has an associated type called `Rhs`. We refer to it as
`Addable.Rhs[t]` as seen in the signature of `add`. Whenever we declare an
instance of `Addable`, we must specify the associated type. 

We can still implement instances for integers and strings, as before. For
example:

```flix
instance Addable[Int32] {
    type Rhs = Int32
    pub def add(x: Int32, y: Int32): Int32 = x + y
}
```

But we can also implement an instance that allows adding an element to a set: 

```flix
instance Addable[Set[a]] with Order[a] {
    type Rhs = a
    pub def add(s: Set[a], x: a): Set[a] = Set.insert(x, s)
}
```

The important point is that _each trait instance specifies the associated type_.

We might wonder if we can specify two instances for `Set[a]`: (a) one for adding
an element to a set, as above, and (b) one for adding two sets:

```flix
instance Addable[Set[a]] with Order[a] {
    type Rhs = Set[a]
    pub def add(x: Set[a], y: Set[a]): Set[a] = Set.union(x, y)

}
```

But while each instance is valid on its own, we cannot have both:

```
❌ -- Instance Error -------------------------------------------------- 

>> Overlapping instances for 'Addable'.

...
```

If we had such overlapping instances, an expression like `Addable.add(Set#{},
Set#{})` would become ambiguous: Are we adding two sets? Or are we adding the
empty set to a set? 

### Example: A `ForEach` Trait

We can use associated types to define a trait for collections that have a
`forEach` function: 

```flix
trait ForEach[t] {
    type Elm
    pub def forEach(f: ForEach.Elm[t] -> Unit \ ef, x: t): Unit \ ef
}
```

Here `t` is the type of the collection and the associated type `Elm` is the type
of its elements. We can implement several instances for `ForEach`. For example,
we can implement an instance for `List[a]`:

```flix
instance ForEach[List[a]] {
    type Elm = a
    pub def forEach(f: a -> Unit \ ef, x: List[a]): Unit \ ef = List.forEach(f, x)
}
```

We can also implement an instance for `Map[k, v]`:

```flix
instance ForEach[Map[k, v]] {
    type Elm = (k, v)
    pub def forEach(f: ((k, v)) -> Unit \ ef, x: Map[k, v]): Unit \ ef = 
        Map.forEach(k -> v -> f((k, v)), x)
}
```

What is interesting and useful is that we can define the element type to be
key-value pairs. We need extra parentheses around the argument to `f` because we
want it to take a pair. 

We can implement an instance for `String` where we can iterate through each
individual character: 

```flix
instance ForEach[String] {
    type Elm = Char
    pub def forEach(f: Char -> Unit \ ef, x: String): Unit \ ef = 
        x |> String.toList |> List.forEach(f)
}
```

### Example: A `Collection` Trait

As another example, we can define a trait for collections:

```flix
trait Collection[t] {
    type Elm
    pub def empty(): t
    pub def insert(x: Collection.Elm[t], c: t): t
    pub def toList(c: t): List[Collection.Elm[t]]
}
```

Here `t` is the type of the collection and `Elm` is the type of its elements.
Every collection must support three operations: `empty`, `insert`, and `toList`. 

We can implement an instance of `Collection` for `Vector[a]`: 

```flix
instance Collection[Vector[a]] {
    type Elm = a
    pub def empty(): Vector[a] = Vector.empty()
    pub def insert(x: a, c: Vector[a]): Vector[a] = Vector.append(c, Vector#{x})
    pub def toList(c: Vector[a]): List[a] = Vector.toList(c)
}
```

And we can implement an instance of `Collection` for `Set[a]`: 

```flix
instance Collection[Set[a]] with Order[a] {
    type Elm = a
    pub def empty(): Set[a] = Set.empty()
    pub def insert(x: a, c: Set[a]): Set[a] = Set.insert(x, c)
    pub def toList(c: Set[a]): List[a] = Set.toList(c)
}
```

### Equality Constraints

We sometimes want to write polymorphic functions where we _restrict_ an
associated type. 

For example, returning to the example of the `Collection` trait, we can write a
function where we require that the element type is an `Int32`. This allows us to
write a sum function:

```flix
def sum(c: t): Int32 with Collection[t] where Collection.Elm[t] ~ Int32 = 
    Collection.toList(c) |> List.sum
```

Here the `where` clause contains a list of _type equality constraints_.
Specifically, the equality constraint `Collection.Elm[t] ~ Int32` assert that
`sum` can be used with any type `t` for which there is an instance of
`Collection` as long as the element type of that instance is equal to `Int32`.
This restriction ensures that the elements of the collection are integers and
allows us to call `List.sum`.

### Default Types

We can define a default type for an associated type.

Returning to `Addable`, we can define the associated type `Rhs` with `t` as its
default:

```flix
trait Addable[t] {
    type Rhs = t  // Associated type with default type.
    pub def add(x: t, y: Addable.Rhs[t]): t
}
```

Here we specify that if `Rhs` is not defined by an instance implementation then
it defaults to `t`. The upshot is that we can define an instance for `Int32`:

```flix
instance Addable[Int32] {
    pub def add(x: Int32, y: Int32): Int32 = x + y
}
```

without having to explicit define `type Rhs = Int32`.
