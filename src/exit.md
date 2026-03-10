# Exit

Flix provides `Exit` as a library effect for terminating the program. The `Exit`
effect has a default handler, so no explicit `runWithIO` call is needed in
`main`. The key module is `Sys.Exit`.

## The Exit Effect

The `Exit` effect has a single operation that immediately stops the JVM with a
given exit code:

```flix
pub eff Exit {
    /// Immediately exits the JVM with the specified `exitCode`.
    def exit(exitCode: Int32): Void
}
```

The return type `Void` indicates that `exit` never returns normally.

## Exiting the Program

The simplest use of `Exit` is to terminate with a specific exit code:

```flix
use Sys.Exit

def main(): Unit \ { Exit, IO } =
    println("Goodbye!");
    Exit.exit(0)
```

A zero exit code conventionally signals success, while a non-zero code signals
an error.
