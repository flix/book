# Frequently Asked Questions

## Does Flix supports constants?

Yes and no. Flix does not support top-level constants. You can, however, declare
a pure function which takes zero arguments:

```flix
def pi(): Float64 = 3.14f64
```

The Flix compiler will inline such constants. 

If you have an expensive computation that you want to perform once, you should
compute it where needed and explicitly pass it around. Flix does not support
top-level constants because they violate the principle that no code should be
executed before main.
