## Effect-Oriented Programming

Programming with effects requires a new mindset, _an effect-oriented mindset_.

Imagine a programmer coming from JavaScript or Python to a statically-typed
programming language such as C# or Java. If they continue to program with
objects, maps, and strings without introducing their own types, then the
benefits of a static type system are lost. In the same way, if a programmer
comes to Flix without adapting _an effect-oriented mindset_ then the benefits of
the Flix type and effect system are lost.

In Flix, we can give every function the `IO` effect and call effectful code
everywhere, but this is not effect-oriented programming and is a bad programming
style. A proper effect-oriented program architecture consists of a functional
core, which may use [algebraic effects and handlers](./effects-and-handlers.md),
surrounded by an imperative shell that performs `IO`. A good rule of thumb is
that `IO` effect should be _close_ to the `main` function.

We now illustrate these points with an example.

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

Here every function, i.e. `getSecretNumber`, `readGuess`, `readAndParseGuess`,
`gameLoop`, and `main` has the `IO` effect. The consequence is that every
function can do anything. Note how effectful code is scattered everywhere
throughout the program. 

Understanding, refactoring, and testing a program written in this style is a
nightmare. 

Programming in a effect-oriented style means that we should define effects for
every action that interacts with the outside world. We should then _handle_
these effects close to the `main` function.

#### A Guessing Game &mdash; The Right Way

Here is what we should have done:

```flix
import java.lang.System
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.{Random => JRandom}

eff Guess {
    def readGuess(): Result[String, String]
}

eff Secret {
    def getSecret(): Int32
}

eff Terminal {
    def println(s: String): Unit    
}

def readAndParseGuess(): Result[String, Int32] \ {Guess} = 
    forM(g <- Guess.readGuess(); 
         n <- Int32.parse(10, g)
    ) yield n

def gameLoop(secret: Int32): Unit \ {Guess, Terminal} = {
    Terminal.println("Enter a guess:");
    match readAndParseGuess() {
        case Result.Ok(g) => 
            if (secret == g) {
                Terminal.println("Correct!")
            } else {
                Terminal.println("Incorrect!");
                gameLoop(secret)
            }
        case Result.Err(_) => 
            Terminal.println("Not a number? Goodbye.");
            Terminal.println("The secret was: ${secret}")
    }
}

def main(): Unit \ IO = 
    run {
        let secret = Secret.getSecret();
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
    } with handler Terminal {
        def println(s, resume) = { println(s); resume() }
    }
```

Here, we have introduced three algebraic effects: 

1. A `Guess` effect that represents the action of asking the user for a guess.
2. A `Secret` effect that represents the action of picking a secret number. 
3. A `Terminal` effect that represents the action of printing to the console.

We have written each function to only use the relevant effects. For example, the
`gameLoop` function uses the `Guess` and `Terminal` effects &mdash; and has no
other effects. Furthermore, all effects are now handled in one place: in the
`main` function. The upshot is that the business is logic is purely functional.
Where impurity is needed, it is precisely encapsulated by the use of effects and
handlers.
