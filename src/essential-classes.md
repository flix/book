# Essential Classes

As a Flix programmer, there are three important type classes you are likely to
run into quickly: `Eq`, `Order`, and `ToString`. 

### Eq

The `Eq` type class captures when two values of a type are equal:

```flix
pub lawful class Eq[a] {

    pub def eq(x: a, y: a): Bool

    // ... additional members omitted ...
}
```

### Order

The `Order` type class captures when one value is smaller or equal to another value:

```flix
pub lawful class Order[a] with Eq[a] {

    ///
    /// Returns `Comparison.LessThan` if `x` < `y`, 
    /// `Equal` if `x` == `y` or 
    /// `Comparison.GreaterThan` `if `x` > `y`.
    ///
    pub def compare(x: a, y: a): Comparison

    // ... additional members omitted ...
}
```

Here the `Comparison` data type is defined as:

```flix
pub enum Comparison {
    case LessThan
    case EqualTo
    case GreaterThan
}
```

### ToString

The `ToString` type class allows us to obtain a human-readable string
representation of a value:

```flix
pub class ToString[a] {
    ///
    /// Returns a string representation of the given x.
    ///
    pub def toString(x: a): String
}
```

Flix uses the `ToString` type class in string interpolations. 

For example, the interpolated string

```flix
"Good morning ${name}, it is ${hour} a clock."
```

is syntactic sugar for the expression:

```flix
"Good morning " + ToString.toString(name) + ", it is " 
                + ToString.toString(hour) + " a clock."
```

In the following subsection, we discuss how implementations of the `Eq`,
`Order`, and `ToString` type classes can be automatically derived. 