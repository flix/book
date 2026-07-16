# 構造体

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/structs.html)を参照してください。

Flix は、mutable(ミュータブル)で _scoped（スコープ付き）_ な構造体（struct）を
サポートしています。構造体は、ユーザーが定義したフィールドの並びです。
フィールドはデフォルトでは immutable(イミュータブル)ですが、`mut` 修飾子を
付けることで mutable にできます。Flix のすべての mutable なメモリと同様に、
すべての構造体は何らかの region(リージョン)に属していなければなりません。

構造体は、immutable な拡張可能レコード（extensible record）に対する、
mutable な代替手段です。

構造体のフィールドは unboxed（非ボックス化）です。すなわち、プリミティブ型が
間接参照（indirection）を引き起こしません。そのため構造体はメモリ効率の良い
データ構造であり、より高水準な mutable データ構造（たとえば mutable なリスト、
スタック、キューなど）を実装するために利用できます。

Flix は、構造体を扱うために 3 つの操作をサポートしています。

- `new Struct @ rc { ... }` による、region 内での構造体インスタンスの生成。
- `struct->field` による、構造体のフィールドへのアクセス。
- `struct->field = ...` による、_mutable_ なフィールドの更新。

それぞれの操作は、その構造体が属する region において効果（effect）を持ちます。

## 構造体の宣言

構造体は、同じ名前のモジュール——その[コンパニオン](companion-modules.md)——の
内部で宣言します。たとえば：

```flix
mod Person {
    pub struct Person[r] {
        name: String,
        mut age: Int32,
        mut height: Int32
    }
}
```

ここでは、`name`、`age`、`height` という 3 つのフィールドを持つ構造体を
宣言しています。`name` フィールドは immutable であり、構造体インスタンスが
生成された後に変更することはできません。`age` と `height` のフィールドは
mutable なので、生成後に変更できます。`Person` 構造体は、`r` という 1 つの型パラメータを持ち、
これは構造体が属する region を指定します。

すべての構造体は region の型パラメータを持たなければならず、それは型パラメータの
リストの最後になければなりません。

## 構造体の生成

`Person` 構造体のインスタンスは、次のように生成できます。

```flix
mod Person {
    pub def mkLuckyLuke(rc: Region[r]): Person[r] \ r =
        new Person @ rc { name = "Lucky Luke", age = 30, height = 185 }
}
```

`mkLuckyLuke` 関数は、構造体に関連付ける region ケイパビリティ（capability）
`rc` という 1 つの引数を取ります。

次の構文：

```flix
new Person @ rc { name = "Lucky Luke", age = 30, height = 185 }
```

は、構造体 `Person` の新しいインスタンスを region `rc` 内に生成することを
指定します。続いて、構造体の各フィールドの値を指定します。構造体のすべての
フィールドは、即座にかつ明示的に初期化しなければなりません。

## フィールドの読み書き

構造体のフィールドは、フィールドアクセス演算子 `->` を使って読み書きできます。
たとえば：

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

`birthday` 関数は `Person` 構造体 `p` を受け取り、その `age` フィールドと
`height` フィールドを変更（mutate）します。

たとえば、次の行：

```flix
p->age = p->age + 1;
```

では、`p->age` で現在の age を取得し、それをインクリメントして、その結果を
`age` フィールドに書き戻しています。

_構造体のフィールドアクセス演算子_ `->` と、関数の矢印
<code>&nbsp; ->  &nbsp;</code> は区別しなければなりません。前者は前後に
スペースがなく、後者は両側にスペースを置きます。まとめると：

- `s->f`：構造体 `s` のフィールド `f` へのフィールドアクセスです。
- `x -> x`：仮引数 `x` から変数式 `x` への関数です。

### フィールドの可視性

Flix では、構造体のフィールドはそのコンパニオンモジュール（companion module）の
内部からのみ可視です。これは、コンパイラによって強制されるカプセル化
（encapsulation）の一形態と考えることができます。

たとえば、次のように書くと：

```flix
mod Point {
    pub struct Point[r] {
        x: Int32,
        y: Int32
    }
}

def area(p: Point[r]): Int32 \ r = 
    p->x * p->y
```

Flix コンパイラは 2 つのエラーを出力します。

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

代わりに、`area` 関数はコンパニオンモジュールの _内部_ で定義すべきです。

```flix
mod Point {
    pub struct Point[r] {
        x: Int32,
        y: Int32
    }

    pub def area(p: Point[r]): Int32 \ r = 
        p->x * p->y
}
```

構造体のフィールドへのアクセスをコンパニオンモジュールの外部から提供したい
場合は、明示的なゲッター（getter）とセッター（setter）を導入できます。
たとえば：

