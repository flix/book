# Functional Predicates

We sometimes run into a situation where we would like to use a logic predicate,
but not to exhaustively enumerate all of its tuples. 

For example, we can image a situation where we want a predicate
`PrimeInRange(from, to, prime)` which holds if `prime` is a prime number in the
range `[from; to]`. While we can imagine such a predicate, it is not feasible to
compute with. Instead, what we often want, is that we want to treat
`PrimeInRange` as a **functional**, i.e. a function that given `from` and `to`
as _input_ produces a set of primes as _output_. To make matters concrete, we
might want to write the rule:

```flix
R(p) :- P(x), Q(y), PrimeInRange(x, y, p).
```

but without having to evaluate `PrimeInRange` for every `x`, `y`, and `p`.

We can achieve this as follows. We write a function:

```flix
def primesInRange(b: Int32, e: Int32): Vector[Int32] = 
    Vector.range(b, e) |> Vector.filter(isPrime)
```

The key is that `primesInRange` is a _function_ which returns a vector of tuples
(in this case single elements), given a begin `b` and end index `e`. Thus
`primesInRange` can efficiently compute the tuples we are interested in. To use
it in our rule, we write: 

```flix
R(p) :- P(b), Q(e), let p = primesInRange(b, e).
```

where `b` and `e` are clearly identified as the input of `primesInRange` and `p`
as its output. Specifically, Flix requires that `b` and `e` are positively bound
(i.e. bound by a non-negative body atom-- in this case `P` and `Q`.) In this
case, `primesInRanges` returns a vector of `Int32`s, but in general a functional
may return a vector of tuples. 

> **Note:** An important limitation in the current implementation is that the
> variables in the LHS of a functional predicate _must not_ be rebound. That is,
> if the functional predicate is of the form `let (a, b) = f(x, y)` then `a` and
> `b` must not be rebound in the rule. 
