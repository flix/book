## Next Steps

We are now ready write our first real program! 

We will write a simple variant of the venerable wordcount (`wc`) program from
UNIX. 

We will use the opportunity to illustrate how to use algebraic effects in Flix.

```flix
def wc(file: String): Unit \ {Console, FileReadWithResult} = {
       match FileReadWithResult.readLines(file) {
            case Ok(lines) => 
                let totalLines = List.length(lines);
                let totalWords = List.sumWith(numberOfWords, lines);
                Console.println("Lines: ${totalLines}, Words: ${totalWords}")
        case Err(_) => 
                Console.println("Unable to read file: ${file}")
        }
}

def numberOfWords(s: String): Int32 = 
     s |> String.words |> List.length

def main(): Unit \ IO = 
    run {
        wc("Main.flix")
    } with Console.runWithIO
      with FileReadWithResult.runWithIO

```

The program works as follows:

We define a `wc` function that takes a filename and reads all lines from the
file using the algebraic effect `FileReadWithResult`.

If the file is successfully read, we calculate:

- The number of lines using `List.length`.
- The number of words by summing the results of applying `numberOfWords` to each
  line. 

The results are printed to the terminal using the `Console` algebraic effect.

If the file cannot be read, an error message is printed to the terminal using
the same effect.

The `wc` function's type and effect signature specifies the `{Console,
FileReadWithResult}` effect set, indicating these effects are required.
Conceptually, the function is pure except for these effects, which must be
handled by the caller. 

The `main` function calls `wc` with a fixed filename. Since `wc` uses the
`Console` and `FileReadWithResult` effects, we must provide their
implementations. This is achieved using the `run-with` construct, where we
specify the default handlers `Console.runWithIO` and
`FileReadWithResult.runWithIO`.
