# Next Steps

We are now ready write our first real program! 

We will write a simple variant of the venerable wordcount (`wc`) program from
UNIX. 

We will use the opportunity to illustrate how to use algebraic effects in Flix.

```flix
use Fs.FileRead

def wc(file: String): Unit \ { FileRead, IO } =
    match FileRead.readLines(file) {
        case Ok(lines) =>
            let totalLines = List.length(lines);
            let totalWords = List.sumWith(numberOfWords, lines);
            println("Lines: ${totalLines}, Words: ${totalWords}")
        case Err(_) =>
            println("Unable to read file: ${file}")
    }

def numberOfWords(s: String): Int32 =
     s |> String.words |> List.length

def main(): Unit \ { FileRead, IO } =
    wc("Main.flix")
```

The program works as follows:

We define a `wc` function that takes a filename and reads all lines from the
file using the `FileRead` effect.

If the file is successfully read, we calculate:

- The number of lines using `List.length`.
- The number of words by summing the results of applying `numberOfWords` to each
  line.

The results are printed to the terminal using `println`.

If the file cannot be read, an error message is printed instead.

The `wc` function's type and effect signature specifies the `{FileRead, IO}`
effect set, indicating these effects are required. Both `FileRead` and `IO` have
default handlers, so no explicit handler calls are needed in `main`.
