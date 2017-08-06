## Gitname

Simple script to set `user.name` and `user.email` or other properties into git repository based on remote hostname.


## Setup
Put `gitname.py` into your path, for example as `~/.local/bin/gitname`

Put file `.gitname` into your home directory with content
```ini
[github.com]
user.name: Alex Shpak
user.email: alex-shpak@users.noreply.github.com

[github.com/alex-shpak/gitname.git]
user.name: Alex
user.email: alex-shpak@users.noreply.github.com
```

Run script in git repository.
As result config will be updated with matching values


## Licence
[MIT](LICENCE.txt)