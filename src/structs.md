## Structs

> **Note:** Requires Flix version 0.51.0

Flix supports mutable _scoped_ structs. 

In Flix, like for arrays, every struct must have an associated region.

### Defining a Struct

We can define a struct as follows:

```flix
struct Person[r] {
    name: String,
    mut age: Int32,
    mut height: Int32
}
```

We see several notable things: First, every struct must have a region type
parameter. Second, a struct consists of a collection of fields. Third, fields
can be immutable, which is the default, or mutable which must be indicated by
using the `mut` modifier. 

> **Note:** The fields of a struct are only visible within the companion module
of the struct. 

### Creating a Struct

We can create an instance of the `Person` struct as follows:

```flix
mod Person {
    pub def mkPerson(rc: Region[r], name: String): Person[r] \ r =
        new Person @ rc { name = name, age = 0, height = 30 }
}
```

The `mkPerson` function takes two arguments: a region capability `rc` and the
`name` of the person. The syntax:

```flix
new Person @ rc { name = name, age = 0, height = 30 }
```

creates an instance of the struct `Person` in the region specified by `rc` with
the values of the fields as specified. Note that the fields must be specified in
the same order as they were in the declaration of the struct. If we specify the
wrong order: 

```flix
new Person @ rc { height = 30, age = 0, name = name }
```

The Flix compiler emits an error:

```
❌ -- Resolution Error -------------------------------------------------- 

>> Structs fields must be initialized in their declaration order

Expected Order: name, age, height
Actual Order:   height, age, name

11 |         new Person @ rc { height = 30, age = 0, name = name }
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             incorrect order
```

## Reading Fields of a Struct

We can read the fields of a struct using the `->` operator:

