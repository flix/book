# References

> 💡 **お知らせ**: このドキュメントはAIによって翻訳されています。表現に違和感がある場合は、[原文（英語）](https://doc.flix.dev/references.html)を参照してください。

Flix は可変（mutable）でスコープ付きの参照（reference）をサポートしています。参照とは、その値が時間とともに変化しうるボックスです。参照に対する 3 つの主要な操作は次のとおりです。

- 新しい参照を作成する `Ref.fresh(rc, e)`。
- 参照をデリファレンス（dereference）する `Ref.get(e)`。
- 参照に代入する `Ref.put(e, e)`。

Flix では、参照の型は `Ref[t, r]` であり、`t` は要素の型、`r` はそのリージョンです。Flix のすべての可変メモリと同様に、すべての参照は何らかのリージョンに属していなければなりません。参照に対する読み取りと書き込みは、エフェクトを伴う（effectful）操作です。たとえば、参照 `Ref[t, r]` の値を読み取ると、エフェクト `r` を伴います。

`Ref.fresh(rc, e)` 操作はヒープのリージョン内に参照セルを割り当て、その位置を返します。`Ref.get` 操作はある位置をデリファレンスし、参照セルの内容を返します。そして代入操作 `Ref.put` は参照セルの値を変更します。直感的には、参照セルは、値を変更できる単一のフィールドを持つ「オブジェクト」と考えることができます。

## 参照の割り当て

参照セルは `Ref.fresh(rc, e)` 関数で割り当てます。たとえば次のようになります。

```flix
region rc {
    let c = Ref.fresh(rc, 42);
    println(Ref.get(c))
}
```

ここでは `rc` という名前のリージョンを導入しています。このリージョンの内部で、値 `42` を持つ `c` という参照セルを作成し、それをデリファレンスして出力しています。

## 参照のデリファレンス

参照セルには `Ref.get` 関数でアクセスします（デリファレンスします）。たとえば次のようになります。

```flix
region rc {
    let c = Ref.fresh(rc, 42);
    let x = Ref.get(c);
    let y = Ref.get(c);
    println(x + y)
}
```

ここでは、このプログラムは `42 + 42 = 84` を出力します。

## 代入

参照セルの値を更新することができます。たとえば次のようになります。

```flix
region rc {
    let c = Ref.fresh(rc, 0);
    Ref.put(Ref.get(c) + 1, c);
    Ref.put(Ref.get(c) + 1, c);
    Ref.put(Ref.get(c) + 1, c);
    println(Ref.get(c))
}
```

ここでは、このプログラムは値 `0` を持つ参照セル `c` を作成します。そしてそのセルをデリファレンスし、その値を 3 回インクリメントします。したがって、このプログラムは `3` を出力します。

## 例：シンプルなカウンター

参照を使って、シンプルなカウンターを実装することができます。

```flix
enum Counter[r: Region] { // ここでの Region は型カインド（type-kind）です
    case Counter(Ref[Int32, r])
}

def newCounter(rc: Region[r]): Counter[r] \ r = Counter.Counter(Ref.fresh(rc, 0))

def getCount(c: Counter[r]): Int32 \ r =
    let Counter.Counter(l) = c;
    Ref.get(l)

def increment(c: Counter[r]): Unit \ r =
    let Counter.Counter(l) = c;
    Ref.put(Ref.get(l) + 1, l)

def main(): Unit \ IO =
    region rc {
        let c = newCounter(rc);
        increment(c);
        increment(c);
        increment(c);
        getCount(c) |> println
    }
```

ここでは、`Counter` データ型がリージョンの型パラメータを持っています。これは、カウンターが内部でリージョンを必要とする参照を使用しているため必須です。したがって、`Counter` もスコープ付きとなります。`newCounter` 関数が新しい `Counter` を作成するためにリージョンハンドルを必要とすることに注意してください。さらに、`getCount` 関数と `increment` 関数がともに `r` エフェクトを持つことに注意してください。

## エイリアシングと参照への参照

エイリアシングこそが参照の目的なので、参照は自然にこれをサポートします。たとえば次のようになります。

```flix
region rc {
    let l1 = Ref.fresh(rc, 42);
    let l2 = l1;
    Ref.put(84, l2);
    println(Ref.get(l1))
}
```

これは `84` を出力します。なぜなら、`l1` が指している参照セルが、エイリアス `l2` を通じて変更されるためです。

参照は、次の例が示すように、参照を指すこともできます。

```flix
region rc {
    let l1 = Ref.fresh(rc, 42);
    let l2 = Ref.fresh(rc, l1);
    let rs = Ref.get(Ref.get(l2));
    println(rs)
}
```

ここでは、`l2` の型は `Ref[Ref[Int32, rc], rc]` です。

## 可変なタプルとレコード

Flix のタプルとレコードはイミュータブル（不変）です。しかし、タプルとレコードは可変な参照を含むことができます。

たとえば、次のものは 2 つの可変な参照を含むペアです。

```flix
region rc {
    let p = (Ref.fresh(rc, 1), Ref.fresh(rc, 2));
    Ref.put(123, fst(p))
};
```

このペアの型は `(Ref[Int32, rc], Ref[Int32, rc])` です。この代入はペアそのものを変更するのではなく、第 1 要素にある参照セルの値を変更します。

同様に、次のものは 2 つの可変な参照を含むレコードです。

```flix
region rc {
    let r = { fstName = Ref.fresh(rc, "Lucky"), lstName = Ref.fresh(rc, "Luke") };
    Ref.put("Unlucky", r#fstName)
};
```

このレコードの型は `{ fstName = Ref[String, rc], lstName = Ref[String, rc] }` です。ここでも、この代入はレコードそのものを変更するのではなく、`fstName` ラベルに対応する参照セルの値を変更します。

<!--
# References

Flix supports mutable _scoped_ references. A reference is a box whose value can
change over time. The three key reference operations are:

- Creating a new reference `Ref.fresh(rc, e)`.
- Dereferencing a reference `Ref.get(e)`.
- Assigning to a reference `Ref.put(e, e)`.

In Flix, the type of a reference is `Ref[t, r]` where `t` is the type of the
element and `r` is its region. Like all mutable memory in Flix, every reference
must belong to some region. Reading from and writing to a reference are
_effectful_ operations. For example, reading the value of a reference `Ref[t, r]`
has effect `r`.

The `Ref.fresh(rc, e)` operation allocates a reference cell in a region of the heap
and returns its location, the `Ref.get` operation dereferences a location and
returns the content of a reference cell, and the assignment `Ref.put` operation
changes the value of a reference cell. Informally, a reference cell can be
thought of as an "object" with a single field that can be changed.

## Allocating References

A reference cell is allocated with the `Ref.fresh(rc, e)` function. For example:

```flix
region rc {
    let c = Ref.fresh(rc, 42);
    println(Ref.get(c))
}
```

Here we introduce a region named `rc`. Inside the region, we create a reference
cell called `c` with the value `42` which we then dereference and print.

## Dereferencing References

A reference cell is accessed (dereferenced) with the `Ref.get` function. For example:

```flix
region rc {
    let c = Ref.fresh(rc, 42);
    let x = Ref.get(c);
    let y = Ref.get(c);
    println(x + y)
}
```

Here the program prints `42 + 42 = 84`.

## Assignment

We can update the value of a reference cell. For example:

```flix
region rc {
    let c = Ref.fresh(rc, 0);
    Ref.put(Ref.get(c) + 1, c);
    Ref.put(Ref.get(c) + 1, c);
    Ref.put(Ref.get(c) + 1, c);
    println(Ref.get(c))
}
```

Here the program creates a reference cell `c` with the value `0`. We dereference
the cell and increment its value three times. Hence the program prints `3`.

## Example: A Simple Counter

We can use references to implement a simple counter:

```flix
enum Counter[r: Region] { // The Region here is a type-kind
    case Counter(Ref[Int32, r])
}

def newCounter(rc: Region[r]): Counter[r] \ r = Counter.Counter(Ref.fresh(rc, 0))

def getCount(c: Counter[r]): Int32 \ r =
    let Counter.Counter(l) = c;
    Ref.get(l)

def increment(c: Counter[r]): Unit \ r =
    let Counter.Counter(l) = c;
    Ref.put(Ref.get(l) + 1, l)

def main(): Unit \ IO =
    region rc {
        let c = newCounter(rc);
        increment(c);
        increment(c);
        increment(c);
        getCount(c) |> println
    }
```

Here the `Counter` data type has a region type parameter. This is required since
the counter internally uses a reference that requires a region. Hence `Counter`s
are also scoped. Note that the `newCounter` function requires a region handle to
create a new `Counter`. Moreover, note that the functions `getCount` and
`increment` both have the `r` effect.

## Aliasing and References to References

References naturally support aliasing since that is their purpose. For example:

```flix
region rc {
    let l1 = Ref.fresh(rc, 42);
    let l2 = l1;
    Ref.put(84, l2);
    println(Ref.get(l1))
}
```

Prints `84` because the reference cell that `l1` points to is modified through
the alias `l2`.

References can also point to references as the following example illustrates:

```flix
region rc {
    let l1 = Ref.fresh(rc, 42);
    let l2 = Ref.fresh(rc, l1);
    let rs = Ref.get(Ref.get(l2));
    println(rs)
}
```

Here the type of `l2` is `Ref[Ref[Int32, rc], rc]`.

## Mutable Tuples and Records

Flix tuples and records are _immutable_. However, tuples and records may contain
mutable references.

For example, here is a pair that contains two mutable references:

```flix
region rc {
    let p = (Ref.fresh(rc, 1), Ref.fresh(rc, 2));
    Ref.put(123, fst(p))
};
```

The type of the pair is `(Ref[Int32, rc], Ref[Int32, rc])`. The assignment does
not change the pair but instead changes the value of the reference cell in the
first component.

Similarly, here is a record that contains two mutable references:

```flix
region rc {
    let r = { fstName = Ref.fresh(rc, "Lucky"), lstName = Ref.fresh(rc, "Luke") };
    Ref.put("Unlucky", r#fstName)
};
```

The type of the record is `{ fstName = Ref[String, rc], lstName = Ref[String, rc] }`.
Again, the assignment does not change the record, but instead changes
the value of the reference cell corresponding to the `fstName` label.
-->
