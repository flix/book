## Stratified Negation

Flix supports _stratified negation_ which allow
restricted use of negation in rule bodies.
For example:

```flix
def main(): Unit \ IO =
    let movies = #{
        Movie("The Hateful Eight").
        Movie("Interstellar").
    };
    let actors = #{
        StarringIn("The Hateful Eight", "Samuel L. Jackson").
        StarringIn("The Hateful Eight", "Kurt Russel").
        StarringIn("The Hateful Eight", "Quentin Tarantino").
        StarringIn("Interstellar", "Matthew McConaughey").
        StarringIn("Interstellar", "Anne Hathaway").
    };
    let directors = #{
        DirectedBy("The Hateful Eight", "Quentin Tarantino").
        DirectedBy("Interstellar", "Christopher Nolan").
    };
    let rule = #{
        MovieWithoutDirector(title) :-
            Movie(title),
            DirectedBy(title, name),
            not StarringIn(title, name).
    };
    query movies, actors, directors, rule
        select title from MovieWithoutDirector(title) |> println
```

The program defines three local variables that
contain information about movies, actors, and
directors.
The local variable `rule` contains a rule that
captures all movies where the director does not star
in the movie.
Note the use negation in this rule.
The query returns an array with the string
`"Interstellar"` because Christopher Nolan did not
star in that movie.

> **Note:** Flix enforces that programs are stratified, i.e. a program must not
> have recursive dependencies on which there is use of negation. If there is,
> the Flix compiler rejects the program.
