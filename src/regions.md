# Regions

> **Note:** This documentation is relevant for Flix version 0.35.0 or higher.

In Flix, all mutable data belongs to a *region*. 
A region can be thought of a lexical scope. 
Once execution leaves the lexical scope, the region is over, and all mutable data associated with that region is no longer reachable.

Regions are useful because they allow us to implement *pure functions* which internally use *mutation*.

We will illustrate this powerful idea with several real-world examples, but let us first discuss how to use a region:

We introduce a new region scope with the `region` construct:

```
region rh { // region starts.
  ...       // the region handle `rh` is in scope.
}           // region ends and all data associated with rh is no longer in scope.
```

