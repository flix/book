# Common Problems

- [ToString is not defined on 'a'](#tostring-is-not-defined-on-a)
- [Records and Complex Instances](#records-and-complex-instances)
- [Expected kind 'Bool or Effect' here, but kind 'Type' is used](#expected-kind-bool-or-effect-here-but-kind-type-is-used)
- [Mismatched type arguments for effect](#mismatched-type-arguments-for-effect)

## ToString is not defined on 'a'

Given the program:

```flix
def main(): Unit \ IO =
    let l = Nil;
    println(l)
```

The Flix compiler reports:

```
❌ -- Type Error ---------------------

>> ToString is not defined on a. [...]

3 |     println(l)
        ^^^^^^^^^^
        missing ToString instance
```

The issue is that the empty list has the polymorphic type: `List[a]` for any
`a`. This means that Flix cannot select the appropriate `ToString` trait
instance.

The solution is to specify the type of the empty list. For example, we can write:

```flix
def main(): Unit \ IO =
    let l: List[Int32] = Nil;
    println(l)
```

which solves the problem because Flix can find an instance of `ToString` trait
for the concrete type `List[Int32]`.

## Records and Complex Instances

Given the program:

```flix
instance Eq[{fstName = String, lstName = String}]
```

The Flix compiler reports:

```
❌ -- Instance Error --------------------------------------------------

>> Complex instance type '{ fstName = String, lstName = String }' in 'Eq'.

1 | instance Eq[{fstName = String, lstName = String}]
             ^^
             complex instance type
```

This is because, at least for the moment, it is not possible to define
trait instances on records (or Datalog schema rows). This may change in the
future. Until then, it is necessary to wrap the record in an algebraic data
type. For example:

```flix
enum Person({fstName = String, lstName = String})
```

and then we can implement `Eq` for the `Person` type:

```flix
instance Eq[Person] {
    pub def eq(x: Person, y: Person): Bool =
        let Person(r1) = x;
        let Person(r2) = y;
        r1#fstName == r2#fstName and r1#lstName == r2#lstName
}
```

## Expected kind 'Bool or Effect' here, but kind 'Type' is used

Given the program:

```flix
enum A[a, b, ef] {
    case A(a -> b \ ef)
}
```

The Flix compiler reports:

```
❌ -- Kind Error -----------------------------------------------

>> Expected kind 'Bool or Effect' here, but kind 'Type' is used.

2 |     case A(a -> b \ ef)
                        ^^
                        unexpected kind.

Expected kind: Bool or Effect
Actual kind:   Type
```

This is because Flix assumes every un-annotated type variable to have kind
`Type`. However, in the above case `a` and `b` should have kind `Type`, but `ef`
should have kind `Bool`. We can make this explicit like so:

```flix
enum A[a: Type, b: Type, ef: Bool] {
    case A(a -> b \ ef)
}
```

## Mismatched type arguments for effect

Given the program:

```flix
eff Emit[t] {
    def emit(x: t): Unit
}

def f(): Unit \ Emit[Int32] + Emit[String] =
    Emit.emit(42);
    Emit.emit("Hello")
```

The Flix compiler reports:

```
-- Type Error [E6795] -------------------------------------------- src/Main.flix

>> Mismatched type arguments for effect 'Emit': 'Int32' and 'String'.

5 | def f(): Unit \ Emit[Int32] + Emit[String] =
                                  ^^^^^^^^^^^^
                                  mismatched effect type argument.

The effect 'Emit' is used with different types for its 1st type parameter 't'.

Effect One: Emit[Int32]
Effect Two: Emit[String]
```

The issue is that a [polymorphic effect](./polymorphic-effects.md) must be used
with the same type arguments throughout a function. This includes effects that
are handled inside the function.

The solution is to move each use into its own function. For example, we can
write:

```flix
def f(): Unit \ Emit[Int32] =
    Emit.emit(42)

def g(): Unit \ Emit[String] =
    Emit.emit("Hello")
```
