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

The key takeaway is that each trait instances gets to specify the associated
types. This is what allows us to add two strings or add an element to a set. 



<div style="color:gray;">


We can go even further. Mul example.

Another example: A trait for collections:

</div>