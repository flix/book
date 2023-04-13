## Companion Modules

In Flix every enum and type class declaration is associated with a _companion
module_.

### Enum Companions

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

### Type Class Companions

Every type class declaration also gives rise to a companion module.

For example, we can define a type class `Addable` for types whose elements can be added:

```flix
class Addable[t] {
    pub def add(x: t, y: t): t
}
```

The `Addable` type class implicitly introduces a companion module `Addable`. We
typically use the companion module to store functionality that is related to the
type class. 

For example, we could have:

```flix
mod Addable {
    pub def add3(x: t, y: t, z: t): t with Addable[t] = add(add(x, y), z)
}
```

When accessing a member of `Addable`, Flix will automatically look in both the
class declaration and its companion namespace. Consequently, `Addable.add`
refers to the type class member `add` whereas `Addable.add3` refers to the
function inside the `Addable` module. Note that the `add` signature is in the
scope of the `Addable` module. 

We should be aware that functions defined in the companion module of a type
class cannot be overridden by instances of the associated type class. Thus we
should only put members into the companion namespace when we do not intend
to override them later. 
