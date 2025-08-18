# Getting Started

Getting started with Flix is straightforward. All you need is [Java version 21+](https://adoptium.net/temurin/releases/).

You can check if Java is installed and its version by typing:

```shell
$ java -version
```

which should print something like:

```
openjdk version "21" 2023-09-19 LTS
OpenJDK Runtime Environment Temurin-21+35 (build 21+35-LTS)
OpenJDK 64-Bit Server VM Temurin-21+35 (build 21+35-LTS, mixed mode, sharing)
```

If Java is not installed or your version is too old, a newer version can be
downloaded from [Adoptium](https://adoptium.net/temurin/releases/).

Once you have Java 21+ installed there are two ways to proceed:

- You can use the [Flix VSCode extension](https://marketplace.visualstudio.com/items?itemName=flix.flix) (__highly recommended__) or
- You can run the Flix compiler from the command line.

### Using Flix from Visual Studio Code (VSCode)

Flix comes with a fully-featured VSCode plugin. Follow these steps to get
started:

> 1. Create a new empty folder (e.g. `my-flix-project`).
> 2. Open VSCode and choose `File -> Open Folder`.
> 3. Create a new file called `Main.flix` in the folder.
> 4. VSCode will ask you want to search the marketplace for extensions. Say "Yes".
> 5. The Flix _extension_ will be downloaded and installed. Once done, it will
>    ask if you want to download the Flix _compiler_. Say "Yes" again.
> 6. When you see "Starting Flix" followed by "Flix Ready!" everything should be ready.

A screenshot of the Flix Visual Studio Code extension in action:

![Visual Studio Code1](images/vscode1.png)

### Using Flix from Neovim

Flix can also be used from [Neovim](https://neovim.io/). Follow these steps to
get started:
- the [official plugin](https://github.com/flix/nvim) relies on features released in Neovim 0.11
- check the version of neovim installed

```shell
nvim --version
```

#### Neovim Flix plugin

There is a Lua [plugin](https://github.com/flix/nvim) which provides an LSP configuration for the native neovim lsp, and several functions to interact with the flix cli. It's repo has detailed installation and configuration instructions.
It can be installed with a plugin manager of choice or cloned locally into your neovim runtime path.

The plugin provides no Keymappings but sets the Flix LSP server up, allowing it to work with your default LSP mappings. An example of setting up LSP keymappings with nvim 0.11 can be seen below. Once your `LspAttach` autocmd has been set the keymappings will apply to *all* configured lsp servers.

```lua
-- create auto command that is triggered when your LSP server attatches to the buffer
vim.api.nvim_create_autocmd('LspAttach', {
  -- give it a name to prevent autocmd conflicts
  group = vim.api.nvim_create_augroup('my.lsp', {}),
  -- the function to run when the server attatches
  callback = function(args)
    -- helper function to set keybinding options with an optional description string
    -- !!! important !!!
    -- `buffer` makes these mappings local to the buffer triggering the autocmd
    local function get_opts(desc)
      return { desc = desc, buffer = args.buf, noremap = true, silent = true }
    end
    -- check that the LSP client supports features before setting bindings
    local client = assert(vim.lsp.get_client_by_id(args.data.client_id))
    if client:supports_method('textDocument/format') then
      vim.keymap.set('n', '<leader>=', vim.lsp.buf.format, get_opts('format buffer'))
    end
    if client:supports_method('textDocument/rename') then
      vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, get_opts('rename'))
    end
    vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action, get_opts("lsp code action"))
    vim.keymap.set("n", "<leader>cl", vim.lsp.codelens.run, get_opts("lsp codelens run"))
    vim.keymap.set("n", "gr", vim.lsp.buf.references, get_opts("lsp references"))
    vim.keymap.set("n", "gd", vim.lsp.buf.definition, get_opts("lsp definition"))
    vim.keymap.set("n", "<leader>h", vim.lsp.buf.document_highlight, get_opts("lsp document highlight"))
    vim.keymap.set("n", "K", vim.lsp.buf.hover, get_opts("lsp hover"))
    vim.keymap.set("n", "gi", vim.lsp.buf.implementation, get_opts("lsp buf implementation"))
    vim.keymap.set('i', '<C-a>', '<C-x><C-o>', get_opts("manual expand completion"))
    vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, get_opts(""))
    vim.keymap.set("n", "<leader>d", vim.diagnostic.open_float, get_opts("diagnostic open float"))
    vim.keymap.set("n", "<leader>ws", vim.lsp.buf.workspace_symbol, get_opts("lsp workspace symbol"))
    vim.keymap.set("n", "<leader>ds", vim.lsp.buf.document_symbol, get_opts("lsp doc symbol"))
  end
})
```

> Previously [lspconfig](https://github.com/neovim/nvim-lspconfig) provided LSP functionality to neovim and lsp configurations. However, after version 0.11 neovim has LSP built in, lspconfig only provides configurations for common lsp servers. This makes its installation less necessary but it is still recommended.

![Visual Studio Code1](images/neovim.png)

#### Manual Neovim Configuration

### Using Flix from Emacs

Flix can be used from [Emacs](https://www.gnu.org/software/emacs/) as well by installing the [flix-mode](https://codeberg.org/mdiin/flix-mode) package. Follow the instructions there to get started writing Flix code in Emacs.

### Using Flix from the Command Line

Flix can also be used from the command line. Follow these steps:

> 1. Create a new empty folder (e.g. `my-flix-project`).
> 2. Download the latest `flix.jar` from [https://github.com/flix/flix/releases/latest](https://github.com/flix/flix/releases/latest) and put it into the folder.
> 3. Enter the created directory (e.g. `cd my-flix-project`) and run `java -jar flix.jar init` to create an empty Flix project.
> 4. Run `java -jar flix.jar run` to compile and run the project.


### Using nix

Flix can also be installed using the [nix package manager](https://nixos.org/).
To install for the currently running shell run:

```shell
$ nix-shell -p flix
```

Or alternatively to install globally:

```shell
$ nix-env -i flix
```

Then run `flix run` in your project directory.

### Troubleshooting

The most common reasons for Flix not working are (a) the `java` command not
being on your `PATH`, (b) the `JAVA_HOME` environmental variable not being set
or being set incorrectly, or (c) having the wrong version of Java installed. To
debug these issues, ensure that:

- The command `java -version` prints the right Java version.
- The `JAVA_HOME` environmental variable is correctly set.
    - On Windows, you can print the variable by typing `echo %JAVA_HOME%`.
    - On Mac and Linux, you can print the variable by typing `echo $JAVA_HOME`.

If you are still stuck, you can ask for help on [Gitter](https://gitter.im/flix/Lobby).
