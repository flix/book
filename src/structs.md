## Structs

> **Note:** Requires Flix version 0.51.0

Flix supports mutable _scoped_ structs. In Flix, like for arrays, every struct
must have an associated region. Flix supports three operations on structs:

- Creating a struct with `new Struct @ rc { ... }`.
- Accessing the field of a struct with `struct->field`.
- Updating a mutable field of a struct with `struct-> field = ...`.

Each operation has an effect in the region associated with the struct.

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

### Reading and Writing Fields of a Struct

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

#### Field Visibility 

The fields of a struct are only visible within the companion module of the
struct. Hence in the above example, all our functions where placed within the
`Person` companion module. If we try to access a struct field outside the module, e.g. with:

```flix
def getName(p: Person[r]): String \ r = 
    p->name 
```

The Flix compiler emits an error:

```flix
❌ -- Resolution Error -------------------------------------------------- 

>> Undefined struct field 'name'.

37 |     p->name 
            ^^^^
            undefined field
```

If we want to provide access to struct fields outside of its companion module
then we can define explicit getters and setters. For example, we could take the
`getName` function from above, and place it into the companion module: 

```flix
mod Person {
    /// A getter function which provides access to the name field.
    def getName(p: Person[r]): String \ r = 
        p->name 
}
```

#### Immutable Fields

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