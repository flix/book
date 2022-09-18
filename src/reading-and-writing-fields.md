## Reading Object Fields

Reading a field of an object is straightforward:

```flix
import new flix.test.TestClass(): ##flix.test.TestClass \ IO as newObject;
import get flix.test.TestClass.boolField: Bool \ IO as getField;
let o = newObject();
getField(o)
```

Here we assume that `TestClass` is a Java class with
an instance field named `boolField` of type `Bool`.

## Writing Object Fields

Writing a field of an object is also straightforward:

```flix
import new flix.test.TestClass(): ##flix.test.TestClass \ IO as newObject;
import get flix.test.TestClass.boolField: Bool \ IO as getField;
import set flix.test.TestClass.boolField: Unit \ IO as setField;
let o = newObject();
setField(o, false);
getField(o)
```

## Reading and Writing Static Fields

Reading or writing _static_ fields is similar to
reading or writing object fields.
For example:

```flix
import static get java.lang.Integer.MIN_VALUE: Int32 \ IO as getMinValue;
getMinValue()
```

As above, the only difference is to write the
`static` keyword to indicate that the reference is to
a static field.
