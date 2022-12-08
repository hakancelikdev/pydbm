## Development and Contributing

## Issue

To make an improvement, add a new feature or anything else, please open an issue first.

**Good first issues are the issues that you can quickly solve, we recommend you take a
look.**
[Good first issue](https://github.com/hakancelikdev/pydbm/labels/good%20first%20issue)

## Fork Repository

[fork the pydbm.](https://github.com/hakancelikdev/pydbm/fork)

## Clone Repository

```shell
$ git clone git@github.com:<USERNAME>/pydbm.git
$ cd pydbm
```

## Setup Branch

```shell
git checkout develop
git checkout -b i{your issue number}
```

## How to Update My Local Repository

```shell
$ git remote add upstream git@github.com:hakancelikdev/pydbm.git
$ git fetch upstream # or git fetch --all
$ git rebase upstream/develop
```

## Testing

Firstly make sure you have py3.8, py3.9 and py3.10 python versions installed on
your system.

After typing your codes, you should run the tests by typing the following command.

```shell
$ python3.10 -m pip install tox
$ tox
```

If tox pass.

## The final step

After adding a new feature or fixing a bug please report your change to
[changelog.md](CHANGELOG.md) and write your name, GitHub address, and email in the
[authors.md](AUTHORS.md) file in alphabetical order.

### Changelog Guide

```
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - YYYY-MM-DD

### Added | Fixed | Changed | Removed
- [{Use the emoji below that suits you.} {Explain the change.} @{Add who solved the issue.}]({Add PR link})

{You can provide more details or examples if you wish.}

```

### Commit Messages

Follow the below commit template;

```
git commit -m "{Description your changes in shortly} #{issue-id}"
```

### Open PR

Then open the pull request to develop branch.