# Hello World

We are now ready to write the famous _Hello World_ program in Flix:

```flix
def main(): Unit \ IO = 
    println("Hello World!")
```

That's it!

You will immediately notice a few things are different from other programming
languages: 

- The `main` function has no formal parameters, in particular it does not take
  an arguments array. Instead the command line arguments are available by
  calling `Environment.getArgs`.
- The return type of the `main` function is `Unit`.
- The `main` function has the `IO` effect since it prints to the terminal.
