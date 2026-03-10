# Env

Flix provides `Env` as a library effect for accessing environment variables,
system properties, and platform information. The `Env` effect has a default
handler, so no explicit `runWithIO` call is needed in `main`. The key module is
`Sys.Env`.

## The Env Effect

The `Env` effect provides operations for reading the program's environment:

```flix
pub eff Env {
    /// Returns the arguments passed to the program via the command line.
    def getArgs(): List[String]

    /// Returns a map of the current system environment.
    def getEnv(): Map[String, String]

    /// Returns the value of the specified environment variable.
    def getVar(name: String): Option[String]

    /// Returns the system property by name.
    def getProp(name: String): Option[String]

    /// Returns the operating system name.
    def getOsName(): Option[String]

    /// Returns the operating system architecture.
    def getOsArch(): Option[String]

    /// Returns the operating system version.
    def getOsVersion(): Option[String]

    /// Returns the file separator.
    def getFileSeparator(): String

    /// Returns the path separator.
    def getPathSeparator(): String

    /// Returns the system line separator.
    def getLineSeparator(): String

    /// Returns the user's current working directory.
    def getCurrentWorkingDirectory(): Option[String]

    /// Returns the default temp file path.
    def getTemporaryDirectory(): Option[String]

    /// Returns the user's account name.
    def getUserName(): Option[String]

    /// Returns the user's home directory.
    def getUserHomeDirectory(): Option[String]

    /// Returns the number of virtual processors available to the JVM.
    def getVirtualProcessors(): Int32
}
```

## Directories and OS Info

The simplest use of `Env` is to query the current directory, home directory,
or operating system:

```flix
use Sys.Env

def main(): Unit \ { Env, IO } =
    let home = Env.getUserHomeDirectory();
    println("Home: ${home}");
    let cwd = Env.getCurrentWorkingDirectory();
    println("CWD: ${cwd}");
    let os = Env.getOsName();
    println("OS: ${os}")
```

## Environment Variables

Use `getVar` to read a single environment variable, or `getEnv` to retrieve all
of them as a map:

```flix
use Sys.Env

def main(): Unit \ { Env, IO } =
    let path = Env.getVar("PATH");
    println("PATH: ${path}");
    let all = Env.getEnv();
    println("Total env vars: ${Map.size(all)}")
```

## System Information

The `Env` effect also exposes platform details such as the OS architecture and
the number of available processors:

```flix
use Sys.Env

def main(): Unit \ { Env, IO } =
    let name    = Env.getOsName();
    let arch    = Env.getOsArch();
    let version = Env.getOsVersion();
    let cpus    = Env.getVirtualProcessors();
    println("OS:   ${name}");
    println("Arch: ${arch}");
    println("Ver:  ${version}");
    println("CPUs: ${cpus}")
```
