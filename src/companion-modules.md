# Companion Modules

In Flix every enum and type class declaration is associated with a _companion
module_.

## Enum Companions

When we declare an enum, its type and cases are automatically available inside
its companion module. For example, we can write:

```flix
enum Color {
    case Red,
    case Green,
    case Blue
}

mod Color {
    pub def isWarm(c: Color): Bool = match c {
        case Red    => true
        case Green  => false
        case Blue   => false
    }
}
```

Here the `Color` type and the `Red`, `Green`, and `Blue` cases are automatically
in scope within the companion `Color` module. 

