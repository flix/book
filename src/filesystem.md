# FileSystem

Flix provides a family of effects for filesystem operations. The key modules
are:

- `Fs.FileSystem` — the unified `FileSystem` effect (all 29 operations)
- `Fs.FileRead` — the `FileRead` effect (read, readLines, readBytes)
- `Fs.FileWrite` — the `FileWrite` effect (write, append, delete, copy, move, mkdir, etc.)
- `Fs.FileStat` — the `FileStat` effect (exists, type tests, permissions, timestamps, size)
- `Fs.DirList` — the `DirList` effect (listing directory contents)
- `Fs.Glob` — the `Glob` effect (finding files by pattern)
- `Fs.Size` — utilities for working with file sizes

All effects have default handlers, so no explicit `runWithIO` call is needed in
`main`.

There are also more fine-grained leaf effects (e.g. `FileExists`,
`ReadFile`, `WriteFile`) that do not have default handlers but can be run into
their parent effects using `runWith` handlers. See [The Effect
Hierarchy](#the-effect-hierarchy) for details.

## Reading a File

We can use `FileRead.read` to read an entire file as a string:

```flix
use Fs.FileRead

def main(): Unit \ { FileRead, IO } =
    match FileRead.read("example.txt") {
        case Ok(content) => println(content)
        case Err(err)    => println("Error: ${err}")
    }
```

All filesystem operations return `Result[IoError, ...]`. The `IoError` type is
a pair of an `ErrorKind` and a message string. The `ErrorKind` enum tells us
what went wrong:

| ErrorKind               | Description                                      |
|--------------------------|--------------------------------------------------|
| `NotFound`               | The file or directory was not found.             |
| `AlreadyExists`          | The file or directory already exists.             |
| `PermissionDenied`       | Access was denied (also used by middleware).      |
| `InvalidPath`            | The path is malformed.                           |
| ...                      | and others.                                      |

> **Note:** The `IO` effect appears in the signature because of `println`.

## Writing a File

We can use `FileWrite.write` to write a string to a file:

```flix
use Fs.FileWrite

def main(): Unit \ { FileWrite, IO } =
    match FileWrite.write(str = "Hello, Flix!", "greeting.txt") {
        case Ok(_)    => println("File written successfully.")
        case Err(err) => println("Error: ${err}")
    }
```

## Reading and Writing Lines

We can use `readLines` and `writeLines` to work with files line by line:

```flix
use Fs.FileRead
use Fs.FileWrite

def main(): Unit \ { FileRead, FileWrite, IO } =
    match FileWrite.writeLines(lines = List#{"Line 1", "Line 2", "Line 3"}, "data.txt") {
        case Err(err) => println("Write error: ${err}")
        case Ok(_) =>
            match FileRead.readLines("data.txt") {
                case Ok(lines) =>
                    foreach (line <- lines) {
                        println(line)
                    }
                case Err(err) => println("Read error: ${err}")
            }
    }
```

> **Note:** Since we both read and write, the effect set includes `FileRead`,
> `FileWrite`, and `IO`.

## Reading and Writing Bytes

We can use `readBytes` and `writeBytes` for binary data:

```flix
use Fs.FileRead
use Fs.FileWrite

def main(): Unit \ { FileRead, FileWrite, IO } =
    let data = Vector#{72i8, 101i8, 108i8, 108i8, 111i8};
    match FileWrite.writeBytes(data, "binary.dat") {
        case Err(err) => println("Write error: ${err}")
        case Ok(_) =>
            match FileRead.readBytes("binary.dat") {
                case Ok(bytes) =>
                    println("Read ${Vector.length(bytes)} bytes.");
                    println("As string: ${String.fromBytes(bytes)}")
                case Err(err) => println("Read error: ${err}")
            }
    }
```

## Appending to a File

We can use `append` to add text to an existing file without overwriting it. The
file is created if it does not exist:

```flix
use Fs.FileRead
use Fs.FileWrite

def main(): Unit \ { FileRead, FileWrite, IO } =
    match FileWrite.write(str = "Line 1\n", "log.txt") {
        case Err(err) => println("Write error: ${err}")
        case Ok(_) =>
            match FileWrite.append(str = "Line 2\n", "log.txt") {
                case Err(err) => println("Append error: ${err}")
                case Ok(_) =>
                    match FileRead.read("log.txt") {
                        case Ok(content) => println(content)
                        case Err(err)    => println("Read error: ${err}")
                    }
            }
    }
```

There are also `appendLines` and `appendBytes` variants.

## Listing a Directory

We can use `DirList.list` to get the names of all files and directories in a
directory:

```flix
use Fs.DirList

def main(): Unit \ { DirList, IO } =
    match DirList.list(".") {
        case Ok(entries) =>
            foreach (entry <- entries) {
                println(entry)
            }
        case Err(err) => println("Error: ${err}")
    }
```

## Finding Files with Glob

We can use `Glob.glob` to find files matching a glob pattern under a base
directory:

```flix
use Fs.Glob

def main(): Unit \ { Glob, IO } =
    match Glob.glob(".", "*.flix") {
        case Ok(files) =>
            foreach (file <- files) {
                println(file)
            }
        case Err(err) => println("Error: ${err}")
    }
```

## File Metadata

We can use the `FileStat` effect to inspect file metadata: existence, type,
size, permissions, and timestamps:

```flix
use Fs.FileStat
use Fs.FileWrite

def main(): Unit \ { FileStat, FileWrite, IO } =
    let file = "example.txt";
    match FileWrite.write(str = "Hello!", file) {
        case Err(err) => println("Write error: ${err}")
        case Ok(_) =>
            match FileStat.exists(file) {
                case Ok(b)    => println("Exists: ${b}")
                case Err(err) => println("Error: ${err}")
            };
            match FileStat.isRegularFile(file) {
                case Ok(b)    => println("Is regular file: ${b}")
                case Err(err) => println("Error: ${err}")
            };
            match FileStat.isDirectory(file) {
                case Ok(b)    => println("Is directory: ${b}")
                case Err(err) => println("Error: ${err}")
            };
            match FileStat.size(file) {
                case Ok(s)    => println("Size: ${s}")
                case Err(err) => println("Error: ${err}")
            };
            match FileStat.modificationTime(file) {
                case Ok(t)    => println("Modification time: ${t}ms")
                case Err(err) => println("Error: ${err}")
            }
    }
```

The `FileStat` effect combines four sub-effects:

| Sub-effect       | Operations                                             |
|------------------|--------------------------------------------------------|
| `FileTest`       | `exists`, `isDirectory`, `isRegularFile`, `isSymbolicLink` |
| `FilePermission` | `isReadable`, `isWritable`, `isExecutable`             |
| `FileTime`       | `accessTime`, `creationTime`, `modificationTime`       |
| `FileSize`       | `size`                                                 |

## Copying, Moving, and Deleting

We can also use the `FileWrite` effect to copy, move, and delete files:

```flix
use Fs.FileWrite

def main(): Unit \ { FileWrite, IO } =
    match FileWrite.write(str = "Hello!", "original.txt") {
        case Err(err) => println("Write error: ${err}")
        case Ok(_) =>
            // Copy with no options.
            match FileWrite.copy(src = "original.txt", "copy.txt") {
                case Ok(_)    => println("Copied.")
                case Err(err) => println("Copy error: ${err}")
            };
            // Move (rename) with no options.
            match FileWrite.move(src = "copy.txt", "renamed.txt") {
                case Ok(_)    => println("Moved.")
                case Err(err) => println("Move error: ${err}")
            };
            // Delete.
            match FileWrite.delete("renamed.txt") {
                case Ok(_)    => println("Deleted.")
                case Err(err) => println("Delete error: ${err}")
            }
    }
```

The `copy` and `move` functions are convenience wrappers around `copyWith` and
`moveWith`, which accept option sets:

- `CopyOption.CopyAttributes` — preserve file attributes
- `CopyOption.ReplaceExisting` — overwrite the destination if it exists
- `MoveOption.AtomicMove` — perform an atomic rename
- `MoveOption.ReplaceExisting` — overwrite the destination if it exists

## Creating Directories

We can use `mkDir` to create a single directory, `mkDirs` to create a directory
and all its parents, and `mkTempDir` to create a temporary directory:

```flix
use Fs.FileWrite

def main(): Unit \ { FileWrite, IO } =
    match FileWrite.mkDirs("a/b/c") {
        case Ok(_)    => println("Created a/b/c.")
        case Err(err) => println("Error: ${err}")
    };
    match FileWrite.mkTempDir("flix-") {
        case Ok(path) => println("Temp dir: ${path}")
        case Err(err) => println("Error: ${err}")
    }
```

## The FileSystem Effect

The `FileSystem` effect combines all filesystem operations into a single
effect. It includes all operations from `FileStat`, `FileRead`, `FileWrite`,
`DirList`, and `Glob`. We can use `FileSystem` when we need multiple categories
of operations together:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    match FileSystem.write(str = "Hello!", "greeting.txt") {
        case Err(err) => println("Write error: ${err}")
        case Ok(_) =>
            match FileSystem.read("greeting.txt") {
                case Ok(content) => println("Read: ${content}")
                case Err(err)    => println("Read error: ${err}")
            }
    }
```

## Middleware

Middleware are effect handlers that intercept filesystem operations. We apply
them using `run { ... } with FileSystem.<middleware>` (or the corresponding
sub-effect module) and compose them by stacking multiple `with` clauses.

### Base Directory

`withBaseDir` resolves relative paths against a base directory. Absolute paths
pass through unchanged:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    match FileSystem.mkDirs("/tmp/flix-basedir") {
        case Err(err) => println("Setup error: ${err}")
        case Ok(_) =>
            run {
                match FileSystem.write(str = "Hello", "greeting.txt") {
                    case Err(err) => println("Write error: ${err}")
                    case Ok(_) =>
                        match FileSystem.read("greeting.txt") {
                            case Ok(content) => println("Read: ${content}")
                            case Err(err)    => println("Read error: ${err}")
                        }
                }
            } with FileSystem.withBaseDir("/tmp/flix-basedir")
    }
```

### Chroot

`withChroot` restricts all operations to a directory subtree. Operations
targeting paths outside the chroot fail with a `PermissionDenied` error:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    match FileSystem.mkDirs("/tmp/flix-chroot") {
        case Err(err) => println("Setup error: ${err}")
        case Ok(_) =>
            run {
                match FileSystem.write(str = "Hello", "/tmp/flix-chroot/data.txt") {
                    case Ok(_)    => println("Write inside chroot succeeded")
                    case Err(err) => println("Error: ${err}")
                };
                match FileSystem.read("/etc/hostname") {
                    case Ok(_)    => println("Unexpected: read outside chroot succeeded")
                    case Err(err) => println("Read outside chroot blocked: ${err}")
                }
            } with FileSystem.withChroot("/tmp/flix-chroot")
    }
```

### Logging

`withLogging` logs each filesystem operation via the `Logger` effect. Note
that `Logger` appears in the type signature of `main`:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, Logger, IO } =
    run {
        match FileSystem.write(str = "Hello, Flix!", "greeting.txt") {
            case Err(err) => println("Write error: ${err}")
            case Ok(_) =>
                match FileSystem.read("greeting.txt") {
                    case Ok(content) => println(content)
                    case Err(err)    => println("Read error: ${err}")
                }
        }
    } with FileSystem.withLogging
```

### Read-Only

`withReadOnly` blocks all write operations with a `PermissionDenied` error.
Read and stat operations pass through normally:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    run {
        match FileSystem.write(str = "This will fail", "blocked.txt") {
            case Ok(_)    => println("Unexpected: write succeeded")
            case Err(err) => println("Write blocked: ${err}")
        };
        match FileSystem.exists("blocked.txt") {
            case Ok(b)    => println("Exists: ${b}")
            case Err(err) => println("Error: ${err}")
        }
    } with FileSystem.withReadOnly
```

### Dry Run

`withDryRun` logs write operations via the `Logger` effect without performing
them. Read operations still execute normally:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, Logger, IO } =
    run {
        match FileSystem.write(str = "This won't be written", "phantom.txt") {
            case Err(err) => println("Write error: ${err}")
            case Ok(_) =>
                match FileSystem.exists("phantom.txt") {
                    case Ok(b)    => println("Exists: ${b}")
                    case Err(err) => println("Error: ${err}")
                }
        }
    } with FileSystem.withDryRun
```

### Atomic Write

`withAtomicWrite` writes data to a temporary file first, then atomically
renames it into place. This prevents partial writes on failure. Only `write`,
`writeLines`, and `writeBytes` are affected — appends and other operations
pass through unchanged:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    run {
        match FileSystem.write(str = "Atomic content", "output.txt") {
            case Ok(_)    => println("Atomic write succeeded.")
            case Err(err) => println("Write error: ${err}")
        }
    } with FileSystem.withAtomicWrite
```

### Backup

`withBackup` creates a backup copy of existing files before overwriting them.
Before each destructive operation (`write`, `writeLines`, `writeBytes`,
`truncate`, `delete`, `copyWith`, `moveWith`), the existing file is copied to
`file + suffix`:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    match FileSystem.write(str = "Original content", "data.txt") {
        case Err(err) => println("Setup error: ${err}")
        case Ok(_) =>
            run {
                match FileSystem.write(str = "New content", "data.txt") {
                    case Ok(_)    => println("Write succeeded; backup saved to data.txt.bak")
                    case Err(err) => println("Write error: ${err}")
                }
            } with FileSystem.withBackup(".bak")
    }
```

### Create Parent Directories

`withMkParentDirs` automatically creates parent directories before write
and append operations. If the parent directory already exists, this is a
no-op:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    run {
        match FileSystem.write(str = "Hello", "deep/nested/path/greeting.txt") {
            case Ok(_)    => println("Write succeeded (parents created).")
            case Err(err) => println("Write error: ${err}")
        }
    } with FileSystem.withMkParentDirs
```

### Conflict Check

`withConflictCheck` tracks file modification times and rejects writes when the
file has been modified externally since the last operation. This catches
write-write conflicts from external processes:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    run {
        match FileSystem.write(str = "First write", "shared.txt") {
            case Err(err) => println("Error: ${err}")
            case Ok(_) =>
                match FileSystem.write(str = "Second write", "shared.txt") {
                    case Ok(_)    => println("No conflict detected.")
                    case Err(err) => println("Conflict: ${err}")
                }
        }
    } with FileSystem.withConflictCheck
```

### Size Rotation

`withSizeRotation` automatically rotates files when they reach a size
threshold. Before append operations, the file's size is checked. If it meets
or exceeds `maxSize`, existing rotated files are shifted (`file.1` -> `file.2`,
etc.) and the current file is moved to `file.1`:

```flix
use Fs.FileSystem
use Fs.Size

def main(): Unit \ { FileSystem, IO } =
    run {
        foreach (i <- List.range(1, 20)) {
            discard FileSystem.append(str = "Log entry ${i}\n", "app.log")
        }
    } with FileSystem.withSizeRotation(Size.kiloBytes(1), 3)
```

### Transfer Limit

`withTransferLimit` rejects read or write operations where the payload exceeds
a maximum size:

```flix
use Fs.FileSystem
use Fs.Size

def main(): Unit \ { FileSystem, IO } =
    run {
        match FileSystem.write(str = "Small", "ok.txt") {
            case Ok(_)    => println("Small write succeeded.")
            case Err(err) => println("Error: ${err}")
        }
    } with FileSystem.withTransferLimit(Size.megaBytes(10))
```

### Access Control

Flix provides middleware for restricting which paths can be accessed. We can use:

- `withAllowList(dirs)` — only paths within the listed directories are allowed
- `withDenyList(dirs)` — paths within the listed directories are blocked
- `withAllowGlob(patterns)` — only paths matching at least one pattern are allowed
- `withDenyGlob(patterns)` — paths matching any pattern are blocked

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    run {
        match FileSystem.read("/tmp/safe/data.txt") {
            case Ok(content) => println(content)
            case Err(err)    => println("Error: ${err}")
        }
    } with FileSystem.withAllowList(Nel.of("/tmp/safe"))
```

### In-Memory Filesystem

`withInMemoryFS` is a terminal handler that replaces the real filesystem with
a fully in-memory implementation. The filesystem starts empty; reads of
non-written files return `NotFound`. No real filesystem access occurs:

```flix
use Fs.FileSystem
use Time.Clock

def main(): Unit \ { Clock, IO } =
    run {
        let result = forM (
            _       <- FileSystem.mkDirs("/data");
            _       <- FileSystem.write(str = "Hello", "/data/hello.txt");
            _       <- FileSystem.write(str = "World", "/data/world.txt");
            entries <- FileSystem.list("/data");
            content <- FileSystem.read("/data/hello.txt");
            _       <- FileSystem.delete("/data/hello.txt");
            exists  <- FileSystem.exists("/data/hello.txt")
        ) yield (entries, content, exists);
        match result {
            case Err(err) => println("Error: ${err}")
            case Ok((entries, content, exists)) =>
                println("Files in /data:");
                foreach (entry <- entries) {
                    println("  ${entry}")
                };
                println("Content: ${content}");
                println("Exists after delete: ${exists}")
        }
    } with FileSystem.withInMemoryFS
```

Note that `withInMemoryFS` requires the `Clock` effect (for file timestamps)
but removes `FileSystem` from the effect signature since it fully handles it.

### Memory Overlay

`withMemoryOverlay` layers an in-memory writable store on top of the real
filesystem. Writes are captured in memory and subsequent reads see the written
data, but the real filesystem is never modified. Reads of files not in the
overlay fall through to the real filesystem:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, IO } =
    run {
        // This write is captured in memory, not written to disk.
        match FileSystem.write(str = "In-memory only", "virtual.txt") {
            case Err(err) => println("Error: ${err}")
            case Ok(_) =>
                match FileSystem.read("virtual.txt") {
                    case Ok(content) => println("Read from overlay: ${content}")
                    case Err(err)    => println("Error: ${err}")
                }
        }
    } with FileSystem.withMemoryOverlay
```

## Composing Middleware

We can compose middleware by stacking `with` clauses. Each `with` wraps the
preceding block, so the outermost handler runs first. Here is an example that
stacks base directory, parent directory creation, backup, atomic writes,
conflict checking, and logging:

```flix
use Fs.FileSystem

def main(): Unit \ { FileSystem, Logger, IO } =
    run {
        match FileSystem.write(str = "Hello, Flix!", "data/greeting.txt") {
            case Err(err) => println("Write error: ${err}")
            case Ok(_) =>
                match FileSystem.read("data/greeting.txt") {
                    case Ok(content) => println("Read: ${content}")
                    case Err(err)    => println("Read error: ${err}")
                }
        }
    } with FileSystem.withBaseDir("/tmp/flix-example")
      with FileSystem.withMkParentDirs
      with FileSystem.withConflictCheck
      with FileSystem.withBackup(".bak")
      with FileSystem.withAtomicWrite
      with FileSystem.withLogging
```

The `FileSystem`, `Logger`, and `Clock` effects all have default handlers, so
they are handled automatically when they appear in the type signature of
`main`.

> **Note:** The order of `with` clauses matters. The outermost handler (listed
> last) wraps all inner handlers. In the example above, `withLogging` is
> outermost, so it sees *every* filesystem operation — including retries from
> conflict checks and temporary files from atomic writes. When composing
> middleware, think about which layer should observe which operations.

## Middleware Summary

The following table shows which middleware are available on which effects:

| Middleware             | FileTest | FilePermission | FileTime | FileStat | FileRead | DirList | Glob | FileWrite | FileSystem |
|------------------------|:--------:|:--------------:|:--------:|:--------:|:--------:|:-------:|:----:|:---------:|:----------:|
| `withLogging`          | x        | x              | x        | x        | x        | x       | x    | x         | x          |
| `withBaseDir`          | x        | x              | x        | x        | x        | x       | x    | x         | x          |
| `withChroot`           | x        | x              | x        | x        | x        | x       | x    | x         | x          |
| `withAllowList`        | x        | x              | x        | x        | x        | x       | x    | x         | x          |
| `withDenyList`         | x        | x              | x        | x        | x        | x       | x    | x         | x          |
| `withAllowGlob`        | x        | x              | x        | x        | x        | x       | x    | x         | x          |
| `withDenyGlob`         | x        | x              | x        | x        | x        | x       | x    | x         | x          |
| `withFollowLinks`      | x        | x              | x        | x        | x        | x       | x    | x         | x          |
| `withTransferLimit`    |          |                |          |          | x        |         |      | x         | x          |
| `withChecksum`         |          |                |          |          | x        |         |      | x         | x          |
| `withDryRun`           |          |                |          |          |          |         |      | x         | x          |
| `withReadOnly`         |          |                |          |          |          |         |      | x         | x          |
| `withAtomicWrite`      |          |                |          |          |          |         |      | x         | x          |
| `withBackup`           |          |                |          |          |          |         |      | x         | x          |
| `withConflictCheck`    |          |                |          |          |          |         |      | x         | x          |
| `withMkParentDirs`     |          |                |          |          |          |         |      | x         | x          |
| `withSizeRotation`     |          |                |          |          |          |         |      | x         | x          |
| `withMemoryOverlay`    |          |                |          |          |          |         |      |           | x          |
| `withInMemoryFS`       |          |                |          |          |          |         |      |           | x          |

## The Effect Hierarchy

The Flix filesystem effects form a hierarchy. At the top is `FileSystem` with
all 29 operations. Below it are intermediate effects that group related
operations, and at the bottom are leaf effects for individual operations:

```text
FileSystem                          (29 ops — unified root)
├── FileStat                        (11 ops)
│   ├── FileTest                    (4 ops: exists, isDirectory, isRegularFile, isSymbolicLink)
│   ├── FilePermission              (3 ops: isReadable, isWritable, isExecutable)
│   ├── FileTime                    (3 ops: accessTime, creationTime, modificationTime)
│   └── FileSize                    (1 op: size)
├── FileRead                        (3 ops: read, readLines, readBytes)
├── DirList                         (1 op: list)
├── Glob                            (1 op: glob)
└── FileWrite                       (13 ops: write, append, delete, copy, move, mkdir, etc.)
```

We can use any level of the hierarchy. For example, we can use a leaf effect
like `FileExists` when we only need `exists`, `FileRead` when we need to read
files, or `FileSystem` when we need everything.

We can run leaf effects into their parent effects using `runWith` handlers.
For example, we can run `FileExists` into `FileTest` and `ReadFile` into
`FileRead`:

```flix
use Fs.FileExists
use Fs.FileRead
use Fs.FileTest
use Fs.ReadFile

def main(): Unit \ { FileRead, FileTest, IO } =
    run {
        safeRead("example.txt")
    } with FileExists.runWithFileTest
      with ReadFile.runWithFileRead

def safeRead(file: String): Unit \ { FileExists, ReadFile, IO } =
    match FileExists.exists(file) {
        case Err(err)  => println("Error: ${err}")
        case Ok(false) => println("File does not exist")
        case Ok(true)  =>
            match ReadFile.read(file) {
                case Ok(content) => println(content)
                case Err(err)    => println("Read error: ${err}")
            }
    }
```
