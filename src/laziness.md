# Laziness

Flix uses eager evaluation in most circumstances, but allows the programmer to opt-in to lazy evaluation when appropriate with the `lazy` keyword:

```flix
let x: Lazy[Int32] = lazy (1 + 2);
```

The expression won't be evaluated until it's *forced*:

```flix
let y: Int32 = force x;
```

Forcing a lazy value that's already been evaluated won't evaluate it for a second time.

## Delaying execution

Laziness can delay evaluation of something expensive until it's used:

```flix
// Emulate an expensive operation
def expensive(n: String): String =
    import static java.lang.Thread.sleep(Int64): Unit \ {};
    debug!("Expensive: " + n);
    let _ = sleep(5000i64);
    n

def lazily(): Unit \ IO =
    let x = lazy expensive("x");
    let y = lazy expensive("y");
    let _z = lazy expensive("z");
    let combined = force x + force y + force y;
    println(combined)
```

Which outputs:

```
Expensive: x 
Expensive: y
xyy
```

Note that `y` is only evaluated once even though it's forced twice, and `z` isn't evaluated because it's never forced.

## Lazy data structures

Laziness can also be used to create lazy data structures which are evaluated as they're used. This even allows us to create infinite data structures.

Here for example, is a data structure which implements an infinitely long list of integers which increase by one each time:

```flix
enum Forever { case Forever(Int32, Lazy[Forever]) }

def forever(x: Int32): Forever = 
    Forever.Forever(x, lazy forever(x + 1))
```

```flix
def exerciseForever(): Unit \ IO =
    let Forever(a, t1) = forever(1);
    let Forever(b, t2) = force t1;
    let Forever(c, _) = force t2;
    println((a, b, c))
```

Which outputs:

```
(1, 2, 3)  
```

Flix provides `DelayList` and `DelayMap` data structures, for example:

```flix
DelayList.from(10) |> DelayList.map(x -> x + 1) |> DelayList.take(10)
```
