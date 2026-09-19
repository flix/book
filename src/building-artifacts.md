# Building Artifacts

When the program works, we can build something we can ship: Java class files, a
JAR-file, a standalone fat JAR-file, or a Flix package.

Two of these are what we usually want: a fat JAR-file, if we distribute a program to
end users, since it runs on its own wherever Java runs, and a Flix package, if we
share a library with other Flix developers.

## Compiling the Project

We can compile the project with the `build` command. The `build` command compiles
the entire project, including code generation, but writes nothing to disk. We use
it to check that the whole project compiles.

## Building Class Files

We can compile the project to Java class files with the `build-classes` command.
Flix writes the class files to the `build/class` directory, and if the project has
a `main` function, we can run it with `java`:

```shell
$ java -cp build/class Main
Hello World!
```

Class files are rarely what we want to ship: we have to keep the directory together,
and we have to put every dependency on the class path ourselves. To hand the program
to someone else, we build a fat JAR-file instead.

> **Note:** If the project, or one of its dependencies, depends on JAR-files, then
> these must also be on the class path.

## Building a JAR-file

We can build a JAR-file with the `build-jar` command. Flix writes the JAR-file to
the `artifact` directory, named after the project directory, and we can run it
with `java`:

```shell
$ java -jar artifact/hello-world.jar
Hello World!
```

The JAR-file holds the class files of the project together with the files in the
`resources` directory, if the project has one.

> **Note:** The `build-jar` command compiles the project itself. There is no need
> to run `build` or `build-classes` first.

A JAR-file built this way does *not* hold the dependencies of the project. If the
program uses one — say a Java library, as described in
[Using Dependencies](./using-dependencies.md) — then the JVM fails to find it when
we run the JAR-file:

```shell
$ java -jar artifact/inventory.jar
Exception in thread "main" java.lang.NoClassDefFoundError: org/apache/commons/lang3/StringUtils
```

We can either put the dependencies on the class path ourselves, or bundle them
into the JAR-file.

## Bundling Dependencies in a Fat JAR-file

We can build a JAR-file with all dependencies bundled — a *fat* JAR-file — with
the `build-fatjar` command. Flix writes it to the same place, and now the program
runs on its own:

```shell
$ java -jar artifact/inventory.jar
!dlroW olleH
```

The fat JAR-file holds the class files of the project, the files in the `resources`
directory, and the contents of every JAR-file in the `lib` directory, i.e. _all_
dependencies — both Flix and Maven.

> **Note:** The `build-jar` and `build-fatjar` commands write to the same
> JAR-file. Whichever we ran last is the one we have.

> **Note:** The `build-fatjar` command compiles the project itself. There is no
> need to run `build` or `build-classes` first.

## Building a Flix Package

We can bundle the project into a Flix package with the `build-pkg` command. Flix
writes the package to the `artifact` directory, and copies the manifest next to it:

```
artifact
├── flix.toml
└── package.fpkg
```

The package file is always called `package.fpkg`, whatever the project is called, so
that the two files of a release can be found from the repository and the version
alone.

A Flix package is essentially a zip-file of the source code of the project: it
holds the manifest, the `README.md`, the `LICENSE.md`, and the Flix files in `src`.
It holds no tests and no compiled code — a Flix package is compiled from source by
whoever depends on it. Together with its manifest, it can be published on GitHub,
as described in [Publishing a Package](./publishing-a-package.md).

> **Note:** The `build-pkg` command checks the project first, and refuses to build
> a package from source code that does not compile.

> **Note:** The `build-pkg` command requires a manifest, since a package without a
> manifest cannot be published.

## Cleaning Up

We can remove the `build` directory with the `clean` command. This deletes the
class files written by `build-classes` and the documentation written by `doc`.

> **Note:** The `clean` command leaves the `artifact` directory alone. We remove
> the JAR- and package-files we have built ourselves.
