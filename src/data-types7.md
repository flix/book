# Type Aliases

Type aliases introduces a short-hand name for a
type.
For example:

```flix
/// 
/// A type alias for a map from keys of type `k` 
/// to values of type `Result[v, String]`
///
type alias M[k, v] = Map[k, Result[v, String]]

def foo(): M[Bool, Int32] = Map#{true => Ok(123)}
```

A *type alias* does not define a new distinct type.
Rather a type alias is simply a syntactic short-hand
for a (usually complex) type.

The Flix compiler expands type aliases before type
checking.
Consequently, type errors are always reported with
respect to the actual underlying types.

#### Warning

A type alias cannot be recursively defined in terms
of itself.
The Flix compiler will detect and report such
recursive cycles.
