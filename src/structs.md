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

## Reading and Writing Fields of a Struct

We can read and write fields of a struct using the `->` operator:

```flix
mod Person {
    pub def birthday(person: Person[r]): Unit \ r =
        person->age = person->age + 1;
        if(person->age < 18) {
            person->height = person->height + 10
        } else {
            ()
        }
}
```

Here the `birthday` function takes a `Person` struct and conceptually increases
their age and height. For example, in the line:

```flix
person->age = person->age + 1;
```

We access the current age as `person->age`, increment it, and then store the
result in the `age` field of the same struct. 

> **Note:** It is important to distinguish the struct field access operator `->`
> from the function arrow ` -> `. The difference is that the field access
> operator cannot have space around it, whereas the function arrow must have
> space around it. 

If a field is immutable, it cannot be changed. For example, if we try:

```flix
mod Person {
    pub def changeName(newName: String, person: Person[r]): Unit \ r = 
        person->name = newName
}
```

The Flix compiler emits an error:

```
❌ -- Resolution Error -------------------------------------------------- 

>> Modification of immutable field `Person.name`. 
>> Mark the field as `mut` to allow mutation.

24 |         person->name = newName
                     ^^^^
                     field not marked `mut`
```

We can overcome this issue by marking the field as `mut`.