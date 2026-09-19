# Checking, Running, and Testing

While we work on a project we mostly use three commands: `check` to find errors,
`run` to see the program work, and `test` to see that it still works.

## Checking for Errors

We can check the project for compiler errors with the `check` command:

```
Found 'flix.toml'. Checking dependencies...
Resolving Flix dependencies...
Downloading Flix dependencies...
Resolving Maven dependencies...
  Running Maven dependency resolver.
Downloading external jar dependencies...
Dependency resolution completed.
```

Flix begins every command by resolving the dependencies of the project, which is
what these lines report. Our project has no dependencies yet, so there is nothing
to download. We leave these lines out of the examples that follow.

If the project does not compile, Flix reports the errors instead. If we add a
function that refers to a name that does not exist:

```flix
def sum(x: Int32, y: Int32): Int32 = x + z
```

then `check` reports:

```
-- Resolution Error [E2136] -------------------------------------- src/Main.flix

>> Undefined name 'z'.

5 | def sum(x: Int32, y: Int32): Int32 = x + z
                                             ^
                                             name not found
```

During development, the `check` command is preferable to the `build` command,
because `check` skips code generation and hence is significantly faster.

> **Tip:** In VSCode we do not have to run `check` at all: the same errors appear
> in the editor as we type.

## Running the Program

We can compile and run the project with the `run` command. We do not have to build
anything first:

```
Hello World!
```

The `run` command runs the `main` function of the project. See
[The Main Function](./main.md) for what `main` may look like.

## Running the Tests

We can run the tests with the `test` command. Flix collects every function marked
with `@Test`, runs it, and prints a summary:

```
Running 1 tests...

   PASS  test01 1.3ms

Passed: 1, Failed: 0. Skipped: 0. Elapsed: 3.8ms.
```

See [Test Framework](./test-framework.md) for how to write tests.

## Generating Documentation

We can generate API documentation for the project with the `doc` command. Flix
writes the documentation to the `build/doc` directory:

```
build
└── doc
    ├── favicon.png
    ├── index.html
    ├── index.js
    └── styles.css
```

We read it by opening `build/doc/index.html` in a browser.

> **Tip:** The `doc` command also takes a `--library` flag, which documents the
> bundled standard library instead of the current project.

## Printing Statistics

We can print statistics about the project with the `stat` command:

```
hello-world 0.1.0

2 files, 5 lines: 4 code, 1 comment, 0 blank.
0 modules, 2 defs: 0 pure, 2 effectful, 0 effect polymorphic.
0 types, 0 traits, 0 instances, 0 effects.
```

Once the program does what we want, we are ready to build something we can ship.
