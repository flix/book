## Automatic Derivation

Flix supports automatic derivation of several type classes. For example:

- `Eq` — to derive structural equality on a type.
- `Order` — to derive a total ordering on a type.
- `ToString` — to derive a human-readable string representation on a type.
- `Sendable` — to enable a type to be sent over a channel.

### Derivation of Eq and Order

We can automatically derive instances of the `Eq` and `Order` type classes using
a `with` clause in the `enum` declaration. For example: 

```flix
enum Shape with Eq, Order {
    case Circle(Int32)
    case Square(Int32)
    case Rectangle(Int32, Int32)
}
```

The derived implementations are structural and rely on the order of the case
declarations:

```flix
def main(): Unit \ IO = 
    println(Circle(123) == Circle(123)); // prints `true`.
    println(Circle(123) != Square(123)); // prints `true`.
    println(Circle(123) <= Circle(123)); // prints `true`.
    println(Circle(456) <= Square(123))  // prints `true`.
```

> **Note**: Automatic derivation of `Eq` and `Order` requires that the types
> used inside the `enum` themselves implement `Eq` and `Order`.

### Derivation of ToString

We can also automatically derive `ToString` instances:

```flix
enum Shape with ToString {
    case Circle(Int32)
    case Square(Int32)
    case Rectangle(Int32, Int32)
}
```

Then we can take advantage of string interpolation and write:

```flix
def main(): Unit \ IO = 
    let c = Circle(123);
    let s = Square(123);
    let r = Rectangle(123, 456);
    println("A ${c}, ${s}, and ${r} walk into a bar.")
```

Which prints:

```
A Circle(123), Square(123), and Rectangle(123, 456) walk into a bar.
```

### Derivation of Sendable

We can also automatically derive implementations of the `Sendable` type class
(which allows values of a specific type to be sent over a channel). For example:

```flix
enum Shape with Sendable, ToString {
    case Circle(Int32)
}

def main(): Unit \ IO = 
    region rh {
        let (tx, rx) = Channel.buffered(rh, 10);
        Channel.send(Circle(123), tx); // OK, since Shape is Sendable.
        println(Channel.recv(rx))
    }
```

We _cannot_ derive `Sendable` for types that rely on scoped mutable memory. For
example, if we try:

```flix
enum Shape[r: Region] with Sendable {
    case Circle(Array[Int32, r])
}
```

We get a compilation error:

```
❌ -- Safety Error --------------------------------------

>> Cannot derive 'Sendable' for type Shape[b27587945]

Because it takes a type parameter of kind 'Region'.

1 | enum Shape[r: Region] with Sendable {
                               ^^^^^^^^
                               unable to derive Sendable.
```
