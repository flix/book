# Getting Started

Getting started with Flix is straightforward. All you need is Java version 11+.

You can check your current version of Java by typing:

```shell
$ java -version
```

which should print something like:

```
openjdk version "18.0.2.1" 2022-08-18
OpenJDK Runtime Environment Temurin-18.0.2.1+1 (build 18.0.2.1+1)
OpenJDK 64-Bit Server VM Temurin-18.0.2.1+1 (build 18.0.2.1+1, mixed mode, sharing)
```

If Java is not installed or your version is too old, a newer version can be
downloaded from [Adoptium](https://adoptium.net/temurin/releases/).

Once you have Java 11+ installed there are two ways to proceed:

- You can use the Flix VSCode extension (__highly recommended__) or
- You can run the Flix compiler from the command line.

### Using Flix from Visual Studio Code (VSCode)

Flix comes with a fully-featured VSCode plugin. Follow these steps to get
started:

> 1. Create a new empty directory (e.g. `my-flix-project`).
> 2. Open VSCode and choose `File -> Open Folder`.
> 3. Create a file called `Main.flix`. 
> 4. VSCode will ask you want to search the marketplace. Say Yes.

A screenshot of the VSCode extension in action:

![Visual Studio Code1](images/vscode1.png)

### Using Flix from the Command Line

Flix can also be used from the command line. Follow these steps:

> 1. Create a new empty directory (e.g. `my-flix-project`).
> 2. Download `flix.jar` from [https://github.com/flix/flix/releases](https://github.com/flix/flix/releases)
> 3. Create a file called `Main.flix` with some source code.
> 4. Run `java -jar flix.jar Main.flix`.

### Troubleshooting Java Issues

The most common reason for Flix not working is (a) `java` not being on your
`PATH` or (b) having the wrong version of Java on your path. To debug these
issues, ensure that:

- The command `java -version` prints the right Java version.
- The `JAVA_HOME` environmental variable is correctly set. 
    - On Windows, you print the variable by typing `echo %JAVA_HOME%`.
    - On Mac and Linux, you print the variable by typing `echo $JAVA_HOME`.
