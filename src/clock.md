# Clock

Flix provides `Clock` as a library effect for querying the current wall-clock
time. The `Clock` effect has a default handler, so no explicit `runWithIO` call
is needed in `main`. The key module is `Time.Clock`.

## The Clock Effect

The `Clock` effect has a single operation that returns the time since the epoch
in a given unit:

```flix
pub eff Clock {
    /// Returns a measure of time since the epoch in the given time unit `u`.
    def currentTime(u: TimeUnit): Int64
}
```

The `TimeUnit` enum determines the granularity of the result:

```flix
pub enum TimeUnit with Eq, ToString {
    case Days,
    case Hours,
    case Microseconds,
    case Milliseconds,
    case Minutes,
    case Nanoseconds,
    case Seconds
}
```

## Reading the Current Time

The simplest use of `Clock` is to read the current time and print it:

```flix
use Time.Clock
use Time.TimeUnit

def main(): Unit \ { Clock, IO } =
    let timestamp = Clock.currentTime(TimeUnit.Milliseconds);
    println("${timestamp} ms since the epoch")
```

Because `Clock` has a default handler, the effect is handled automatically.

## The `now` Function

The `Clock.now` function is a shorthand for
`Clock.currentTime(TimeUnit.Milliseconds)`:

```flix
use Time.Clock

def main(): Unit \ { Clock, IO } =
    let before = Clock.now();
    // ... do some work ...
    let after = Clock.now();
    println("Elapsed: ${after - before} ms")
```
