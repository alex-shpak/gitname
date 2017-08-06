## Gitname

Simple script to set `user.name` and `user.email` or other properties into git repository based on remote hostname.


## Setup
Put `gitname.py` into your path

Put file `.gitname` into your home directory with content
```ini
[github.com]
user.name: User Name
user.email: username@users.noreply.github.com
```

Run script in git repository.
As result name and email config will be updated with matching values


## Licence
[MIT](LICENCE.txt)