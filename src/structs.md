## Structs

> **Note:** Requires Flix version 0.51.0

<div style="color:gray">

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

</div>

### Reading and Writing Fields

We can read and write fields of a struct using the `->` operator:

```flix
mod Person {
    pub def birthday(p: Person[r]): Unit \ r =
        p->age = p->age + 1;
        if(p->age < 18) {
            p->height = p->height + 10
        } else {
            ()
        }
}
```

The `birthday` function takes a `Person` struct `p` and mutates its `age` and
`height` fields. 

For example, in the line:

```flix
p->age = p->age + 1;
```

We access the current age as `p->age`, increment it, and store the result back
in the `age` field.

We must distinguish between the _struct field access operator_ `->` and the
function arrow ` -> `. The former has no space around it, whereas the latter
should have space on both sides. In summary:

- `s->f`: a struct field access of field `f` on struct `s`.
- `x -> x`: a function from formal parameter `x` to the variable expression `x`.

#### Field Visibility 

In Flix, the fields of a struct are only visible from within its companion
module. 

For example, if we write:

```flix
struct Point[r] {
    x: Int32,
    y: Int32
}

def area(p: Point[r]): Int32 \ r = 
    p->x * p->y
```

The Flix compiler emits two compilation errors:

```
❌ -- Resolution Error -------------------------------------------------- 

>> Undefined struct field 'x'.

7 |     p->x * p->y
           ^
           undefined field

❌ -- Resolution Error -------------------------------------------------- 

>> Undefined struct field 'y'.

7 |     p->x * p->y
                  ^
                  undefined field
```

Instead, we should define the `area` function inside the companion module:

```flix
struct Point[r] {
    x: Int32,
    y: Int32
}

mod Point { // Companion module for Point
    pub def area(p: Point[r]): Int32 \ r = 
        p->x * p->y
}
```

If we want to provide access to fields of a struct from outside its companion
module, we can introduce getters (and setters). For example: 

```flix
mod Point {
    pub def getX(p: Point[r]): Int32 \ r = p->x
    pub def getY(p: Point[r]): Int32 \ r = p->y
}
```

Thus access to the data of a struct is tightly controlled.

#### Immutable and Mutable Fields

In Flix, every field of a struct is either immutable or mutable. A mutable field
must be marked with the `mut` modifier. Otherwise the field is immutable by
default, i.e. the value of the field cannot be changed once the struct value has
been created. 

For example, we can define a struct to represent a `User`:

```flix
struct User[r] {
    id: Int32,
    mut name: String,
    mut email: String
}
```

Here the identifier `id` is immutable and cannot be changed, whereas the `name`
and `email` fields can be changed over the lifetime of the struct value. 

If we try to modify an immutable field:

```flix
mod User {
    pub def changeId(u: User[r]): Unit \ r =
        u->id = 0
}
```

The Flix compiler emits a compiler error:

```
❌ -- Resolution Error -------------------------------------------------- 

>> Modification of immutable field 'id' on User'.

9 |         u->id = 0
               ^^
               immutable field

Mark the field as 'mut' in the declaration of the struct.
```

We remark that immutability is _not_ transitive. 

For example, we can define a struct:

```flix
struct Book[r] {
    title: String,
    authors: MutList[String, r]
}
```

where the `authors` field is immutable. 

However, since a `MutList` can be changed, we can write:

```flix
mod Book {
    pub def addAuthor(a: String, b: Book[r]): Unit \ r =
        MutList.push!(a, b->authors)
}
```

Here we are not changing the field of the struct. We are changing the underlying
mutable list. 
