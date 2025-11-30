# Using Modules

As we have already seen, the `use` construct brings members of a module into local scope.

For example, given the program:

```flix
mod A {
    mod B {
        pub enum Color {
            case Red, Green, Blue
        }

        pub type alias Hue = Color 

        pub def isWarm(c: Color): Bool = 
            match c {
                case Color.Red    => true
                case Color.Green  => false
                case Color.Blue   => false
            }

    }
}
```

All of the following `use`s are meaningful:

```flix
use A.B.Color 
use A.B.Color.{Red, Green, Blue}
use A.B.Hue
use A.B.isWarm 
```

## All Kinds of Uses

Flix supports several kinds of uses, including:

- A qualified use of a name: `use A.B.Color`.
- A qualified use of multiple names: `use A.B.Color.{Red, Green, Blue}`.
- A qualified use with rename: `use A.B.Color => AColor`.
- A qualified use with multiple renames: `use A.B.Color.{Red => R, Green => G, Blue => B}`.

> **Note:** Flix does not support wildcard.

## Where can Uses Occur?

Flix supports uses in two places:

- Inside modules.
- Inside functions.

For example:

```flix
mod A {
    use Chain
    use Chain.Empty
    use Chain.Chain
    use Int32.max

    pub def maxValue(c: Chain[Int32]): Int32 = 
        match c {
            case Empty       => 0
            case One(x)      => x
            case Chain(x, y) => max(maxValue(x), maxValue(y))
        }
}
```

which can also be written as:

```flix
mod A {
    use Chain

    pub def maxValue(c: Chain[Int32]): Int32 = 
        use Chain.Empty;
        use Chain.Chain;
        use Int32.max;
        match c {
            case Empty       => 0
            case One(x)      => x
            case Chain(x, y) => max(maxValue(x), maxValue(y))
        }
}
```

Note the use of semicolons when inside an expression. 

## Default Uses

In Flix, a few built-in constructors are always in scope:

- `List.Nil` and `List.Cons`.
- `Result.Ok` and `Result.Err`.

