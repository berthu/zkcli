# [`zk`]cli

zk is a command line interface used to manage Zettalkasten notes. Requirements:

- A config file, placed in `$HOME/.zkcli`, can be generated with `python3 -m zk init`
- A Zettelkasten directory with subfolders designed according to the config file specifications. Notably, there should be a `.Templates` folder with note templates.

# Installation

```bash
$ python3 setup.py install
```
It helps to have the following in `.zshrc`:
```bash
alias zk='python3 -m zk'
```

# Usage

- `zk daily`
- `zk fleet [TOPIC](optional)`
- `zk perm TOPIC`
- `zk lit TOPIC`
- `zk meet TOPIC`

Append `-e` to edit file with editor. If file exists, editor opens existing file. Default editor is vim.


# `--help`

```
Usage: zk [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version         Show the application's version and exit.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  daily  Create a daily note.
  fleet  Create a fleeting note with optional[TOPIC].
  init   Initialize the config file in home directory.
  lit    Create a literature note with required[TOPIC].
  meet   Create a meeting note with required[TOPIC].
  perm   Create a permanent note with required[TOPIC].
```


