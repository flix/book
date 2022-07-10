# Build and Package Management

Flix has a nascent build system and package manager.
The package manager does not yet support
*dependency resolution*, but the system is sufficient
to build and share packages.
There is no central package registry, so distribution
and versioning must be handled manually for the
moment.
We propose that the semantic version of a package is
included as part of its name, e.g. `foo-1.2.1.fpkg`.

The Flix build system makes it easy to create,
compile, run, and test a Flix project.

## Overview

The Flix build system supports the following commands:

| Command     | Description                                     |
|:-----------:|:-----------------------------------------------:|
| `init`      | Creates a new project in the current directory. |
| `check`     | Checks the current project for errors.          |
| `build`     | Builds (i.e. compiles) the current project.     |
| `build-jar` | Builds a jar-file from the current project.     |
| `build-pkg` | Builds a fpkg-file from the current project.    |
| `run`       | Runs main for the current project.              |
| `test`      | Runs tests for the current project.             |

A command is executed by running `flix <command>` in
the project directory.
For example:

```bash
$ java -jar path/to/flix.jar init
```

Build commands can also be invoked from within Visual
Studio Code by pressing `CTRL + SHIFT + P` (to bring
up the command palette) and typing the name of the
relevant command.
This is the recommended way to use the build system.

**Tip:** To create a new project in Visual Studio
Code:

1. create a new empty folder,
2. open the folder in Visual Studio Code (`File -> Open Folder...`), and
3. press `CTRL + SHIFT + P` and type `Flix init`.

## Creating a New Project

We can create a new project by creating an empty
directory and running the `init` command inside it:

```bash
$ mkdir myproject
$ cd myproject
$ java -jar path/to/flix.jar init
```

This will create a project structure with the
following layout (running `$ tree .` in the directory will give the result below):

```
.
├── build
├── flix.jar
├── HISTORY.md
├── lib
├── LICENSE.md
├── README.md
├── src
│   └── Main.flix
└── test
    └── TestMain.flix

4 directories, 6 files
```

The most relevant files are `src/Main.flix` and
`test/TestMain.flix`.

The `lib/` directory is intended to hold Flix package
files (`.fpkg`-files).
The build system and Visual Studio Code will
automatically detect Flix packages that are in the
`lib/` directory.

## Checking a Project

We can check a project for errors by running the
`check` command inside the project directory:

```bash
$ java -jar path/to/flix.jar check
```

Checking a project is equivalent to building a project, except no code is generated and the
process is significantly faster than a complete build.

## Building a Project

We can build a project by running the `build` command
inside the project directory:

```bash
$ java -jar path/to/flix.jar build
```

Building a project populates the `build` directory
with class files.

#### Design Note

There is no `clean` command, but deleting everything
inside the `build` directory serves the same purpose.

## Building a JAR-file

We can compile a project to a JAR-file with the
`build-jar` command:

```bash
$ java -jar path/to/flix.jar build-jar
```

which will produce a `myproject.jar` ready to run:

```bash
$ java -jar myproject.jar
```

The JAR-file contains all class files from the
`build/` directory.

#### Warning

The project must have been built beforehand with the
`build` command.

#### Design Note

At the time of writing (July 2021), the built
JAR-file still depends on the `flix.jar` file.
Thus to run a Flix program you must put both the
generated JAR-file and `flix.jar` on the class path.
For example, on Windows, the command would be:
`java -jar "flix.jar;myproject.jar" Main`.
In the future, the plan is to make the generated
JAR-file fully self-contained.

## Building a Flix Project File (fpkg)

We can compile a project to a Flix package file
(fpkg) with the `build-pkg` command:

```bash
$ java -jar path/to/flix.jar build-pkg
```
which will produce a `myproject.fpkg` package.

A Flix package file is essentially a zip-file of the
project source code.
A Flix package file can be reused in another project
by placing it into the `lib/` directory.

It is recommended to include the semantic version in
the filename of the package, e.g. `foo-1.2.1.fpkg`.

#### Design Note

Flix does not compile to an intermediate format, but
instead relies on packages to contain source code.
This means that Flix does not lose any information
about a package and can perform cross-package
optimizations.

## Running a Project

We do not have to build a JAR-file to run a project,
we can simply use the `run` command:

```bash
$ java -jar path/to/flix.jar run
```

which will compile and run the main entry point.

## Testing a Project

We can use the `test` command to run all test cases
in a project:

```bash
$ java -jar path/to/flix.jar test
```

Flix will collect all functions marked with `@test`,
execute them, and print a summary of the results:

```
-- Tests -------------------------------------------------- root
✓ testMain01
```
