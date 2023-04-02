## Build Management

### Creating a New Project

We can create a new project, inside a directory, with the `init` command. 

This will create the default Flix project structure:

```
.
├── flix.toml
├── LICENSE.md
├── README.md
├── src
│   └── Main.flix
└── test
    └── TestMain.flix

2 directories, 6 files
```

The most relevant files are `flix.toml`, `src/Main.flix` and
`test/TestMain.flix`.

> **Tip:** The `init` command is safe to use; it will only create files which do
> not already exist. 

### Checking a Project

We can check a project for compiler errors by with the `check` command. The
`check` command is significantly faster than the `build` command because it
skips code generation. 

### Building a Project

We can build a project by with the `build` command. Running the `build` command
will compile the entire project and emit Java bytecode. 

> **Note:** Flix has no `clean` command. Deleting the `build` directory serves
> the same purpose.

### Building a JAR-file

We can compile a Flix project to a fat JAR-file with the `build-jar` command.
The `build-jar` command with emit an `artifact/projectname.jar` file. We can
then run it: 

```bash
$ java -jar artifact/projectname.jar
```

The JAR-file contains all class files from the `build` directory. The built JAR
may depend on external JARs, if the project or one of its dependencies, depends
on JAR-files (e.g. via Maven dependencies). 

> **Note:** The project must be compiled with `build` before running
> `build-jar`.

### Building a Flix Project

We can bundle a Flix project into a Flix package file (fpkg) `build-pkg`
command. Running the `build-pkg` command will emit the fpkg file in the
`artifact` directory. 

A Flix package file is essentially zip-file of the project source code. A Flix
package, together with its `flix.toml` manifest, can be published on GitHub.

### Running a Project

We do not have to build a JAR-file to run a project, we can simply use the `run`
command which will compile and run the main entry point.

### Testing a Project

We can use the `test` command to run all test cases in a project. Flix will
collect all functions marked with `@Test`, execute them, and print a summary of
the results:

```
Running 1 tests...

   PASS  test01 1,1ms

Passed: 1, Failed: 0. Skipped: 0. Elapsed: 3,9ms.
```
