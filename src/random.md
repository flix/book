# Random

Flix provides `Random` as a library effect for generating pseudorandom numbers.
The `Random` effect has a default handler, so no explicit `runWithIO` call is
needed in `main`. The key module is `Math.Random`.

## The Random Effect

The `Random` effect has two operations:

```flix
pub eff Random {
    /// Returns a pseudorandom 64-bit floating-point number in [0.0, 1.0].
    def randomFloat64(): Float64

    /// Returns a pseudorandom 64-bit integer.
    def randomInt64(): Int64
}
```

## Generating Random Values

The simplest use of `Random` is to generate a value and act on it:

```flix
use Math.Random

def main(): Unit \ { Random, IO } =
    let flip = Random.randomFloat64() > 0.5;
    if (flip)
        println("heads")
    else
        println("tails")
```

Because `Random` has a default handler, the effect is handled automatically with
a fresh random seed.

## Seeded Randomness

The `runWithSeed` handler uses a fixed seed so that every run produces the same
sequence of random values. This is useful for reproducible tests and
benchmarks:

```flix
use Math.Random

def main(): Unit \ IO =
    run {
        let a = Random.randomFloat64();
        let b = Random.randomFloat64();
        println("a = ${a}, b = ${b}")
    } with Random.runWithSeed(42i64)
```

Because a seeded random number generator is fully deterministic, `runWithSeed`
eliminates the `Random` effect without introducing `IO`.
