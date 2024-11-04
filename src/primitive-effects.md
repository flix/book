## Primitive Effects

> **Note:** The following text applies to Flix 0.54.0 or later.

Flix comes with a collection of pre-defined primitive effects. Unlike algebraic
and heap effects, primitive effects cannot be handled and never go out of scope.
A primitive effect represents a side-effect that happens on the machine. It
cannot be undone or reinterpreted.

The most important primitive effect is the `IO` effect.

### The `IO` Effect

The `IO` effect represents any action that interacts with the world outside the
program. Such actions include printing to the console, creating, reading, and
writing files, accessing the network, and more. The `IO` represents actions that
_change_ the outside world (e.g., modifying a file) but also actions that merely
_access_ the outside world (e.g., retrieving the current time). Unlike a pure
function, a function with the `IO` effect may change behavior every time it is
called, even if its arguments are the same. For example, reading the same file
twice is not guaranteed to return the same result since the file may have
changed between the two accesses.

The `IO` effect, and all other primitive effects, are _viral_. If a function has
a primitive effect, all its callers will also have that primitive effect. That
is to say, once you have tainted yourself with impurity, you remain tainted. 

### The Other Primitive Effects

In addition to the all-important `IO` effect, Flix has a small collection of
pre-defined primitive effects. The point of these primitive effects is to
provide more information about the specific actions a function can take. Except
for the `NonDet` effect, all of effects below always come together with the `IO`
effect. 

- **Env**: The `Env` effect represents actions that involve access to
  information about the environment, including information from the operating
  system (e.g., the name of the current user, the current working directory, and
  so on), as well as information about the hardware (e.g., the number of
  processors in the machine, the total amount of memory, and so on).

- **Exec**: The `Exec` effect represents actions that involve process creation
  (i.e., spawning new processes that run outside the JVM), including using
  `System.exec`, the `Process` and `ProcessBuilder` classes, and dynamic library
  loading.

- **FileRead**: The `FileRead` effect represents actions that read from the file
  system &mdash; for example, reading a file, reading its meta-data, or listing
  the contents of a directory.

- **FileWrite**: The `FileWrite` effect represents actions that write to the
  file system &mdash; for example, creating a file, writing a file, or deleting
  a file.

- **Net**:  The `Net` effect represents actions that involve network access
  &mdash; for example, binding to a local port, connecting to a remote socket,
  or DNS resolution.

- **NonDet**: The `NonDet` effect represents an almost pure computation. For
  example, a function that flips a coin is virtually pure; it has no
  side-effects. Yet, it may return different results, even when given the same
  arguments.

- **Sys**: The `Sys` effect represents actions that interact with the JVM
  &mdash; for example, using the `Runtime` and `System` classes, class loaders,
  or reflection.

All of the above effects, except for the `NonDet` effect, always occur together
with the `IO` effect. In particular, they capture a more precise aspect of the
`IO` effect. For example, from a security point-of-view, it seems reasonable
that a web server library should have the `FileRead` and `Net` work effects, but
it would be worrying if it had the `FileWrite` and `Sys` effects. As another
example, it seems reasonable that a logging library would have the `FileWrite`
effect, but it would be a cause for concern if it also had the `Exec` and `Net`
effects.

The above effects represent dangerous actions except for `IO`, `Env`, and
`NonDet`, which are relatively harmless. `Exec` allows arbitrary process
execution, `FileRead` can be used to access sensitive data, `FileWrite` can be
used to trash the filesystem, `Net` can be used to exfiltrate data, and `Sys`
via reflection allows access to all of the previous. We should always be
suspicious if unknown or untrusted code uses any of these effects. 

The primitive effects are mostly disjoint, but not entirely. For example, we can
use the `Exec` effect to indirectly gain access to the file system. The
`FileRead` effect may allow us to access a mounted network drive, a form of
network access. Ultimately, whether one effect can emulate another depends on
what side channels the underlying operating system allows. The point of the
effect system is that if a function does not have the `FileWrite` effect, it
cannot write to the file system using the ordinary file APIs available on the
JVM. 

### Where do Primitive Effects Come From?

The Flix compiler ships with a built-in database that maps classes,
constructors, and methods in the Java Class Library to primitive effects. For
example, the database assigns the `Exec` effects to every constructor and method
in the `java.lang.Process`, `java.lang.ProcessBuilder`, and
`java.lang.ProcessHandle` classes. 
