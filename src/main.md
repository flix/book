# The Main Function

The entry point of any Flix program is the `main`
function which _must_ have the signature:

```flix
def main(): Unit \ IO
```

That is, the `main` function

1. must return `Unit`, and
2. must be `Impure` (marked with annotation `\ IO`).

The signature of `main` does not specify any
arguments, but the command line arguments passed to
the program can be accessed by calling
`Environment.getArgs()`.

```flix
def main(): Unit \ IO =
    let args = Environment.getArgs();
    ...
```

Flix requires main to be `Impure`.
If main was pure there would be no reason to run the
program.
Typically the impurity requirement is satisfied
because main prints to the console or has another
side-effect.
