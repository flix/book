# The Main Function

The entry point of any Flix program is the `main` function which must take zero
arguments and return `Unit`:

```flix
def main(): Unit \ IO =
    println("Hello World!")
```

## Effects of Main

The `main` function can use any combination of:

- **Primitive effects:** `IO` and `NonDet`.
- **Any effect with a default handler:** for example `Env`, `Exit`, `Clock`,
  `Logger`, and others.

Effects with default handlers are automatically translated into `IO` by the Flix
compiler. See [Default Handlers](./default-handlers.md) for details.

For example, main can use the `Env` and `Exit` effects:

```flix
def main(): Unit \ {Env, Exit} =
    let args = Env.getArgs();
    match List.head(args) {
        case None    =>
            println("Missing argument.");
            Exit.exit(1)
        case Some(a) =>
            println("Hello ${a}!")
    }
```

## Accessing Command Line Arguments

The command line arguments passed to the program can be accessed by calling
`Env.getArgs()` through the `Env` effect:

```flix
def main(): Unit \ {Env, IO} =
    let args = Env.getArgs();
    println("Arguments: ${args}")
```

## Exiting the Program

The program can be terminated with a specific exit code using `Exit.exit`:

```flix
def main(): Unit \ Exit =
    Exit.exit(0)
```

## Why Must Main Be Effectful?

Flix requires `main` to be effectful. If `main` was pure there would be no
reason to run the program. Typically this requirement is satisfied because `main`
prints to the console or has another side-effect.
