# Sleep

Flix provides `Sleep` as a library effect for pausing the current thread. The
`Sleep` effect has a default handler, so no explicit `runWithIO` call is needed
in `main`. The key module is `Time.Sleep`.

## The Sleep Effect

The `Sleep` effect has a single operation:

```flix
pub eff Sleep {
    /// Sleeps the current thread for the given duration `d`.
    def sleep(d: Duration): Unit
}
```

Durations are created with helpers from the `Time.Duration` module, such as
`seconds`, `milliseconds`, `minutes`, and so on.

## Basic Sleep

The simplest use of `Sleep` is to pause for a fixed duration:

```flix
use Time.Duration.seconds
use Time.Sleep

def main(): Unit \ { Sleep, IO } =
    println("Going to sleep...");
    Sleep.sleep(seconds(1));
    println("Woke up!")
```

## No-Op Sleep

The `withNoOp` handler skips all sleeps, which is useful for testing code that
contains delays without actually waiting:

```flix
use Time.Duration.seconds
use Time.Sleep

def main(): Unit \ IO =
    run {
        println("Going to sleep...");
        Sleep.sleep(seconds(10));
        println("Woke up instantly!")
    } with Sleep.withNoOp
```

Because `withNoOp` fully handles the `Sleep` effect, the result type no longer
includes `Sleep`.

## Middleware

The `Time.Sleep` module provides several middleware handlers that intercept and
transform sleep durations before forwarding to the underlying `Sleep` effect.
Middleware re-raises `Sleep`, so multiple layers can be composed.

| Middleware          | Description                                               |
|---------------------|-----------------------------------------------------------|
| `withConstant`      | Replaces every sleep duration with a fixed value.         |
| `withScale`         | Multiplies each duration by a factor.                     |
| `withMaxSleep`      | Caps each individual sleep to a maximum.                  |
| `withMinSleep`      | Ensures each sleep is at least a minimum.                 |
| `withMaxTotalSleep` | Caps the cumulative sleep across all calls to a budget.   |
| `withJitter`        | Adds random jitter (±factor) to each duration.            |
| `withLogging`       | Logs each sleep duration via the `Logger` effect.         |
| `withCollect`       | Collects all durations into a list instead of sleeping.   |

For example, `withMaxSleep` caps each sleep to a maximum and `withLogging` logs
each duration:

```flix
use Time.Duration.{milliseconds, seconds}
use Time.Sleep

def main(): Unit \ { Logger, Sleep, IO } =
    run {
        println("Sleeping for 2 seconds (capped to 500ms)...");
        Sleep.sleep(seconds(2));
        println("Done!")
    } with Sleep.withMaxSleep(milliseconds(500))
      with Sleep.withLogging
```

## Composing Middleware

Because each middleware re-raises `Sleep`, they stack naturally. The following
example adds ±20% random jitter to each sleep and logs the resulting durations:

```flix
use Math.Random
use Time.Duration.{seconds}
use Time.Sleep

/// Composes `withJitter` and `withLogging` to add ±20% random jitter
/// to sleep durations and log each sleep via the `Logger` effect.
def main(): Unit \ { Logger, Random, Sleep, IO } =
    run {
        println("Sleeping 3 times with ±20% jitter...");
        Sleep.sleep(seconds(1));
        Sleep.sleep(seconds(2));
        Sleep.sleep(seconds(3));
        println("Done!")
    } with Sleep.withJitter(0.2)
      with Sleep.withLogging
```

The order matters: `withJitter` intercepts the original durations, applies
jitter, and re-raises `Sleep`. The `withLogging` handler then sees the
jittered durations.
