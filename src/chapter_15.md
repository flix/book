# Tips and Tricks

This page documents a few features that make Flix code easier to read and write.

## Main

The entry point of any Flix program is the `main` function which *must* have the
signature:

```flix
def main(): Unit & Impure = ...
```

That is, the main function (i) must return `Unit`, and (ii) must be `Impure`.

