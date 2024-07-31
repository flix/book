## Java Collections

Flix has support for conversion from and to Java collections. 

In the following, we use the following import aliases:

```flix
import java.util.{List => JList}
import java.util.{Set => JSet}
import java.util.{Map => JMap}
```

The following functions are available in the
[Adaptor](https://api.flix.dev/Adaptor.html) module: 

### Flix to Java

The following functions _convert_ Flix collections to Java collections:

```flix
///
/// Lists
///
def toList(ma: m[a]): JList \ IO with Foldable[m]
def toArrayList(ma: m[a]): ArrayList \ IO with Foldable[m]
def toLinkedList(ma: m[a]): LinkedList \ IO with Foldable[m]

///
/// Sets
///
def toSet(ma: m[a]): Set \ IO with Order[a], Foldable[m]
def toTreeSet(ma: m[a]): TreeSet \ IO with Order[a], Foldable[m]

///
/// Maps
///
def toMap(m: Map[k, v]): JMap \ IO with Order[k]
def toTreeMap(m: Map[k, v]): TreeMap \ IO with Order[k] 
```

Each function constructs a new collection and copies all its elements into it.
Hence each operation takes at least linear time. The result is a normal Java
collection (which can be modified). 

### Java to Flix

The following functions _convert_ Java collections to Flix collections:

```flix
/// Lists
def fromList(l: JList): List[a]

/// Sets
def fromSet(l: JSet): Set[a] with Order[a]

/// Maps
def fromMap(m: JMap): Map[k, v] with Order[k]
```

Each function constructs a new Flix collection from a Java Collection. Hence
each operation takes at least linear time. Note that for `Set` and `Map`, the
Flix collections use the `Order[a]` instance defined on `a`. This may not be the
same ordering as used by Java. 

> **Warning:** Converting Flix and/or Java collections with primitive values
> requires extra care. In particular, values must be manually boxed or unboxed
> before any conversion.
