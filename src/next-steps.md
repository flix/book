## Next Steps

We are now ready write our first real program: A simple variant of the venerable
wordcount (`wc`) program from UNIX. We shall not be concerned with efficiency,
but we will carefully handle input, output, and the errors that may occur at
runtime.

Create a new folder and put the following into `Main.flix`:

```flix
def main(): Unit \ IO = 
    let args = Environment.getArgs();
    match args {
        case Nil => println("Missing argument: filename")
        case file :: _ => 
            match File.readLines(file) {
                case Err(_) => 
                    println("Unable to read: ${file}")
                case Ok(lines) => 
                    let totalLines = List.length(lines);
                    let totalWords = List.sumWith(numberOfWords, lines);
                    println("Lines: ${totalLines}, Words: ${totalWords}")
            }
    }

def numberOfWords(s: String): Int32 = 
    s |> String.words |> List.length
```

The program works as follows: First, we retrieve the program arguments (using
`Environment.getArgs()`). We expect this to be a list with one element: the name
of the file to count words in. We use pattern matching to extract the filename
and to print an error if no arguments were specific. Second, we read all lines
in the file (using `File.readLines`). Third, and finally, we compute the total
number of lines and total words in the list of strings we have read. 

We can compile and run this program as follows:

```shell
$ java -jar flix.jar build    
$ java -jar flix.jar build-jar
$ java -jar wc.jar Main.flix  
Lines: 17, Words: 62
```

The above program gets the job done, but it is a bit verbose. 

A slightly more idiomatic Flix program could be:

```flix
def main(): Unit \ IO = 
    let args = Environment.getArgs();
    discard for (
        file  <- List.head(args) |> 
                 Option.toOk("Missing argument: filename");
        lines <- File.readLines(file) |> 
                 Result.mapErr(_ -> "Unable to read: ${file}")
    ) yield {
        let totalLines = List.length(lines);
        let totalWords = List.sumWith(numberOfWords, lines);
        println("Lines: ${totalLines}, Words: ${totalWords}")
    }
```

which uses a few more combinators and the monadic for-yield construct.