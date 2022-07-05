# Singleton Enums

An enum with a single case:

```flix
enum USD {
    case USD(Int32)
}
```

can simply be expressed as:

```flix
enum USD(Int32)
```

The same syntax works with type class derivation:

```flix
enum USD with Eq, Order, ToString {
    case USD(Int32)
}
```

can be expressed as:

```flix
enum USD(Int32) with Eq, Order, ToString
```
