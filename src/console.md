# Console

Flix provides `Console` as a library effect for terminal I/O. The `Console`
effect has a default handler, so no explicit `runWithIO` call is needed in
`main`. The key module is `Sys.Console`.

## The Console Effect

The `Console` effect has five operations: one reads a line from standard input,
and four write a string to standard output or standard error:

```flix
pub eff Console {
    /// Reads a single line from the console.
    /// Returns `None` if the end of input has been reached.
    def readln(): Option[String]

    /// Writes the given string `s` to the standard out.
    def write(s: String): Unit

    /// Writes the given string `s` to the standard out followed by a new line.
    def writeLine(s: String): Unit

    /// Writes the given string `s` to the standard err.
    def writeErr(s: String): Unit

    /// Writes the given string `s` to the standard err followed by a new line.
    def writeErrLine(s: String): Unit
}
```

The operations are the interface that a handler implements. A program rarely
calls them directly. Instead it calls the functions of the `Console` module,
which are defined in terms of the operations.

## The Console Module

The `Console` module provides the printing functions and several prompts:

```flix
mod Sys.Console {
    /// Prints the string representation of `x` to the standard out.
    def print(x: a): Unit \ Console with ToString[a]

    /// Prints the string representation of `x` to the standard out followed by a new line.
    def println(x: a): Unit \ Console with ToString[a]

    /// Prints the string representation of `x` to the standard err.
    def eprint(x: a): Unit \ Console with ToString[a]

    /// Prints the string representation of `x` to the standard err followed by a new line.
    def eprintln(x: a): Unit \ Console with ToString[a]

    /// Prints prompt `p`, reads a line, and applies `f` to the input.
    /// Prints `msg` and re-prompts on `Err(msg)`. Returns `Some(v)` on `Ok(v)`.
    /// Returns `None` if the end of input has been reached.
    def readlnWith(p: a, f: String -> Result[String, b]): Option[b] \ Console with ToString[a]

    /// Prints prompt `p`, reads a line, and parses it as a value of type `b`.
    /// Prints an error and re-prompts if the input cannot be parsed.
    /// Returns `None` if the end of input has been reached.
    def readlnAs(p: a): Option[b] \ Console with ToString[a], FromString[b]

    /// Prints prompt `p` with a yes/no hint and reads a boolean answer.
    /// Empty input returns `default`. Prints an error and re-prompts on any other
    /// input than "y", "yes", "n", or "no".
    def confirm(p: a, default: {default = Bool}): Bool \ Console with ToString[a]
}
```

Unlike the operations, `print`, `println`, `eprint`, and `eprintln` accept any
value with a `ToString` instance, not just a `String`.

## Basic Console I/O

The simplest use of `Console` is to print a prompt, read input, and respond.
Since `readln` returns `None` at the end of input, the program matches on the
result:

```flix
use Sys.Console

def main(): Unit \ Console =
    Console.print("What is your name? ");
    match Console.readln() {
        case Some(name) => Console.println("Hello ${name}!")
        case None       => Console.println("No name given.")
    }
```

## Confirmed Input

The `Console.confirm` function asks a yes/no question and returns a `Bool`. The
prompt is followed by a `[Y/n]` or `[y/N]` hint that shows the default, which is
used when the user presses Enter without typing anything. Any answer other than
`y`, `yes`, `n`, or `no` (ignoring case) prints an error and re-prompts. At the
end of input the default is returned:

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
`Err(message)` to print the message and re-prompt. The result is `None` if the
end of input is reached before a line passes:

```flix
use Sys.Console

def main(): Unit \ Console =
    let n = Console.readlnWith(
        "Enter a number (1-10): ",
        s -> match Int32.fromString(s) {
            case Some(i) if i >= 1 and i <= 10 => Ok(i)
            case _                             => Err("Please enter a number between 1 and 10.")
        }
    );
    match n {
        case Some(i) => Console.println("You entered: ${i}")
        case None    => Console.println("No number given.")
    }
```

## Parsed Input

The `Console.readlnAs` function prompts for a value of any type with a
`FromString` instance. It trims the line, parses it, and re-prompts until the
line parses. The type to parse is determined by a type annotation or by how the
result is used:

```flix
use Sys.Console

def main(): Unit \ Console =
    let n: Option[Int32] = Console.readlnAs("Enter an integer: ");
    match n {
        case Some(i) => Console.println("${i} squared is ${i * i}.")
        case None    => Console.println("No integer given.")
    }
```

## Writing a Console Handler

Because every function of the module is defined in terms of the five
operations, a handler that implements those operations handles all of them. For
example, a handler can feed scripted input and collect the output, which lets a
program that uses `Console` run without a terminal. The handler below ignores
standard error:

```flix
use Sys.Console

def greet(): Unit \ Console =
    Console.print("What is your name? ");
    match Console.readln() {
        case Some(name) => Console.println("Hello ${name}!")
        case None       => Console.println("No name given.")
    }

def main(): Unit \ IO =
    region rc {
        let sb = StringBuilder.empty(rc);
        run {
            greet()
        } with handler Console {
            def readln(k)           = k(Some("Ada"))
            def write(s, k)         = { StringBuilder.append(s, sb); k() }
            def writeLine(s, k)     = { StringBuilder.appendLine(s, sb); k() }
            def writeErr(_s, k)     = k()
            def writeErrLine(_s, k) = k()
        };
        println(StringBuilder.toString(sb))
    }
```
