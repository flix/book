## Library Effects

The Flix Standard Library comes with a collection of algebraic effects and
handlers.

We give an overview of the most important to illustrate their use.

### Clock

Flix defines a `Clock` effect to access the time since the [UNIX epoch](https://en.wikipedia.org/wiki/Unix_time):

```flix
eff Clock {
    /// Returns a measure of time since the epoch in the given time unit `u`.
    def currentTime(u: TimeUnit): Int64
}
```

```flix
mod Clock {
    /// Runs `f` handling the `Clock` effect using `IO`.
    def runWithIO(f: Unit -> a \ ef): a \ (ef - {Clock} + IO)

    /// Returns `f` with the `Clock` effect handled using `IO`.
    def handle(f: a -> b \ ef): a -> b \ (ef - {Clock} + IO)
}
```

Every effect in the standard library comes with `handle` and `runWithIO`
functions.

#### Example: Using `Clock`

```flix
def main(): Unit \ IO = 
    run {
        println(Clock.currentTime(TimeUnit.Milliseconds))
    } with Clock.runWithIO
```

### Console

Flix defines a `Console` effect to read from and write to shell:

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

#### Example: Using `Console`

```flix
def main(): Unit \ IO = 
    run {
        Console.println("Please enter your name: ");
        let name = Console.readln();
        Console.println("Hello ${name}")
    } with Console.runWithIO
```

### FileReadWithResult

Flix defines a `FileReadWithResult` effect to read from the file system:

```flix
eff FileReadWithResult {
    /// Returns `true` if the given file `f` exists.
    def exists(f: String): Result[IoError, Bool]

    /// Returns `true` is the given file `f` is a directory.
    def isDirectory(f: String): Result[IoError, Bool]

    /// Returns `true` if the given file `f` is a regular file.
    def isRegularFile(f: String): Result[IoError, Bool]

    /// Returns `true` if the given file `f` is readable.
    def isReadable(f: String): Result[IoError, Bool]

    /// Returns `true` if the given file `f` is a symbolic link.
    def isSymbolicLink(f: String): Result[IoError, Bool]

    /// Returns `true` if the given file `f` is writable.
    def isWritable(f: String): Result[IoError, Bool]

    /// Returns `true` if the given file `f` is executable.
    def isExecutable(f: String): Result[IoError, Bool]

    /// Returns the last access time of the given file `f` in milliseconds since the epoch.
    def accessTime(f: String): Result[IoError, Int64]

    /// Returns the creation time of the given file `f` in milliseconds since the epoch.
    def creationTime(f: String): Result[IoError, Int64]

    /// Returns the last-modified timestamp of the given file `f` in milliseconds since the epoch.
    def modificationTime(f: String): Result[IoError, Int64]

    /// Returns the size of the given file `f` in bytes.
    def size(f: String): Result[IoError, Int64]

    /// Returns a string of all lines in the given file `f`.
    def read(f: String): Result[IoError, String]

    /// Returns a list of all lines in the given file `f`.
    def readLines(f: String): Result[IoError, List[String]]

    /// Returns a vector of all the bytes in the given file `f`.
    def readBytes(f: String): Result[IoError, Vector[Int8]]

    /// Returns a list with the names of all files and directories in the given directory `d`.
    def list(f: String): Result[IoError, List[String]]
}
```

#### Example: Using `FileReadWithResult`

```flix
def main(): Unit \ IO = 
    run {
        match FileReadWithResult.readLines("Main.flix") {
            case Result.Ok(lines) => 
                lines |> List.forEach(println)
            case Result.Err(err) => 
                println("Unable to read file. Error: ${err}")
        }
    } with FileReadWithResult.runWithIO
```

### FileWriteWithResult

Flix defines a `FileWriteWithResult` effect to write to the file system:

```flix
eff FileWriteWithResult {
    /// Writes `str` to the given file `f`.
    def write(data: {str = String}, f: String): Result[IoError, Unit]

    /// Writes `lines` to the given file `f`.
    def writeLines(data: {lines = List[String]}, f: String): Result[IoError, Unit]

    /// Writes `data` to the given file `f`.
    def writeBytes(data: Vector[Int8], f: String): Result[IoError, Unit]

    /// Appends `str` to the given file `f`.
    def append(data: {str = String}, f: String): Result[IoError, Unit]

    /// Appends `lines` to the given file `f`.
    def appendLines(data: {lines = List[String]}, f: String): Result[IoError, Unit]

    /// Appends `data` to the given file `f`.
    def appendBytes(data: Vector[Int8], f: String): Result[IoError, Unit]

    /// Truncates the given file `f`.
    def truncate(f: String): Result[IoError, Unit]

    /// Creates the directory `d`.
    def mkDir(d: String): Result[IoError, Unit]

    /// Creates the directory `d` and all its parent directories.
    def mkDirs(d: String): Result[IoError, Unit]

    /// Creates a new temporary directory with the given prefix.
    def mkTempDir(prefix: String): Result[IoError, String]
}
```

#### Example: Using `FileWriteWithResult`

```flix
def main(): Unit \ IO = 
    run {
        let data = List#{"Hello", "World"};
        match FileWriteWithResult.writeLines(lines = data, "data.txt"){
            case Result.Ok(_)    => ()
            case Result.Err(err) => 
                println("Unable to write file. Error: ${err}")
        }
    } with FileWriteWithResult.runWithIO
```

### HttpWithResult

Flix defines a `HttpWithResult` effect to communicate over HTTP:

```flix
eff HttpWithResult {
    def request(method: String, url: String, headers: Map[String, List[String]], body: Option[String]): Result[IoError, Http.Response]
}
```

The `HttpWithResult` companion module provides several convenience functions:

```flix
mod HttpWithResult {
    /// Send a `GET` request to the given `url` with the given `headers` and wait for the response.
    def get(url: String, headers: Map[String, List[String]]): Result[IoError, Http.Response] \ HttpWithResult

    /// Send a `POST` request to the given `url` with the given `headers` and `body` and wait for the response.
    def post(url: String, headers: Map[String, List[String]], body: String): Result[IoError, Http.Response] \ HttpWithResult

    /// Send a `PUT` request to the given `url` with the given `headers` and `body` and wait for the response.
    def put(url: String, headers: Map[String, List[String]], body: String): Result[IoError, Http.Response] \ HttpWithResult
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

Flix defines a `Process` effect for running commands outside of the JVM:

```flix
eff Process {
    /// Executes the command `cmd` with the arguments `args`, by the path `cwd` and with the environmental `env`.
    def execWithCwdAndEnv(cmd: String, args: List[String], cwd: Option[String], env: Map[String, String]): ProcessHandle
}
```

The `Process` companion module provides several convenience functions:

```flix
/// Executes the command `cmd` with the arguments `args`.
pub def exec(cmd: String, args: List[String]): ProcessHandle \ Process

/// Executes the command `cmd` with the arguments `args`, by the path `cwd`.
def execWithCwd(cmd: String, args: List[String], cwd: Option[String]): ProcessHandle \ Process

/// Executes the command `cmd` with the arguments `args` and with the environmental `env`.
def execWithEnv(cmd: String, args: List[String], env: Map[String, String]): ProcessHandle \ Process
```

### Random

Flix defines a `Random` effect for the generation of random values:

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

### Running Functions with Algebraic Effects

Every Flix Standard Library effects defines two functions: `runWith` and
`handle` in the companion module of the effect. We can use these functions to
re-interpret the effect in `IO`. That is, **to make the effect happen.**

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

If a function has more than one effect we cannot use `run`. Instead, we must
handle each effect, and call the result. For example, we can use `Clock.handle`
and `Console.handle`:

```flix
def main(): Unit \ IO = 
    let f = Clock.handle(
                Console.handle(
                    () -> greet("Mr. Bond")));
    println(f())
```

We have to write `() -> greet("Mr. Bond")` because `handle` expects a function. 

### Using Pre-defined Handlers

As the above examples show, it can be cumbersome to use the library provided
`handle` functions. A simpler approach is to use the provided `runWith`
functions. 

For example, we can write:

```flix
def greet(name: String): Unit \ {Clock, Console} = 
    let h = Clock.now();
    Console.println("Hello ${name}. The current time is: ${h}")

def main(): Unit \ IO = 
    run {
        greet("James Bond")
    } with Clock.runWithIO
      with Console.runWithIO
```