```flix
mod Point {
    pub def getX(p: Point[r]): Int32 \ r = p->x
    pub def getY(p: Point[r]): Int32 \ r = p->y
}
```

このように、構造体のフィールドへのアクセスは厳密に制御されます。

### immutable なフィールドと mutable なフィールド

Flix では、構造体のすべてのフィールドは immutable か mutable のいずれかです。
mutable なフィールドには `mut` 修飾子を付けなければなりません。そうでない場合、
フィールドはデフォルトで immutable となり、すなわち構造体インスタンスが生成された
後はそのフィールドの値を変更できません。

たとえば、ユーザーを表す構造体を次のように定義できます。

```flix
mod User {
    pub struct User[r] {
        id: Int32,
        mut name: String,
        mut email: String
    }
}
```

ここで識別子 `id` は immutable であり変更できませんが、`name` と `email` の
フィールドは構造体インスタンスの生存期間を通じて変更できます。

immutable なフィールドを変更しようとすると：

```flix
mod User {
    pub def changeId(u: User[r]): Unit \ r =
        u->id = 0
}
```

Flix コンパイラはエラーを出力します。

```
❌ -- Resolution Error -------------------------------------------------- 

>> Modification of immutable field 'id' on User'.

9 |         u->id = 0
               ^^
               immutable field

Mark the field as 'mut' in the declaration of the struct.
```

フィールドの immutability（不変性）は _推移的ではない_ ことに注意してください。

たとえば、次の構造体を定義できます。

```flix
mod Book {
    pub struct Book[r] {
        title: String,
        authors: MutList[String, r]
    }
}
```

ここで `authors` フィールドは immutable です。

しかし、`MutList` は変更できるので、次のように書けます。

```flix
mod Book {
    pub def addAuthor(a: String, b: Book[r]): Unit \ r =
        MutList.push(a, b->authors)
}
```

ここでは、構造体のフィールドを変更しているのではありません。基盤となっている
mutable なリストを変更しているのです。

## 再帰的な構造体と多相的な構造体

再帰的（recursive）かつ多相的（polymorphic）な、二分探索木のための構造体を
定義できます。

```flix
mod Tree {
    pub struct Tree[k, v, r] {
        key: k,
        mut value: v,
        mut left: Option[Tree[k, v, r]],
        mut right: Option[Tree[k, v, r]]
    }
}
```

`Tree[k, v, r]` がソート済みであると仮定すると、`search` 関数を次のように
定義できます。

```flix
mod Tree {
    // 木 `t` から指定されたキー `k` を探索する関数。
    pub def search(k: k, t: Tree[k, v, r]): Option[v] \ r with Order[k] =
        match (Order.compare(k, t->key)) {
            case Comparison.EqualTo  => Some(t->value)
            case Comparison.LessThan =>
                // 左の部分木を探索します。
                match t->left {
                    case None            => None
                    case Some(leftTree)  => search(k, leftTree)
                }
            case Comparison.GreaterThan =>
                // 右の部分木を探索します。
                match t->right {
                    case None            => None
                    case Some(rightTree) => search(k, rightTree)
                }
        }
}
```

<!--
# Structs

Flix supports mutable _scoped_ structs. A struct is a sequence of user-defined
fields. Fields are immutable by default, but can be made mutable by marking them
with the `mut` modifier. Like all mutable memory in Flix, every struct must
belong to some region. 

Structs are the mutable alternative to extensible records which are immutable.

The fields of a struct are unboxed, i.e. primitive types do not cause
indirection. Thus structs are a memory efficient data structure that can be used
to implement higher-level mutable data structures, e.g. mutable lists, mutable
stacks, mutable queues, and so forth. 

Flix supports three operations for working with structs:

- Creating a struct instance in a region with `new Struct @ rc { ... }`.
- Accessing a field of a struct with `struct->field`.
- Updating a _mutable_ field of a struct with `struct->field = ...`.

Each operation has an effect in the region of the struct.

## Declaring a Struct

A struct is declared inside a module of the same name — its
[companion](companion-modules.md). For example:

```flix
mod Person {
    pub struct Person[r] {
        name: String,
        mut age: Int32,
        mut height: Int32
    }
}
```

Here we declare a struct with three fields: `name`, `age`, and `height`. The
`name` field is immutable, i.e. cannot be changed once the struct instance has
been created. The `age` and `height` fields are mutable and hence can be
changed after creation. The `Person` struct has one type parameter: `r` which
specifies the region that the struct belongs to.

Every struct must have a region type parameter and it must be the last in the
type parameter list. 

