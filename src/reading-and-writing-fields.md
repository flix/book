## Reading and Writing Fields

We can read and write fields by importing functions that serve as "getters" and "setters".

Assume we have the Java class:

```java
class TestClass {
    boolean boolField = true;
}
```

Then here is how we can access the `boolField`:

```flix
import java_new flix.test.TestClass(): ##flix.test.TestClass \ IO as newObject;
import java_get_field flix.test.TestClass.boolField: Bool \ IO as getField;
let o = newObject();
getField(o)
```

Here we import the (default, empty) constructor of `TestClass` as `newObject`.
Next, we import the field `boolField` as the function `getField`. We use
`newObject` to construct a fresh object and we call `getField` on it to
obtain the value of `o.boolField`.

Writing a field of an object is similar:

```flix
import java_new flix.test.TestClass(): ##flix.test.TestClass \ IO as newObject;
import java_get_field flix.test.TestClass.boolField: Bool \ IO as getField;
import set flix.test.TestClass.boolField: Unit \ IO as setField;
let o = newObject();
setField(o, false);
getField(o)
```

Here we import both a "getter" and "setter" for the `boolField` field.

### Reading and Writing Static Fields

Reading or writing _static_ fields is similar to
reading or writing object fields.
For example:

```flix
import static java_get_field java.lang.Integer.MIN_VALUE: Int32 \ IO as getMinValue;
getMinValue()
```

The only difference is to write the
`static` keyword to indicate that the reference is to
a static field.
