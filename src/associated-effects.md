## Associated Effects

We have seen how associated types increase the flexibility of traits by allowing
each instance to specify concrete types for the associated types. Associated
_effects_ work in the same manner, but concern effects. 

We motivate the need for associated effects with a simple example.

We can define a trait for types that can be divded:

```flix
trait Dividable[t] {
    pub def div(x: t, y: t): t
}
```

and we can implement the trait for e.g. `Float32` and `Int32`:

```flix
instance Dividable[Float32] {
    pub def div(x: Float32, y: Float32): Float32 = x / y
}

instance Dividable[Int32] {
    pub def div(x: Int32, y: Int32): Int32 = x / y
}
```

But what about division-by-zero? Assume we want to raise an exception and have
it tracked by the type and effect system. We would like to write:

```flix
pub eff DivByZero {
    pub def throw(): Void
}

instance Dividable[Int32] {
    pub def div(x: Int32, y: Int32): Int32 \ DivByZero = 
        if (y == 0) DivByZero.throw() else x / y
}
````

But unfortunately this does not quite work:

```
❌ -- Type Error --------------------------------------------------

>> Mismatched signature 'div' required by 'Dividable'.

14 |     pub def div(x: Int32, y: Int32): Int32 \ DivByZero = 
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
    pub def div(x: t, y: t): t \ Dividable.Aef[t]
}
```

and we re-implement the instances for `Float32` and `Int32`:

```flix
instance Dividable[Float32] {
    type Aef = { Pure } // No exception, div-by-zero yields NaN.
    pub def div(x: Float32, y: Float32): Float32 = x / y
}

instance Dividable[Int32] {
    type Aef = { DivByZero }
    pub def div(x: Int32, y: Int32): Int32 \ DivByZero = 
        if (y == 0) DivByZero.throw() else x / y
}
```

### Associated Effects and Regions

We often want to use associated effects in combination with regions.

Assume we have the `ForEach` trait from the before:

```flix
trait ForEach[t] {
    type Elm
    pub def forEach(f: ForEach.Elm[t] -> Unit \ ef, x: t): Unit \ ef
}
```

As we have seen, we can implement it for e.g. `List[t]` but also `Map[k, v]`.
But what if we wanted to implement it for e.g. `MutList[t, r]` or `MutSet[t,
r]`. We can try: 

```flix
instance ForEach[MutList[t, r]] {
    type Elm = t
    pub def forEach(f: t -> Unit \ ef, x: MutList[t, r]): Unit \ ef = 
        MutList.forEach(f, x)
}
```

But Flix reports:

```
❌ -- Type Error -------------------------------------------------- 

>> Unable to unify the effect formulas: 'ef' and 'ef + r'.

9 |         MutList.forEach(f, x)
            ^^^^^^^^^^^^^^^^^^^^^
            mismatched effect formulas.
```

The problem is that `MutList.forEach` has an effect in the region `r`, but the
signature of `forEach` in the trait only permits the `ef` effect from the
function `f`. 

We can solve the problem by extending the `ForEach` trait with an associated effect:

```flix
trait ForEach[t] {
    type Elm
    type Aef: Eff
    pub def forEach(f: ForEach.Elm[t] -> Unit \ ef, x: t): Unit \ ef + ForEach.Aef[t]
}
```

We must specify that `Aef` is an effect with the kind annotation `Aef: Eff`. If
we don't specify the kind then it defaults to `Type` which is not what we want
here. 

With the updated `ForEach` trait, we can implement it for both `List[t]` and
`MutList[t]`:

```flix
instance ForEach[List[t]] {
    type Elm = t
    type Aef = { Pure }
    pub def forEach(f: t -> Unit \ ef, x: List[t]): Unit \ ef = List.forEach(f, x)
}
```

and 

```flix
instance ForEach[MutList[t, r]] {
    type Elm = t
    type Aef = { r }
    pub def forEach(f: t -> Unit \ ef, x: MutList[t, r]): Unit \ ef + r = 
        MutList.forEach(f, x)
}
```

Notice how the implementation for `List[t]` specifies that the associated effect
is pure, whereas the implementation for `MutList[t, r]` specifies that there is
a heap effect in region `r`. 

