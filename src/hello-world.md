# Hello World

We can now see the famous _Hello World_ program in `src/Main.flix` file:

```flix
def main(): Unit \ IO = 
    println("Hello World!")
```

That's it!

You will immediately notice a few things are different from other programming
languages: 

- The `main` function has no formal parameters, in particular it does not take
  an arguments array. Instead the command line arguments are available through
  the `Env` effect (see [The Main Function](./main.md)).
- The return type of the `main` function is `Unit`.
- The `main` function has the `IO` effect since it prints to the terminal.
