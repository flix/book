## Foundational Effects

> **Note:** The following text applies to Flix 0.54.0 or later.

<div style="color:gray">

Flix comes with a small set of built-in *foundational effects*. A foundational
effect, unlike a library or user-defined effect, cannot be re-interpreted or
handled. It simply happens, and when it happens there is no way to get rid of
it. 

More, concretely foundational effects happen when interacting with the outside
world through Java interoperability. 

In Flix, the foundational effects are:

- **Exec**: The `Exec` effect represents the actions required to start (i.e.
  run) a new process outside the JVM. This includes use of `System.exec`, the
  `Process` class, and the `ProcessBuilder` class.
- **FileRead**: The `FileRead` effect represents the actions to required to read
  from the file system.
- **FileWrite**: The `FileWrite` effect represents the actions to required to
  write to the file system.
- **Net**:  The `Net` effect represents the actions required to communicate over
  the network. This includes binding to local ports, DNS resolution, and
  connecting to the outside.
- **NonDet**:  The `NonDet` effect represents one or more non-deterministic actions.
- **Sys**:  The `Sys` effect represents actions that interact with the JVM. This includes use of class loaders, the `Runtime` class, and reflection.
- **IO**: The `IO` effect represents the actions not described by any other effect.

The foundational effects, with the exception of `NonDet`, are all dangerous in
the sense that they provide raw access to the machine. 

For example, with the `FileRead` effect, a program can ready any file on the
file system (and any attached devices). 

The foundational effects are not completely disjoint. For example, using `Exec`
one can start a process that reads files from the file system. Similarly, using
`Sys` one can use reflection to access the file system. 

The `Exec` and `Sys` effects are **incredibly dangerous** and once should be
very suspicious of third-party code that uses them. In contrast, the `NonDet`
effect is completely harmless and the `IO` effect is mostly harmless. Whether
the `FileRead`, `FileWrite`, and `Net` effects are dangerous depends on the
specific application. A `Http` library will probably need the `Net` effect, but
it probably should not have the `FileRead` effect.

### What is the `IO` Effect?

The `IO` effect is a generic catch-all effect that captures any interaction with
the outside which is not captured by the other effects. For example, calling
`System.nanoTime()` has the `IO` effect. 

### Origin of Foundational Effects

Where does foundational effects come from? They come from an analysis of the
Java Standard Library which assignes one or more foundational effects to every
class, constructor, and method. For example, Flix assigns the `Exec` effects to
every constructor and method in the `java.lang.Process`,
`java.lang.ProcessBuilder`, and `java.lang.ProcessHandle` classes. While it can
be argued that no `Exec` effect actually happens __until__
`ProcessBuilder.start` and hence assigning the `Exec` effect to every
constructor and method in `ProcessBuilder` is imprecise, in practice it works
well. 

Now, Flix also provides Flix functions that use Java underneath. Such functions
are not Java constructors or methods, but rather provide a layer on-top-off
Java. These functions also have foundational effects such as `FileRead`,
`FileWrite`, and more. 

### How to Program with Foundational Effects

In general, one should not write Java in Flix. That is to say: one should write
pure programs that may use local mutable state and effects and handlers. But one
should not write programs that mix Java and Flix code. Instead, one should write
a program that calls an effect, and then _the handler of that effect can call
out into Java_. 

We can give an example of this. Imagine that we want to write a guessing game. 

</div>

#### A Guessing Game &mdash; The Wrong Way

Consider the following program written in a mixed style of Flix and Java:

```flix
import java.lang.System
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.{Random => JRandom}

def getSecretNumber(): Int32 \ IO = 
    let rnd = new JRandom();
    rnd.nextInt()

def readGuess(): Result[String, String] \ IO = 
    let reader = new BufferedReader(new InputStreamReader(System.in));
    let line = reader.readLine();
    if (Object.isNull(line)) 
        Result.Err("no input")
    else 
        Result.Ok(line)

def readAndParseGuess(): Result[String, Int32] \ IO = 
    forM(g <- readGuess(); 
         n <- Int32.parse(10, g)
    ) yield n

def gameLoop(secret: Int32): Unit \ IO = {
    println("Enter a guess:");
    match readAndParseGuess() {
        case Result.Ok(g) => 
            if (secret == g) {
                println("Correct!")
            } else {
                println("Incorrect!");
                gameLoop(secret)
            }
        case Result.Err(_) => 
            println("Not a number? Goodbye.");
            println("The secret was: ${secret}")
    }
}

def main(): Unit \ IO = 
    let secret = getSecretNumber();
    gameLoop(secret)

```

The problem is that every function: `getSecretNumber`, `readGuess`,
`readAndParseGuess`, `gameLoop`, and `main` has the `IO` effect. The consequence
is that every function can do anything. Note how the effectful code responsible
for interoperability with Java is scattered all over the program. Understanding,
refactoring, and testing a program written in this style is a nightmare. 

Programming in a style where every function has the `IO` effect is akin to
programming in a style where every function argument and return type has the
`Object` type &mdash; it makes the type (or effect) system useless.

Programming in a programming language with algebraic effects means that we
should define effects for each action or interaction with the outside world. We
should then _handle_ these effects close to the program's boundary. 

#### A Guessing Game &mdash; The Right Way

Here is what we should have done:

```flix
import java.lang.System
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.{Random => JRandom}

eff Guess {
    pub def readGuess(): Result[String, String]
}

eff Secret {
    pub def getSecret(): Int32
}

eff Terminal {
    pub def println(s: String): Unit    
}

def readAndParseGuess(): Result[String, Int32] \ {Guess} = 
    forM(g <- do Guess.readGuess(); 
         n <- Int32.parse(10, g)
    ) yield n

def gameLoop(secret: Int32): Unit \ {Guess, Terminal} = {
    do Terminal.println("Enter a guess:");
    match readAndParseGuess() {
        case Result.Ok(g) => 
            if (secret == g) {
                do Terminal.println("Correct!")
            } else {
                do Terminal.println("Incorrect!");
                gameLoop(secret)
            }
        case Result.Err(_) => 
            do Terminal.println("Not a number? Goodbye.");
            do Terminal.println("The secret was: ${secret}")
    }
}

def main(): Unit \ IO = 
    try {
        let secret = do Secret.getSecret();
        gameLoop(secret)
    } with Secret {
        def getSecret(_, resume) = 
            let rnd = new JRandom();
            resume(rnd.nextInt())
    } with Guess {
        def readGuess(_, resume) = 
            let reader = new BufferedReader(new InputStreamReader(System.in));
            let line = reader.readLine();
            if (Object.isNull(line)) 
                resume(Result.Err("no input"))
            else 
                resume(Result.Ok(line))
    } with Terminal {
        def println(s, resume) = { println(s); resume() }
    }
```

Here, we have introduced three effects: 

1. An effect `Secret` that represents the action of picking a secret number. 
2. An effect `Guess` that represents the action of asking the user for a guess.
3. An effect `Terminal` that represents the action of printing to the console.

We have written each function to use the relevant effects. For example, the
`gameLoop` function uses the `Guess` and `Terminal` effects &mdash; and has no
other effects. Moreover, all effects are now handled in one place: in the `main`
function. The upshot is that the program's core does not have to worry about
interoperability.
