# Laziness

Flix uses eager evaluation in most circumstances, but allows the programmer to opt-in to lazy evaluation when appropriate with the `lazy` keyword:

```flix
let x: Lazy[Int32] = lazy (1 + 2);
```

The expression won't be evaluated until it's *forced*:

```flix
let y: Int32 = force x;
```
> **Note:** The `lazy` construct requires the expression it's given to be pure.

> **Note:** Forcing a lazy value that's already been evaluated won't evaluate it for a second time.

## Lazy data structures

Laziness can be used to create lazy data structures which are evaluated as they're used. This even allows us to create infinite data structures.

Here for example, is a data structure which implements an infinitely long stream of integers which increase by one each time:

```flix
namespace IntStream {

    enum IntStream { case SCons(Int32, Lazy[IntStream]) }

    pub def from(x: Int32): IntStream =
        IntStream.SCons(x, lazy from(x + 1))
}
```

Given this, we can implement functions such as `map` and `take`:

```flix
    pub def take(n: Int32, s: IntStream): List[Int32] =
        match n {
            case 0 => Nil
            case _ => match s {
                case SCons(h, t) => h :: take(n - 1, force t)
            }
        }

    pub def map(f: Int32 -> Int32, s: IntStream): IntStream =
        match s {
            case SCons(h, t) => IntStream.SCons(f(h), lazy map(f, force t))
        }
```

So, for example:

```flix
IntStream.from(42) |> IntStream.map(x -> x + 10) |> IntStream.take(10)
```

Will return:

```flix
52 :: 53 :: 54 :: 55 :: 56 :: 57 :: 58 :: 59 :: 60 :: 61 :: Nil
```

Flix provides `DelayList` and `DelayMap` data structures which already implement this functionality and more:

```flix
DelayList.from(42) |> DelayList.map(x -> x + 10) |> DelayList.take(10)
```
