# Logger

Flix provides `Logger` as a library effect for structured logging. The `Logger`
effect has a default handler, so no explicit `runWithIO` call is needed in
`main`. The key module is `Logger`.

## The Logger Effect

The `Logger` effect has a single operation that logs a message at a given
severity:

```flix
pub eff Logger {
    /// Logs the given message `m` at the given severity `s`.
    def log(s: Severity, m: RichString): Unit
}
```

The `Severity` enum defines five levels, from lowest to highest:

```flix
pub enum Severity with Eq, Order, ToString {
    case Trace
    case Debug
    case Info
    case Warn
    case Fatal
}
```

## The Logger Module

The `Logger` module provides convenience functions:

```flix
mod Logger {
    /// Logs the message `m` at the Trace level.
    def trace(m: a): Unit \ Logger with Formattable[a]

    /// Logs the message `m` at the Debug level.
    def debug(m: a): Unit \ Logger with Formattable[a]

    /// Logs the message `m` at the Info level.
    def info(m: a): Unit \ Logger with Formattable[a]

    /// Logs the message `m` at the Warn level.
    def warn(m: a): Unit \ Logger with Formattable[a]

    /// Logs the message `m` at the Fatal level.
    def fatal(m: a): Unit \ Logger with Formattable[a]
```

> **Note:** The logging functions accept any type that implements the
> `Formattable` trait. Most standard types (`String`, `Int32`, `Bool`, etc.)
> implement `Formattable`, so plain values can be logged directly. The trait
> converts values into `RichString`, which supports styled terminal output
> (colors, bold, etc.).

## Logging Messages

The convenience functions accept any value that implements `Formattable`:

```flix
def main(): Unit \ { Logger } =
    Logger.info("Application started");
    Logger.debug("Loading configuration...");
    Logger.warn("Cache size exceeds threshold");
    Logger.fatal("Unrecoverable error")
```

The default handler prints each message to standard output with a colored
severity prefix, for example: `[Info] Application started`.
