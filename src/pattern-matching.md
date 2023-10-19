## Pattern Matching

### Matching on Enums

Flix supports pattern matching on algebraic data types.

For example, if we have an algebraic data type that models shapes:

```flix
enum Shape {
    case Circle(Int32)
    case Square(Int32)
    case Rectangle(Int32, Int32)
}
```

Then we can write a function to compute the area of a `Shape` using pattern
matching:

```flix
def area(s: Shape): Int32 = match s {
    case Shape.Circle(r)       => 3 * (r * r)
    case Shape.Square(w)       => w * w
    case Shape.Rectangle(h, w) => h * w
}
```

This also works for record types, however, the syntax is slightly different.
Let us rewrite the `Shape` type from before using records.

```flix
enum Shape {
    case Circle({ radius = Int32 })
    case Square({ width = Int32 })
    case Rectangle({ height = Int32, width = Int32 })
}

def area(s: Shape): Int32 = match s {
    case Shape.Circle({ radius })           => 3 * (radius * radius)
    case Shape.Square({ width })            => width * width
    case Shape.Rectangle({ height, width }) => height * width
}
```

In general, the syntax for record patterns are similar to their types:

TODO: Write this out properly

```
{ }            // The empty record
{ radius }     // A record containing ONLY the field `radius`
{ radius | _ } // A record containg at least the field `radius`
{ radius | r } // A record containg at least the field `radius` where the rest of the record is bound to `r`
{ radius = r } // A record containg at least the field `radius` where the value is bound to `r` in the scope
// { radius } is actually syntactic sugar for { radius = radius }
```

### Let Pattern Match

In addition to the pattern `match` construct, a let-binding can be used to
destruct a value. For example:

```flix
let (x, y, z) = (1, 2, 3)
```

Binds the variables `x`, `y`, and `z` to the values `1`, `2`, and `3`,
respectively.

Any exhaustive pattern may be used in a let-binding. For example:

```flix
let (x, Foo(y, z)) = (1, Foo(2, 3))
```

is legal provided that the `Foo` constructor belongs to a type where it is the
only constructor.

The following let-bindings are *illegal* because they are not exhaustive:

```flix
let (1, 2, z) = ...
let Some(x) = ...
```

The Flix compiler will reject such non-exhaustive patterns.

### Match Lambdas

Pattern matches can also be used with lambda expressions. For example:

```flix
List.map(match (x, y) -> x + y, (1, 1) :: (2, 2) :: Nil)
```

is equivalent to:

```flix
List.map(w -> match w { case (x, y) => x + y }, (1, 1) :: (2, 2) :: Nil)
```

As for let-bindings, such pattern matches must be exhaustive.

Note the difference between the two lambda expressions:

```flix
let f = (x, y, z) -> x + y + z + 42i32
let g = match (x, y, z) -> x + y + z + 42i32
```

Here `f` is a function that expects *three* `Int32` arguments, whereas `g` is a
function that expects *one* three tuple `(Int32, Int32, Int32)` argument.
