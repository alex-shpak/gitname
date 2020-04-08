# Gitname
Simple tool to set `user.name` and `user.email` or other properties in local git repository based on remote URL.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Go Report Card](https://goreportcard.com/badge/github.com/alex-shpak/gitname)](https://goreportcard.com/report/github.com/alex-shpak/gitname)

## Use case
It is common to have multiple git repositories and platforms to work with. For example you might contribute OSS at `github.com` and have private organisation `github.com/private-organization` at your work, also some repositories at `gitlab.com`. So then you might want to use different email and/or config for these repositories.

Here is where this tool useful. When you run `gitname`, it will set local config in repository according to git remote.  More specific URL has higher priority. See [configuration](#configure) for example.

## Install
### Homebrew
```sh
$ brew tap alex-shpak/gitname http://github.com/alex-shpak/gitname
$ brew install gitname
```

### Pre-compiled Binaries
You can download binary for your platform directly from [releases](https://github.com/alex-shpak/gitname/releases) page.

### Install from sources
```
$ go get -u github.com/alex-shpak/gitname
$ go install github.com/alex-shpak/gitname
```

## Configure
Add these lines to `.gitconfig` file into your home directory, modify where needed. You can use other global [git config files](https://git-scm.com/docs/git-config#FILES) as well.

```ini
[user "github.com"]
	name = Alex Shpak
	email = alex-shpak@users.noreply.github.com

[user "github.com/private-organization"]
	name = Alexander Shpak
	email = organization-email@example.com
	signingKey = xxx

[user "gitlab.com"]
	name = Alex Shpak
	email = gitlab-email@example.com
```

## Run
Navigate to target git repository and run `gitname`:
```
~/Projects/gitname » gitname
2019/10/11 21:14:54 Committing as Alex Shpak <alex-shpak@users.noreply.github.com>
```

You can set specific section by passing name of section as argument: `gitname github.com`, this comes useful when there is no remote yet.

You can also create handy alias.

```sh
$ git config --global alias.name '!gitname'
$ git name
```

## Unset globally configured name
Optionally run below commands to unset globally configured name and email and [prevent Git](https://git-scm.com/docs/git-config#git-config-useruseConfigOnly) from guessing them in newly cloned repositories.

```sh
$ git config --global user.name ""
$ git config --global user.email ""
$ git config --global user.useConfigOnly true
```
