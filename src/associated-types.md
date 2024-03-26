## Associated Types

> **Warning:** Associated types are an experimental feature. 

> **Warning:** Associated types have not yet been released and are only
> available on nightly builds. 

An associated type is a type member of a trait that is specified by each trait
instance. Associated types are a more natural alternative to multi-parameter
type classes. 

We illustrate associated types with an example. 

We can define a trait for types that can be added:

```flix
trait Addable[t] {
    pub def add(x: t, y: t): t
}
```

We can define multiple instances of the `Addable` trait for types such as
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

The `Addable` trait now has an associated type called `Rhs`. We can refer to it
as `Addable.Rhs[t]` as seen in the signature of `Add`. Whenever we declare an
instance of `Addable`, we must specify the associated effect. 

We can still implement instances for integers and strings, as before. For example:

```flix
instance Addable[Int32] {
    type Rhs = Int32
    pub def add(x: Int32, y: Int32): Int32 = x + y
}
```

But we can now also implement an instance that allows adding an element to a
set: 

```flix
instance Addable[Set[a]] with Order[a] {
    type Rhs = a
    pub def add(s: Set[a], x: a): Set[a] = Set.insert(x, s)
}
```

The important point is that each trait instance can specify the associated type. 

We might wonder if we can specify two instances for `Set[a]`: (i) one for adding
an element to a set, as above, and (ii) one for adding two sets:

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

### Example: A `ForEach` Trait

We can use associated types to define a trait for collections that have a
`forEach` function: 

```flix
trait ForEach[t] {
    type Elm
    pub def forEach(f: ForEach.Elm[t] -> Unit \ ef, x: t): Unit \ ef
}
```

Here `t` is type of the collection and the associated type `Elm` is the type of
its elements. We can implement several instances for `ForEach`. For example, we
can implement an instance for `List[a]`:

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
key-value pairs. Note: We need extra parentheses around the argument to `f`
because we want it to take a pair. 

We can even define an instance for `String` where we can iterate through each
individual character: 

```flix
instance ForEach[String] {
    type Elm = Char
    pub def forEach(f: Char -> Unit \ ef, x: String): Unit \ ef = 
        x |> String.toList |> List.forEach(f)
}
```

### Example: A `Collection` Trait




<div style="color:gray;">


We can go even further. Mul example.

Another example: A trait for collections:

</div>