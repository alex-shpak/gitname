## Gitname

Simple script to set `user.name` and `user.email` or other properties into git repository based on remote hostname or repository.


## Setup
Put `gitname.py` into your path, for example as `~/.local/bin/gitname`  
Run `chmod +x gitname.py` if needed
Put file `.gitname` into your home directory with content
```ini
[github.com]
user.name: Alex Shpak
user.email: alex-shpak@users.noreply.github.com

[github.com/alex-shpak/gitname.git]
user.name: Alex
```

Run script in git repository. As result local git config will be updated with matching values.  
Note that repository specific config sections has higher priority.


## Git hook
You can setup local or global git hook for automatic run. See [git docs](https://git-scm.com/docs/githooks)


## Licence
[MIT](LICENCE.txt)