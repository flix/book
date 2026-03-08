# Process

Flix provides `Process` as a library effect for spawning and managing OS
processes. The `Process` effect has a default handler, so no explicit
`runWithIO` call is needed in `main`. The key module is `Sys.Process`.

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

## Other Operations

The `Sys.Process` module provides several additional operations:

- `Process.isAlive(ph)` — returns `true` if the process is still running
- `Process.pid(ph)` — returns the process ID
- `Process.stop(ph)` — terminates the process
- `Process.stdin(ph)` — returns the process's standard input stream (implements `Writable`)
- `Process.exitValue(ph)` — returns the exit code without blocking (fails if the process is still running)
- `Process.waitForTimeout(ph, time, tUnit)` — blocks until the process exits or the timeout expires
