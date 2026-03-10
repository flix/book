# Process

Flix provides `Process` as a library effect for spawning and managing OS
processes. The `Process` effect has a default handler, so no explicit
`runWithIO` call is needed in `main`. The key module is `Sys.Process`.

## The Process Effect

The `Process` effect supports spawning processes, accessing their I/O streams,
and waiting for completion:

```flix
pub eff Process {
    /// Executes `cmd` with `args`, working directory `cwd`, and environment `env`.
    def execWithCwdAndEnv(cmd: String, args: List[String],
        cwd: Option[String], env: Map[String, String]):
        Result[IoError, ProcessHandle]

    /// Returns the exit value of the process `ph`.
    def exitValue(ph: ProcessHandle): Result[IoError, Int32]

    /// Returns whether the process `ph` is alive.
    def isAlive(ph: ProcessHandle): Result[IoError, Bool]

    /// Returns the PID of the process `ph`.
    def pid(ph: ProcessHandle): Result[IoError, Int64]

    /// Returns the stdin stream of the process `ph`.
    def stdin(ph: ProcessHandle): Result[IoError, StdIn]

    /// Returns the stdout stream of the process `ph`.
    def stdout(ph: ProcessHandle): Result[IoError, StdOut]

    /// Returns the stderr stream of the process `ph`.
    def stderr(ph: ProcessHandle): Result[IoError, StdErr]

    /// Stops the process `ph`.
    def stop(ph: ProcessHandle): Result[IoError, Unit]

    /// Waits for the process `ph` to finish and returns its exit value.
    def waitFor(ph: ProcessHandle): Result[IoError, Int32]

    /// Waits at most `time` (in the given `tUnit`) for the process `ph` to finish.
    /// Returns `true` if the process exited, `false` if the timeout elapsed.
    def waitForTimeout(ph: ProcessHandle, time: Int64, tUnit: TimeUnit):
        Result[IoError, Bool]
}
```

## The Process Module

The `S` module provides convenience functions built on the `Process`
effect:

```flix
mod Process {
    /// Executes the command `cmd` with the arguments `args`.
    def exec(cmd: String, args: List[String]):
        Result[IoError, ProcessHandle] \ Process

    /// Executes `cmd` with `args` and working directory `cwd`.
    def execWithCwd(cmd: String, args: List[String], cwd: Option[String]):
        Result[IoError, ProcessHandle] \ Process

    /// Executes `cmd` with `args` and environment variables `env`.
    def execWithEnv(cmd: String, args: List[String], env: Map[String, String]):
        Result[IoError, ProcessHandle] \ Process
}
```

## Executing a Command

The simplest way to spawn an OS process is with `Process.exec`. It takes a
command and a list of arguments, and returns a
`Result[IoError, ProcessHandle]`:

```flix
use Sys.Process

def main(): Unit \ { Process, IO } =
    match Process.exec("java", "-version" :: Nil) {
        case Result.Ok(_)    => println("Process started successfully.")
        case Result.Err(err) => println("Unable to execute process: ${err}")
    }
```

## Reading Process Output

After spawning a process, you can access its output streams with
`Process.stdout` and `Process.stderr`. The returned `StdOut` and `StdErr` types
implement `Readable`, so you can read bytes from them:

```flix
use Sys.Process

def main(): Unit \ { Process, IO } = region rc {
    match Process.exec("java", "-version" :: Nil) {
        case Result.Err(err) => println("exec failed: ${err}")
        case Result.Ok(ph)   =>
            match Process.stderr(ph) {
                case Result.Err(err) => println("stderr failed: ${err}")
                case Result.Ok(err)  =>
                    let buf = Array.repeat(rc, 1024, (0i8: Int8));
                    match Readable.read(buf, err) {
                        case Result.Err(e) => println("read failed: ${e}")
                        case Result.Ok(n)  => println("Read ${n} bytes from stderr.")
                    }
            }
    }
}
```

> **Note:** `java -version` writes to stderr, not stdout.

## Waiting for Completion

Use `Process.waitFor` to block until a process exits. It returns the exit code
as an `Int32`:

```flix
use Sys.Process

def main(): Unit \ { Process, IO } =
    match Process.exec("java", "-version" :: Nil) {
        case Result.Err(err) => println("exec failed: ${err}")
        case Result.Ok(ph)   =>
            match Process.waitFor(ph) {
                case Result.Err(err) => println("waitFor failed: ${err}")
                case Result.Ok(code) => println("Process exited with code: ${code}")
            }
    }
```

## Working Directory and Environment

`Process.execWithCwd` spawns a process with a specific working directory.
`Process.execWithEnv` passes additional environment variables:

```flix
use Sys.Process

def main(): Unit \ { Process, IO } =
    match Process.execWithCwd("java", "-version" :: Nil, Some("/tmp")) {
        case Result.Ok(_)    => println("execWithCwd succeeded.")
        case Result.Err(err) => println("execWithCwd failed: ${err}")
    };
    match Process.execWithEnv("java", "-version" :: Nil, Map#{"MY_VAR" => "hello"}) {
        case Result.Ok(_)    => println("execWithEnv succeeded.")
        case Result.Err(err) => println("execWithEnv failed: ${err}")
    }
```

