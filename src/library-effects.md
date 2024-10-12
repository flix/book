## Library Effects

Flix comes with a collection of built-in effects that are available in the
standard library. 

Each effect introduces a companion module which contains both `handle` and `run`
functions. 

Here are some of them: 

### Clock

```flix
eff Clock {
    /// Returns a measure of time since the epoch in the given time unit `u`.
    pub def currentTime(u: TimeUnit): Int64
}
```

The `Clock` module also contains the methods:

```flix
TBD
```

Every effect comes with these `handle` and `run` functions in the companion module of the effect. 

### Console

```flix
eff Console {
    /// Reads a single line from the console.
    pub def readln(): String

    /// Prints the given string `s` to the standard out.
    pub def print(s: String): Unit

    /// Prints the given string `s` to the standard err.
    pub def printErr(s: String): Unit

    /// Prints the given string `s` to the standard out followed by a new line.
    pub def println(s: String): Unit

    /// Prints the given string `s` to the standard err followed by a new line.
    pub def printlnErr(s: String): Unit
}
```

### Logger

```flix
pub eff Logger {

    ///
    /// Logs the given message `m` at the given severity `s`.
    ///
    pub def log(s: Severity, m: String): Unit

}
```

Module provides:

```flix
mod Logger {
    ///
    /// Logs the message `m` at the `Trace` level.
    ///
    pub def trace(m: a): Unit \ Logger with ToString[a] = do Logger.log(Severity.Trace, "${m}")

    ///
    /// Logs the message `m` at the `Debug` level.
    ///
    pub def debug1(m: a): Unit \ Logger with ToString[a] = do Logger.log(Severity.Debug, "${m}")

    ///
    /// Logs the message `m` at the `Info` level.
    ///
    pub def info(m: a): Unit \ Logger with ToString[a] = do Logger.log(Severity.Info, "${m}")

    ///
    /// Logs the message `m` at the `Warn` level.
    ///
    pub def warn(m: a): Unit \ Logger with ToString[a] = do Logger.log(Severity.Warn, "${m}")

    ///
    /// Logs the message `m` at the `Fatal` level.
    ///
    pub def fatal(m: a): Unit \ Logger with ToString[a] = do Logger.log(Severity.Fatal, "${m}")
}
```

### Process

```flix
eff Process {

    ///
    /// Immediately executes the command `cmd` passing the arguments `args`.
    ///
    pub def exec(cmd: String, args: List[String]): Unit

}
```

### Random

```flix
pub eff Random {

    ///
    /// Returns a pseudorandom boolean.
    ///
    pub def randomBool(): Bool

    ///
    /// Returns a pseudorandom 32-bit floating-point number.
    ///
    pub def randomFloat32(): Float32

    ///
    /// Returns a pseudorandom 64-bit floating-point number.
    ///
    pub def randomFloat64(): Float64

    ///
    /// Returns a pseudorandom 32-bit integer.
    ///
    pub def randomInt32(): Int32

    ///
    /// Returns a pseudorandom 64-bit integer.
    ///
    pub def randomInt64(): Int64

    ///
    /// Returns a Gaussian distributed 64-bit floating point number.
    ///
    pub def randomGaussian(): Float64

}
```

### Running Effects

If we have a program that uses the `Clock` effect:

```flix
def getEpoch(): Int64 \ {Clock} = Clock.now()
```

We can run it by writing:

```flix
def main(): Unit \ IO = 
    println(Clock.handle(getEpoch)())
```

If a function has multiple effects:

```flix
def greet(name: String): Unit \ {Clock, Console} = ...
```

We can run the program by writing:

```flix
def main(): Unit \ IO = 
    println(Clock.handle(Console.handle(getEpoch))())
```

### Using App

Manually adding all the handlers can be tedius. For a simpler solution, which
handles all library provided effects, we can use `App.run`:

```flix
def main(): Unit \ IO = 
    App.run(myFunction)
```
