# obsidian-front-matter-manager

> Adds one or more tags to all of the Obsidian (YAML+Markdown) files in a
  specified Vault.

## Setup

This tool uses [Poetry](https://python-poetry.org/) for dependency
management.

If you do not have Poetry installed (check with `poetry --version`),
you will need to install it according to [the official
instructions](https://python-poetry.org/docs/master/#installing-with-the-official-installer) before proceeding.

Then clone the `obsidian-front-matter-manager` repo to a location of
your choice, navigate into it, and run:  
`poetry install`

This should produce output similar to the following:

```
Creating virtualenv obsidian-front-matter-manager-wEDrdZeW-py3.10 in /Users/myuser/Library/Caches/pypoetry/virtualenvs
Installing dependencies from lock file

Package operations: 2 installs, 0 updates, 0 removals

  • Installing pyyaml (6.0)
  • Installing python-frontmatter (1.0.0)
```

## Usage

After installing Poetry and using the `poetry install` command to
download and install dependencies, the script can be run using the
command `poetry run python3 main.py`.

```
$ poetry run python3 main.py -h
usage: main.py [-h] --obsidian-vault-root OBSIDIAN_VAULT_ROOT [--required-tags REQUIRED_TAGS [REQUIRED_TAGS ...]] [--dry-run]

options:
  -h, --help            show this help message and exit
  --obsidian-vault-root OBSIDIAN_VAULT_ROOT
                        Absolute path to root of Obsidian Vault to Manage
  --required-tags REQUIRED_TAGS [REQUIRED_TAGS ...]
                        List of tags required to be present in each md file.
  --dry-run             When True, operate on a temp copy of the vault root dir.
```


### Example

In the following example, the tag "work" is being added to all Markdown (`.md` suffix) files
located inside the Obsidian Vault `~/Desktop/Work-test`.

```
$ poetry run python3 main.py --obsidian-vault-root ~/Desktop/Work-test/ --required-tags "work"

2022-08-29 01:50:27,884 obsidian_vault_root: /Users/myuser/Desktop/Work-test
2022-08-29 01:50:27,884 required_tags: ['work']
2022-08-29 01:50:27,884 walking root dir /Users/myuser/Desktop/Work-test. Pruned dirs: ['Attachments', 'Completed Items', 'HR', 'Reference', 'Templates']
2022-08-29 01:50:27,884 walking root dir /Users/myuser/Desktop/Work-test/Attachments. Pruned dirs: []
2022-08-29 01:50:27,885 walking root dir /Users/myuser/Desktop/Work-test/Completed Items. Pruned dirs: []
2022-08-29 01:50:27,886 	2019-12-12 Parking Info.md: ['TODO/closed', 'work', 'personal']
2022-08-29 01:50:27,887 	2019-12-13 ToDo.md: ['TODO/closed', 'work']
[...]
```
