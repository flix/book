## Associated Types

> **Warning:** Associated types are an experimental feature. 

> **Warning:** Associated types have not yet been released and are only
> available on nightly builds. 

Explain what assoc types are. Explain why they are useful.
Allow a type to depend on the specific data type instance.

We now give an example. We can define a trait for types that can be added: 

```flix
trait Addable[t] {
...
}
```

Now we can define instances that allow us to add ints, floats, strings, etc.

We can also define an instance that allows us to add two sets:

But what if we wanted to add an  element to a set, e.g. `Set#{1, 2} + 3`. 
We cannot do that because the type param is the same everywhere.
Enter associated types.

We add an associated type for the the RHS. 


We can go even further. Mul example.

Another example: A trait for collections:

