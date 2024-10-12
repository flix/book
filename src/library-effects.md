## Library Effects

The Flix Standard Library comes with a collection of effects and handlers ready
for use. 

### Clock

Flix defines a `Clock` effect to access the time since the [UNIX epoch](https://en.wikipedia.org/wiki/Unix_time):

```flix
eff Clock {
    /// Returns a measure of time since the epoch in the given time unit `u`.
    def currentTime(u: TimeUnit): Int64
}
```

The `Clock` companion module also defines the functions `run` and `handle`:

```flix
mod Clock {
    /// Runs `f` handling the `Clock` effect using `IO`.
    def run(f: Unit -> a \ ef): a \ (ef - {Clock} + IO)

    /// Returns `f` where the `Clock` effect has been handled using `IO`.
    def handle(f: a -> b \ ef): a -> b \ (ef - {Clock} + IO)
}
```

Every standard library effect defines a companion module with `run` and `handle`
functions.

### Console

Flix defines a `Console` effect to read from and write to the user's shell:

```flix
eff Console {
    /// Reads a single line from the console.
    def readln(): String

    /// Prints the given string `s` to the standard out.
    def print(s: String): Unit

    /// Prints the given string `s` to the standard err.
    def eprint(s: String): Unit

    /// Prints the given string `s` to the standard out followed by a new line.
    def println(s: String): Unit

    /// Prints the given string `s` to the standard err followed by a new line.
    def eprintln(s: String): Unit
}
```

### Logger

Flix defines a `Logger` effect for logging messages:

```flix
eff Logger {
    /// Logs the given message `m` at the given severity `s`.
    def log(s: Severity, m: String): Unit
}
```

The `Logger` companion module provides several convenience functions:

```flix
mod Logger {
    /// Logs the message `m` at the `Trace` level.
    def trace(m: a): Unit \ Logger with ToString[a]

    /// Logs the message `m` at the `Debug` level.
    def debug(m: a): Unit \ Logger with ToString[a]

    /// Logs the message `m` at the `Info` level.
    def info(m: a): Unit \ Logger with ToString[a]

    /// Logs the message `m` at the `Warn` level.
    def warn(m: a): Unit \ Logger with ToString[a]

    /// Logs the message `m` at the `Fatal` level.
    def fatal(m: a): Unit \ Logger with ToString[a]
}
```

### Process

Flix defines a `Process` effect for execution of commands outside of the JVM:

```flix
eff Process {
    /// Immediately executes the command `cmd` passing the arguments `args`.
    def exec(cmd: String, args: List[String]): Unit
}
```

### Random

Flix defines a `Random` effect for the creation of random values:

```flix
eff Random {
    /// Returns a pseudorandom boolean.
    def randomBool(): Bool

    /// Returns a pseudorandom 32-bit floating-point number.
    def randomFloat32(): Float32

    /// Returns a pseudorandom 64-bit floating-point number.
    def randomFloat64(): Float64

    /// Returns a pseudorandom 32-bit integer.
    def randomInt32(): Int32

    /// Returns a pseudorandom 64-bit integer.
    def randomInt64(): Int64

    /// Returns a Gaussian distributed 64-bit floating point number.
    def randomGaussian(): Float64
}
```

### Running Functions with Effects

As discussed, every Flix Standard Library effect provides two functions: `run`
and `handle` for re-interpreting the effect in `IO`. In other words, for
**making the effect happen**. 

For example, if a we have a function that uses the `Clock` effect:

```flix
def getEpoch(): Int64 \ Clock = Clock.now()
```

We can run it by writing:

```flix
def main(): Unit \ IO = 
    println(Clock.run(getEpoch))
```

Or we can handle it and then run the returned function:

```flix
def main(): Unit \ IO = 
    let f = Clock.handle(getEpoch);
    println(f())
```

If a function has multiple effects:

```flix
def greet(name: String): Unit \ {Clock, Console} = ...
```

We cannot easily use `run`, but we can use `Clock.handle` and `Console.handle`:

```flix
def main(): Unit \ IO = 
    let f = Clock.handle(
                Console.handle(
                    () -> greet("Mr. Bond")));
    println(f())
```

We had to write `() -> greet("Mr. Bond")` because `handle` takes a function as
its argument.

### Using App

Using individual handlers can be cumbersome. For convenience, Flix offers a
`App.runAll` function which can handle all effects in the standard library:

```flix
def main(): Unit \ IO = 
    App.runAll(() -> greet("Mr. Bond"))
```
