## Structs

> **Note:** Requires Flix version 0.51.0

Flix supports mutable _scoped_ structs. A struct is a sequence of user-defined
fields. Fields are immutable by default, but can made mutable by marking them
with the `mut` modifier. 

Like all mutable memory in Flix, every struct must belong to some region.
Structs are the mutable alternative to extensible records which are immutable.

The fields of a struct are unboxed, i.e. primitive types do not cause an extra
layer of indirection. Thus structs are a memory efficient data structure that
can be used to implement higher-level mutable data structures, e.g. mutable
lists, mutable stacks, mutable queues, and so forth. 

Flix supports three operations on structs:

- Creating a struct with `new Struct @ rc { ... }`.
- Accessing the field of a struct with `struct->field`.
- Updating a _mutable_ field of a struct with `struct->field = ...`.

Each operation has an effect in the region of the struct.

An immutable field cannot be updated. 

### Declaring a Struct

We can declare a struct as follows:

```flix
struct Person[r] {
    name: String,
    mut age: Int32,
    mut height: Int32
}
```

Here we declare a struct with three fields: `name`, `age`, and `height`. The
`name` field is immutable, i.e. cannot be changed once a struct instance has
been created. The `age` and `heights` are mutable and can be changed after
creation. The `Person` struct has one type parameter: `r` which specifies the
region that the struct belongs to.

Every struct must have a region type parameter and it must be the last in the
type parameter list. 

### Creating a Struct

We can create an instance of the `Person` struct as follows:

```flix
mod Person {
    pub def mkLuckyLuke(rc: Region[r]): Person[r] \ r =
        new Person @ rc { name = "Lucky Luke", age = 30, height = 185 }
}
```

The `mkPerson` function takes one argument: the region capability `rc` which the
new instance should belong to. The syntax:

```flix
new Person @ rc { name = "Lucky Luke", age = 30, height = 185 }
```

specifies that we create a new instance of the `Person` struct in the region
`rc`. We then specify the values of each field of the struct. All struct fields
must be initialized immediately and explicitly. 

In addition, the fields must be specified in the same order as the declaration
order. 

For example, if we were to write:


```flix
new Person @ rc { age = 30, name = "Lucky Luke", height = 185 }
```

The Flix compiler emits the error:

```
❌ -- Resolution Error -------------------------------------------------- 

>> Struct fields must be initialized in their declaration order

Expected: name, age, height
Actual  : age, name, height

11 |         new Person @ rc { age = 30, name = "Lucky Luke", height = 185 }
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             incorrect order
```

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

### Recursive and Polymorphic Structs

We can define a struct for a binary search tree that is recursive and polymorphic:

```flix
struct Tree[k, v, r] {
    key: k,
    mut value: v,
    mut left: Option[Tree[k, v, r]],
    mut right: Option[Tree[k, v, r]]
}
```

If we assume that `Tree[k, v, r]` is sorted, we can define a `search` function:

```flix
mod Tree {
    pub def search(k: k, t: Tree[k, v, r]): Option[v] \ r with Order[k] = 
        match (k <=> t->key) {
            case Comparison.EqualTo     => Some(t->value)
            case Comparison.LessThan    => 
                // Search left.
                forM(l <- t->left;  result <- search(k, l)) 
                    yield result
            case Comparison.GreaterThan => 
                // Search right.
                forM(r <- t->right; result <- search(k, r)) 
                    yield result
        }
}
```