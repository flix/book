## Associated Effects

> **Warning:** Associated effects are an experimental feature. 

> **Warning:** Associated effects have not yet been released and are only
> available on nightly builds. 

We have seen how associated types increase the flexibility of traits by allowing
each instance to specify concrete types for the associated types. Associated
_effects_ work in the same manner, but concern effects. 

We motivate the need for associated effects with a simple example.

We can define a trait for types that can be divded:

```flix
trait Dividable[t] {
    pub def add(x: t, y: t): t
}
```

and we can implement the trait for e.g. `Float32` and `Int32`:

```flix
instance Dividable[Float32] {
    pub def add(x: Float32, y: Float32): Float32 = x / y
}

instance Dividable[Int32] {
    pub def add(x: Int32, y: Int32): Int32 = x / y
}
```

But what about division-by-zero? Assume we want to raise an exception and have
it tracked by the type and effect system. We would like to write:

```flix
pub eff DivByZero {
    pub def throw(): Void
}

instance Dividable[Int32] {
    pub def add(x: Int32, y: Int32): Int32 \ DivByZero = 
        if (y == 0) do DivByZero.throw() else x / y
}
````

But unfortunately this does not quite work:

```
❌ -- Type Error --------------------------------------------------

>> Mismatched signature 'add' required by 'Dividable'.

14 |     pub def add(x: Int32, y: Int32): Int32 \ DivByZero = 
                 ^^^
...
```

The problem, as the compiler explains, is that the definition of `div` in the
trait `Dividable` is declared as pure. Hence we are not allowed to raise an
exception. We could change the signature of `Dividable.div`, but that would be
problematic for the `Float32` instance, because division-by-zero returns `NaN`
and does not raise an exception. 

The solution is to use an associated effect: then the instance for `Int32` can
specify that a `DivByZero` exception may be raised whereas the instance for
`Float32` can be pure. We add an associated effect `Aef` to `Dividable`: 

```flix
trait Dividable[t] {
    type Aef: Eff
    pub def add(x: t, y: t): t \ Dividable.Aef[t]
}
```

and we re-implement the instances for `Float32` and `Int32`:

```flix
instance Dividable[Float32] {
    type Aef = { Pure } // No exception, div-by-zero yields NaN.
    pub def add(x: Float32, y: Float32): Float32 = x / y
}

instance Dividable[Int32] {
    type Aef = { DivByZero }
    pub def add(x: Int32, y: Int32): Int32 \ DivByZero = 
        if (y == 0) do DivByZero.throw() else x / y
}
```

### Associated Effects and Regions

