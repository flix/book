# Build and Package Management

> **Note:** This section is a work in progress.

Flix has a nascent build system and package manager.

The Flix build system makes it easy to create,
compile, run, and test a Flix project.


### Overview

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
$ java -jar flix.jar init
```
