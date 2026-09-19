# Projects and Packages

Flix comes with a build system and a package manager.

The build system compiles a project to Java class files, to a JAR-file, or to a
single standalone fat JAR-file. The package manager downloads the Flix packages
and Java libraries that a project depends on, and publishes a project on GitHub
as a package that others can depend on.

A Flix project is a directory with a `flix.toml` manifest, Flix source code in
`src`, and tests in `test`. We create such a project with the `init` command, we
work on it with the `check`, `run`, and `test` commands, and we ship it with the
`build-jar` and `release` commands.

We run the commands from the command line. How we invoke Flix depends on how we
installed it, as described in [Getting Started](./getting-started.md). Most
commands can also be run from the REPL, where they are written with a colon, e.g.
`:check` and `:test`. In VSCode we do not have to run anything: the project is
checked as we type, and `▶ Run` and `▶ Run Tests` appear above `main` and above
every test.

## The Commands at a Glance

| Command         | Description                                             | Described in                                                        |
|-----------------|---------------------------------------------------------|---------------------------------------------------------------------|
| `init`          | creates a new project in the current directory.         | [Creating a Project](./creating-a-project.md)                        |
| `check`         | checks the project for compiler errors.                 | [Checking, Running, and Testing](./checking-running-and-testing.md)  |
| `run`           | runs `main` in the project.                             | [Checking, Running, and Testing](./checking-running-and-testing.md)  |
| `test`          | runs all tests in the project.                          | [Checking, Running, and Testing](./checking-running-and-testing.md)  |
| `doc`           | generates API documentation for the project.            | [Checking, Running, and Testing](./checking-running-and-testing.md)  |
| `stat`          | prints statistics about the project.                    | [Checking, Running, and Testing](./checking-running-and-testing.md)  |
| `build`         | compiles the entire project.                            | [Building Artifacts](./building-artifacts.md)                        |
| `build-classes` | compiles the project to Java class files.               | [Building Artifacts](./building-artifacts.md)                        |
| `build-jar`     | builds a JAR-file from the project.                     | [Building Artifacts](./building-artifacts.md)                        |
| `build-fatjar`  | builds a JAR-file with all dependencies bundled.        | [Building Artifacts](./building-artifacts.md)                        |
| `build-pkg`     | builds a Flix package (an fpkg-file) from the project.  | [Building Artifacts](./building-artifacts.md)                        |
| `clean`         | removes the `build` directory.                          | [Building Artifacts](./building-artifacts.md)                        |
| `outdated`      | shows dependencies which have newer versions available. | [Versions and Upgrades](./versions-and-upgrades.md)                  |
| `release`       | releases a new version of the project to GitHub.        | [Publishing a Package](./publishing-a-package.md)                    |

We declare the dependencies of a project in its manifest, as described in
[Using Dependencies](./using-dependencies.md). Every dependency is built in a
*security context* that limits what it is allowed to do, as described in
[Trusting Dependencies](./trusting-dependencies.md).

> **Note:** Most commands also work in a directory that has no manifest. Flix
> then loads source files from `*.flix`, `src/**`, and `test/**`, and has no
> dependencies to resolve. The `build-pkg`, `clean`, and `release` commands
> require a manifest.

We begin by creating a project.
