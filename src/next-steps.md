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
                Console.println("Unable to read: ${file}")
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

We define a `wordCount` function that takes a file name. The function reads all
lines from the file using the algebraic effect `FileReadWithResult`.

If the file can be opened and read successfully, we count the number of lines
using `List.length` and we count the number of words by computing the number of
words on each line and summing the result. In particular, we use the
`numberOfWords` helper function to compute how many words are on one line. We
then print the information to the terminal using the `Console` algebraic effect. 

If the file cannot be opened or read we print an error message to the terminal,
again using the `Console` algebraic effect. 

The type and effect signature of the `wordCount` function has the effect set:
`{Console, FileReadWithResult}` since those two effects are used within the
function. We should think of `wordCount` as a _pure_ function modulo these two
effects whose details must be filled in later. 

Lastly, we define the `main` function. In `main` we call the `wordCount`
function fixing the filename. More importantly, since `wordCount` uses the
`Console` and `FileReadWithResult` effects we must supply implementations of
these. We achieve that using the `run-with` construct where we specify the both
`Console` and `FileReadWithResult` should be _handled_ using the default
implementations provided by `Console.runWithIO` and
`FileReadWithResult.runWithIO`. 
