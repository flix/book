# Companion Modules

Inside a module we can declare an enum, struct, effect, or trait with the
same name as the module. Such a declaration is called the _companion_ of the
module.

For example:

```flix
mod Color {
    pub enum Color {
        case Red,
        case Green,
        case Blue
    }
}
```

Here the `Color` enum is the companion of the `Color` module.

The companion's name is exported from the module. This means that `Color` can
refer to both the module and the enum. We can refer to a case as `Color.Red`
or as `Color.Color.Red`.

The companion must appear before any other declaration inside its module.
Otherwise the compiler raises an error.

## Enum Companions

When an enum is declared as the companion of its module, the type and its
cases are automatically available throughout the module:

```flix
mod Color {
    pub enum Color {
        case Red,
        case Green,
        case Blue
    }

    pub def isWarm(c: Color): Bool = match c {
        case Red    => true
        case Green  => false
        case Blue   => false
    }
}
```

Here the `Color` type and the `Red`, `Green`, and `Blue` cases are in scope
within the companion `Color` module.

## Struct Companions

A struct may also be declared as the companion of its module. The fields of a
struct are only visible from within its companion module, so any function that
reads or writes them must live there.

For example:

```flix
mod Point {
    pub struct Point[r] {
        x: Int32,
        mut y: Int32
    }

    pub def area(p: Point[r]): Int32 \ r = p->x * p->y
}
```

Here `area` can access the `x` and `y` fields because it lives inside the
companion module of `Point`. See [Structs](structs.md) for more on field
visibility.

## Effect Companions

An effect may be declared as the companion of its module. The default handler
for the effect, if any, lives in the same companion module:

```flix
mod Fs.Glob {
    pub eff Glob {
        def glob(base: String, pattern: String): Result[IoError, List[String]]
    }

    // Handlers and helpers for the effect go here.
}
```

## Trait Companions

A trait may also be declared as the companion of its module. We typically use
the companion module to store functionality that is related to the trait:

```flix
mod Addable {
    pub trait Addable[t] {
        pub def add(x: t, y: t): t
    }

    pub def add3(x: t, y: t, z: t): t with Addable[t] = add(add(x, y), z)
}
```

When accessing a member of `Addable`, Flix automatically looks in both the
trait declaration and its companion module. Consequently, `Addable.add` refers
to the trait member `add` whereas `Addable.add3` refers to the function inside
the `Addable` module.

We should be aware that functions defined in the companion module of a trait
cannot be redefined by instances of the associated trait. Thus we should only
put members into the companion module when we do not intend to redefine them
later.

## Instances in Companion Modules

A trait instance may be declared in the companion module of its type. For
example, instances of `Add`, `Sub`, and `ToString` for the `Size` enum are
placed alongside the enum itself:

```flix
mod Fs.Size {
    pub enum Size(Int64) with Eq, Order, Hash

    instance Add[Size] {
        pub def add(x: Size, y: Size): Size =
            let Size(x1) = x;
            let Size(y1) = y;
            Size(x1 + y1)
    }

    pub def zero(): Size = Size(0i64)
}
```

This is the recommended location for instances when the trait is defined
elsewhere.
