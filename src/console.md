# Console

Flix provides `Console` as a library effect for terminal I/O. The `Console`
effect has a default handler, so no explicit `runWithIO` call is needed in
`main`. The key module is `Sys.Console`.

## The Console Effect

The `Console` effect supports reading from standard input and writing to
standard output and standard error:

```flix
pub eff Console {
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

## The Console Module

The `Console` module provides several higher-level functions built on the
`Console` effect:

```flix
mod Sys.Console {
    /// Prints prompt `p`, reads a line, and returns `default` if the input is empty.
    def readlnWithDefault(p: a, default: String): String \ Console

    /// Prints prompt `p`, reads a line, and applies `f` to the input.
    /// Re-prompts on `Err(msg)`, returns `v` on `Ok(v)`.
    def readlnWith(p: a, f: String -> Result[String, b]): b \ Console

    /// Prints prompt `p` with a yes/no hint and reads a boolean answer.
    /// Empty or unrecognized input returns `default`.
    def confirm(p: a, default: {default = Bool}): Bool \ Console

    /// Prints prompt `p` with a numbered list of choices and reads a selection.
    /// Returns `None` if the input is invalid.
    def pick(p: a, choices: List[b]): Option[b] \ Console

    /// Like `pick`, but re-prompts until the user makes a valid selection.
    def pickWith(p: a, choices: List[b]): b \ Console
}
```

## Basic Console I/O

The simplest use of `Console` is to print a prompt, read input, and respond:

```flix
use Sys.Console

def main(): Unit \ Console =
    Console.print("What is your name? ");
    let name = Console.readln();
    Console.println("Hello ${name}!")
```

## Confirmed Input

The `Console.confirm` function asks a yes/no question and returns a `Bool`. You
can supply a default value that is used when the user presses Enter without
typing anything:

```flix
use Sys.Console

def main(): Unit \ Console =
    let proceed = Console.confirm("Deploy to production?", default = true);
    if (proceed)
        Console.println("Deploying...")
    else
        Console.println("Aborted.")
```

## Validated Input

The `Console.readlnWith` function repeatedly prompts the user until the input
passes a validator. The validator returns `Ok(value)` on success or
`Err(message)` to re-prompt:

```flix
use Sys.Console

def main(): Unit \ Console =
    let n = Console.readlnWith("Enter a number (1-10): ", s ->
        match Int32.fromString(s) {
            case Some(i) if i >= 1 and i <= 10 => Ok(i)
            case _ => Err("Please enter a number between 1 and 10.")
        }
    );
    Console.println("You entered: ${n}")
```
