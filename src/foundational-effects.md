## Foundational Effects

Flix comes with a small set of built-in *foundational effects*. A foundational
effect, unlike a library or user-defined effect, cannot be re-interpreted or
handled. It simply happens, and when it happens there is no way to get rid of
it. 

More, concretely foundational effects happen when interacting with the outside
world through Java interoperability. 

In Flix, the foundational effects are:

- **Exec**: The `Exec` effect represents the actions required to start (i.e.
  run) a new process outside the JVM. This includes use of `System.exec`, the
  `Process` class, and the `ProcessBuilder` class.
- **FileRead**: The `FileRead` effect represents the actions to required to read
  from the file system.
- **FileWrite**: The `FileWrite` effect represents the actions to required to
  write to the file system.
- **Net**:  The `Net` effect represents the actions required to communicate over
  the network. This includes binding to local ports, DNS resolution, and
  connecting to the outside.
- **NonDet**:  The `NonDet` effect represents one or more non-deterministic actions.
- **Sys**:  The `Sys` effect represents actions that interact with the JVM. This includes use of class loaders, the `Runtime` class, and reflection.
- **IO**: The `IO` effect represents the actions not described by any other effect.

The foundational effects, with the exception of `NonDet`, are all dangerous in
the sense that they provide raw access to the machine. 

For example, with the `FileRead` effect, a program can ready any file on the
file system (and any attached devices). 

The foundational effects are not completely disjoint. For example, using `Exec`
one can start a process that reads files from the file system. Similarly, using
`Sys` one can use reflection to access the file system. 

The `Exec` and `Sys` effects are **incredibly dangerous** and once should be
very suspicious of third-party code that uses them. In contrast, the `NonDet`
effect is completely harmless and the `IO` effect is mostly harmless. Whether
the `FileRead`, `FileWrite`, and `Net` effects are dangerous depends on the
specific application. A `Http` library will probably need the `Net` effect, but
it probably should not have the `FileRead` effect.


