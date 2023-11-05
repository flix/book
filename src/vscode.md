## Visual Studio Code Extension

Flix comes with [a fully-featured Visual Studio Code Extension](https://marketplace.visualstudio.com/items?itemName=flix.flix):

![Visual Studio Code1](images/vscode1.png)

The Flix extension uses the real Flix compiler hence all information (e.g. error
messages) are always 1:1 with the real Flix programming language.

Flix also comes with an (optional) Visual Studio Code color theme called "Flixify Dark".

### Features

* __Semantic Syntax Highlighting__
    - Code highlighting for *.flix files. This work best with the [official vscode theme](https://marketplace.visualstudio.com/items?itemName=flix.flixify-dark).

* __Diagnostics__
    - Compiler error messages. 

* __Auto-complete__
    - Auto-complete as you type.
    - Auto-completion is context aware.
    - Type-directed completion of program holes.

* __Snippets__
    - Auto-complete common code constructs.

* __Inlay Hints__
    - Shows inline type information.

* __Type and Effect Hovers__
    - Hover over any expression to see its type and effect.
    - Hover over any local variable or formal parameter to see its type.
    - Hover over any function to see its type signature and documentation.

* __Jump to Definition__
    - Jump to the definition of any function.
    - Jump to the definition of any local variable or formal parameter.
    - Jump to the definition of any enum case.

* __Find References__
    - Find all references to a function.
    - Find all references to a local variable or formal parameter.
    - Find all references to an enum case.
    - Find all implementations of a trait.

* __Symbols__
    - List all document symbols.
    - List all workspace symbols.

* __Rename__
    - Rename local variables or formal parameters.
    - Rename functions.

* __Code Lenses__
    - Run `main` from within the editor.
    - Run tests from within the editor.

* __Highlight__
    - Highlights semantically related symbols.

* __Semantic Tokens__
    - Additional code highlighting hints provided by the compiler.

### Known Limitations

- There is a known issue with PowerShell and using file names that contain
  special characters. We recommend that Flix source files are given only ASCII
  names. 

- The extension assumes that you are working in "Workspace Mode", i.e. you must
  have a folder open which contains your Flix source code. 

- Upon startup, the Flix compiler has to load the entire Flix standard library
  into its caches which takes a few seconds.
