## Next Steps

We are now ready write our first real program! 

We will write a simple variant of the venerable wordcount (`wc`) program from
UNIX. We shall not be concerned with efficiency, but we will carefully check all 
error cases. 

Create a new folder (e.g. `wc`) and put the following code into `Main.flix`:

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

The program works as follows:

1. We use `Environment.getArgs()` to get the program arguments. We expect a list
   with at least one element; the name of the file to count lines and words in.
   We use pattern matching on `args` to extract the file name and report an
   error if the list is empty.
2. We use `File.readLines` to read all lines of the file. This operation may
   fail (e.g. if the file does not exist) and hence it returns a `Result`. We use pattern matching on the result and print an error message if we could not read the file.
3. Otherwise we have a `List[String]` from which we can easily compute the
   number of lines and using the helper function `numberOfWords`, we can also
   easily compute the total number of words. Finally, we print these two numbers.

We can compile and run the program as follows:

```shell
$ java -jar flix.jar build    
$ java -jar flix.jar build-jar
$ java -jar wc.jar Main.flix  
Lines: 17, Words: 62
```

The above program gets the job done, but it is a bit verbose. A more readable
version is:

```flix
def main(): Unit \ IO = 
    let args = Environment.getArgs();
    let result = 
        for (
            file  <- List.head(args) |> 
                     Option.toOk("Missing argument: filename");
            lines <- File.readLines(file) |> 
                     Result.mapErr(_ -> "Unable to read: ${file}")
        ) yield {
            let totalLines = List.length(lines);
            let totalWords = List.sumWith(numberOfWords, lines);
            (totalLines, totalWords)
        };
    match result {
        case Ok((lines, words)) => println("Lines: ${lines}, Words: ${words}")
        case Err(message)       => println(message)
    }

def numberOfWords(s: String): Int32 = 
    s |> String.words |> List.length
```

which takes advantages of the [monadic for-yield construct](./monadic-for-yield.md).
