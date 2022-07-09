# Function Composition

Flix supports several operators for function
composition and pipelining:

```flix
let f = x -> x + 1;
let g = x -> x * 2;
let h = f >> g;     // equivalent to x -> g(f(x))
```

Here `>>` is forward function composition.

We can also write function applications using the
pipeline operator:

```flix
List.range(1, 100) |>
List.filter(x -> x mod 2 == 0) |>
List.map(x -> x * x) |>
println;
```

Here `x |> f` is equivalent to the function
application `f(x)`.
