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

> **Tip:** We should prefer the REPL while we work. The REPL keeps the project in
> memory and recompiles only what has changed, so `:check` and `:test` in the REPL
> are much faster than re-running the same commands from the shell, where every run
> starts from scratch.

## The Commands at a Glance

| Command         | Description                                             |
|-----------------|---------------------------------------------------------|
| `init`          | creates a new project in the current directory.         |
| `check`         | checks the project for compiler errors.                 |
| `run`           | runs `main` in the project.                             |
| `test`          | runs all tests in the project.                          |
| `doc`           | generates API documentation for the project.            |
| `stat`          | prints statistics about the project.                    |
| `build`         | compiles the entire project.                            |
| `build-classes` | compiles the project to Java class files.               |
| `build-jar`     | builds a JAR-file from the project.                     |
| `build-fatjar`  | builds a JAR-file with all dependencies bundled.        |
| `build-pkg`     | builds a Flix package (an fpkg-file) from the project.  |
| `clean`         | removes the `build` and `artifact` directories.         |
| `install`       | adds a Flix package to the dependencies.                |
| `upgrade`       | changes the version of a Flix package dependency.       |
| `remove`        | removes a Flix package from the dependencies.           |
| `outdated`      | shows dependencies which have newer versions available. |
| `release`       | releases a new version of the project to GitHub.        |

We declare the dependencies of a project in its manifest, which we can edit
ourselves or with the `install`, `upgrade`, and `remove` commands, as described in
[Using Dependencies](./using-dependencies.md). Every dependency is built in a
*security context* that limits what it is allowed to do, as described in
[Trusting Dependencies](./trusting-dependencies.md).

> **Note:** Most commands also work in a directory that has no manifest. Flix
> then loads source files from `*.flix`, `src/**`, and `test/**`, and has no
> dependencies to resolve. The `build-pkg`, `clean`, `install`, `upgrade`,
> `remove`, and `release` commands require a manifest.
