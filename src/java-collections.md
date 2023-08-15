## Java Collections

Flix has support for conversion to and from Java collections. 

### Flix to Java

The following functions _convert_ Flix collections to Java collections:

```flix
///
/// Lists
///
def toList(ma: m[a]): ##java.util.List \ IO with Foldable[m]
def toArrayList(ma: m[a]): ##java.util.ArrayList \ IO with Foldable[m]
def toLinkedList(ma: m[a]): ##java.util.LinkedList \ IO with Foldable[m]

///
/// Sets
///
def toSet(ma: m[a]): ##java.util.Set \ IO with Order[a], Foldable[m]
def toTreeSet(ma: m[a]): ##java.util.TreeSet \ IO with Order[a], Foldable[m]

///
/// Maps
///
def toMap(m: Map[k, v]): ##java.util.Map \ IO with Order[k]
def toTreeMap(m: Map[k, v]): ##java.util.TreeMap \ IO with Order[k] 
```

Each function constructs a new collection and copies all its elements into it.
Hence each operation takes at least linear time. The upshot is that the result
is a normal Java collection (which can be modified). 

### Java to Flix

The following functions _convert_ Java collections to Flix collections:

```flix
/// Lists
def fromList(l: ##java.util.List): List[a]

/// Sets
def fromSet(l: ##java.util.Set): Set[a] with Order[a]

/// Maps
def fromMap(m: ##java.util.Map): Map[k, v] with Order[k]
```

Each function constructs a new Flix collection from a Java Collection. Hence
each operation takes at least linear time. Note that for `Set` and `Map`, the
Flix collections use the `Order[a]` instance defined on `a`. This may not be the
same ordering as used by Java. Thus one has to be careful.

### Wrapping Flix Collections

TBD.

### Primitive Values

**Warning:** Converting Flix and/or Java collections with primitive values
requires extra care. In particular, values must be manually boxed or unboxed
before any conversion.