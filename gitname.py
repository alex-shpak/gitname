#!/usr/bin/python

import commands
import ConfigParser
import os
from urlparse import urlparse
from os.path import expanduser


status, remote = commands.getstatusoutput('git remote get-url origin')
if status is not 0:
    print 'No remote found in'
    os.system('git config --list')
    quit()

if '://' not in remote:
    remote = 'scheme://%s' % remote

hostname = urlparse(remote).hostname

config_defaults = { 'name': None, 'email': None }
config = ConfigParser.SafeConfigParser(defaults = config_defaults)
config.read('%s/.gitname' % expanduser('~'))

if not config.has_section(hostname):
    print 'No section "%s" found in ~/.gitname' % hostname
    quit()

git_name = config.get(hostname, 'name')
git_email = config.get(hostname, 'email')

if git_name is not None:
    print '-- %s<%s>' % (git_name, git_email)
    os.system('git config user.name "%s"' % git_name)
    os.system('git config user.email "%s"' % git_email)