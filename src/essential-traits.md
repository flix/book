# Essential Traits

Practical programming in Flix requires knowledge of at least three traits: `Eq`,
`Order`, and `ToString`. 

## The Eq Trait

The `Eq` trait captures when two values of a specific type are equal:

```flix
trait Eq[a] {

    ///
    /// Returns `true` if and only if `x` is equal to `y`.
    ///
    pub def eq(x: a, y: a): Bool

    // ... additional members omitted ...
}
```

To implement `Eq`, we only have to implement the `eq` function. When we
implement `eq` we automatically get an implementation of `Eq.neq`.

## The Order Trait

The `Order` trait captures when one value is smaller or equal to another value
of the same type:

```flix
trait Order[a] with Eq[a] {

    ///
    /// Returns `Comparison.LessThan` if `x` < `y`, 
    /// `Equal` if `x` == `y` or 
    /// `Comparison.GreaterThan` if `x` > `y`.
    ///
    pub def compare(x: a, y: a): Comparison

    // ... additional members omitted ...
}
```

To implement the `Order` trait, we must implement the `compare` function which
returns value of type `Comparison`. The `Comparison` data type is defined as:

```flix
enum Comparison {
    case LessThan
    case EqualTo
    case GreaterThan
}
```

When we implement `compare`, we automatically get implementations of
`Order.less`, `Order.lessThan`, `Order.greater`, `Order.greaterEqual`,
`Order.max`, and `Order.min`.

## The ToString Trait

The `ToString` trait is used to obtain a string representation of a specific value:

```flix
trait ToString[a] {
    ///
    /// Returns a string representation of the given `x`.
    ///
    pub def toString(x: a): String
}
```

Flix uses the `ToString` trait in string interpolations. 

For example, the interpolated string

```flix
"Good morning ${name}, it is ${hour} o'clock."
```

is actually syntactic sugar for the expression:

```flix
"Good morning " + ToString.toString(name) + ", it is " 
                + ToString.toString(hour) + " o'clock."
```

In the following subsection, we discuss how to automatically derive
implementations of the `Eq`, `Order`, and `ToString` traits.
