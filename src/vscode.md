# Visual Studio Code Extension

Flix comes with a fully-featured Visual Studio Code Extension:

![Visual Studio Code1](images/vscode1.png)

The extension uses the real Flix compiler hence all information (e.g. error
messages) are always 1:1 with the real Flix programming language.

Flix also comes with an (optional) Visual Studio Code color theme called "Flixify Dark".

## Known Limitations

- Most functionality is only available while the program parses and type checks. 
    - Thus before e.g. renaming a local variable it is best to ensure that no
      errors are reported.

- The extension assumes that you are working in "Workspace Mode", i.e. you must
  have a folder open which contains your Flix source code. 

- Standby seems to break the connection between VSCode and the Flix language server.

- Upon startup, the Flix compiler has to load the entire Flix standard library
  into its caches which takes a few seconds.
