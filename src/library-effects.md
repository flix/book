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

### Exec

### Logger

### Process

### Random

### Time

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
