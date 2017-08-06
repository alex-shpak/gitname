## Gitname

Simple script to set `user.name` and `user.email` into git repository based on remote hostname.


## Setup
Put `gitname.py` into your path

Put file `.gitname` into your home directory with content
```ini
[github.com]
name: User Name
email: username@users.noreply.github.com
```

Run script in git repository.
As result name and email config will be updated with matching values


## Licence
[MIT](LICENCE.txt)