## Creating a Struct

We can create an instance of the `Person` struct as follows:

```flix
mod Person {
    pub def mkLuckyLuke(rc: Region[r]): Person[r] \ r =
        new Person @ rc { name = "Lucky Luke", age = 30, height = 185 }
}
```

The `mkLuckyLuke` function takes one argument: the region capability `rc` to
associate with the struct.

The syntax:

```flix
new Person @ rc { name = "Lucky Luke", age = 30, height = 185 }
```

specifies that we create a new instance of the `Person` struct in the region
`rc`. We then specify the values of each field of the struct. All struct fields
must be initialized immediately and explicitly. 

## Reading and Writing Fields

We can read and write fields of a struct using the field access operator `->`. For example: 

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

we access the current age as `p->age`, increment it, and store the result back
in the `age` field.

We must distinguish between the _struct field access operator_ `->` and the
function arrow <code>&nbsp; ->  &nbsp;</code>. The former has no space around
it, whereas the latter should have space on both sides. In summary:

- `s->f`: is a struct field access of field `f` on struct `s`.
- `x -> x`: is a function from formal parameter `x` to the variable expression `x`.

### Field Visibility

In Flix, the fields of a struct are only visible from within its companion
module. We can think of this as a form of compiler-enforced encapsulation. 

For example, if we write:

```flix
mod Point {
    pub struct Point[r] {
        x: Int32,
        y: Int32
    }
}

def area(p: Point[r]): Int32 \ r = 
    p->x * p->y
```

The Flix compiler emits two errors:

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

Instead, we should define the `area` function _inside_ the companion module:

```flix
mod Point {
    pub struct Point[r] {
        x: Int32,
        y: Int32
    }

    pub def area(p: Point[r]): Int32 \ r = 
        p->x * p->y
}
```

If we want to provide access to the fields of a struct from outside its companion
module, we can introduce explicit getters and setters. For example: 

```flix
mod Point {
    pub def getX(p: Point[r]): Int32 \ r = p->x
    pub def getY(p: Point[r]): Int32 \ r = p->y
}
```

Thus access to the fields of struct is tightly controlled. 

### Immutable and Mutable Fields

In Flix, every field of a struct is either immutable or mutable. A mutable field
must be marked with the `mut` modifier. Otherwise the field is immutable by
default, i.e. the value of the field cannot be changed once the struct instance has
been created. 

For example, we can define a struct to represent a user:

```flix
mod User {
    pub struct User[r] {
        id: Int32,
        mut name: String,
        mut email: String
    }
}
```

Here the identifier `id` is immutable and cannot be changed whereas the `name`
and `email` fields can be changed over the lifetime of the struct instance. 

If we try to modify an immutable field:

```flix
mod User {
    pub def changeId(u: User[r]): Unit \ r =
        u->id = 0
}
```

The Flix compiler emits an error:

```
❌ -- Resolution Error -------------------------------------------------- 

>> Modification of immutable field 'id' on User'.

9 |         u->id = 0
               ^^
               immutable field

Mark the field as 'mut' in the declaration of the struct.
```

We remark that field immutability is _not_ transitive. 

For example, we can define a struct:

```flix
mod Book {
    pub struct Book[r] {
        title: String,
        authors: MutList[String, r]
    }
}
```

where the `authors` field is immutable. 

However, since a `MutList` can be changed, we can write:

```flix
mod Book {
    pub def addAuthor(a: String, b: Book[r]): Unit \ r =
        MutList.push(a, b->authors)
}
```

Here we are not changing the field of the struct. We are changing the underlying
mutable list. 

## Recursive and Polymorphic Structs

We can define a struct for a binary search tree that is recursive and polymorphic:

```flix
mod Tree {
    pub struct Tree[k, v, r] {
        key: k,
        mut value: v,
        mut left: Option[Tree[k, v, r]],
        mut right: Option[Tree[k, v, r]]
    }
}
```

If we assume that `Tree[k, v, r]` is sorted, we can define a `search` function:

```flix
mod Tree {
    // A function to search the tree `t` for the given key `k`.
    pub def search(k: k, t: Tree[k, v, r]): Option[v] \ r with Order[k] =
        match (Order.compare(k, t->key)) {
            case Comparison.EqualTo  => Some(t->value)
            case Comparison.LessThan =>
                // Search in the left subtree.
                match t->left {
                    case None            => None
                    case Some(leftTree)  => search(k, leftTree)
                }
            case Comparison.GreaterThan =>
                // Search in the right subtree.
                match t->right {
                    case None            => None
                    case Some(rightTree) => search(k, rightTree)
                }
        }
}
```
-->
