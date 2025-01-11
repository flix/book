## Next Steps

We are now ready write our first real program! 

We will write a simple variant of the venerable wordcount (`wc`) program from
UNIX. We will use the opportunity to illustrate how to use algebraic effects in
Flix.

Please follow the following steps:

1. Create a new empty folder (e.g. `wc`)
2. Initialize an empty project in that folder (e.g. `java -jar flix.jar init`)
3. Put the following code into `src/Main.flix`:

```flix
def wordCount(file: String): Unit \ {Console, FileReadWithResult} = {
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
        wordCount("Main.flix")
    } with Console.runWithIO
      with FileReadWithResult.runWithIO

```

The program works as follows:

We define a `wordCount` function that takes a filename and reads all lines from
the file using the algebraic effect `FileReadWithResult`.

If the file is successfully read, we calculate:

- The number of lines using `List.length`.
- The number of words by summing the results of applying the `numberOfWords`
  helper function to each line. This function computes the number of words in a
  given string.

The results are printed to the terminal using the `Console` algebraic effect.

If the file cannot be read, an error message is printed to the terminal using
the same effect.

The `wordCount` function's type and effect signature specifies the `{Console,
FileReadWithResult}` effect set, indicating these effects are required.
Conceptually, the function is pure except for these specified effects, which
must be handled by the caller. 

Finally, the `main` function calls `wordCount` with a fixed filename. Since
`wordCount` uses the `Console` and `FileReadWithResult` effects, we must provide
their implementations. This is achieved using the `run-with` construct, where we
specify the default handlers `Console.runWithIO` and
`FileReadWithResult.runWithIO`.
