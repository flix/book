# Projects

> 🤔 Note: The following is written from the POV of command line usage, but we should have and document VSCode equivalents.

## Creating a Flix Project

You can create and run a new Flix project with `flix new`, for example:

```
% flix new hello-world
Creating project from template "app" in hello-world
% cd hello-world
% flix run
Hello world!
```

## Anatomy of a Flix Project

This is the structure that the above creates:

```svgbob
 |
 +- src
 |   |
 |   '- Main.flix
 |
 +- test
 |   |
 |   '- TestMain.flix
 |
 +- FlixProject.toml
 +- LICENSE.txt
 '- README.md
```

Flix treats any directory containing a file called `FlixProject.toml` as a Flix project. There are two different basic types of Flix project:

* **Applications:** Collections of source files and other resources (e.g. HTML files, images, ...) which are built into an executable project.

* **Libraries:** Collections of source files and other resources which are intended for use within applications (or other libraries).

By default `flix new` creates an application project, but it can be used to create a library by specifying the `lib` template: `flix new --template lib my-new-library`.

> 🤔 Note: Perhaps not at first release, but eventually we should allow the creation of user defined templates to automate the creation of more complex projects, e.g. web apps (which in addition to the above would have a `resources` directory, `index.html`, default routes, etc.).
