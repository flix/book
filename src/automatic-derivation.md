# Automatic Derivation

Flix supports the automatic derivation of several type classes.

## Derivation of Eq and Order

We can automatically derive instances of the `Eq` and `Order` type classes using
the `with` clause in the `enum` declaration. For example: 

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

## Derivation of ToString

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

```flix
A Circle(123), Square(123), and Rectangle(123, 456) walk into a bar.
```
