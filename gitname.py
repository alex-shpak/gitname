#!/usr/bin/python

import commands
import ConfigParser
import os
from urlparse import urlparse
from os.path import expanduser

def color(text, color='\033[0;32m'):
    return '%s%s\033[0m' % (color, text)

status, remote = commands.getstatusoutput('git remote get-url origin')

if status is not 0:
    print 'No remote found in'
    os.system('git config --list')
    quit()

if '://' not in remote:
    remote = 'scheme://%s' % remote

hostname = urlparse(remote).hostname

config = ConfigParser.SafeConfigParser()
config.read('%s/.gitname' % expanduser('~'))

if not config.has_section(hostname):
    print 'No section %s found in ~/.gitname' % color(hostname)
    quit()

host_items = config.items(hostname)
if not host_items:
    print 'No properties found for %s' % color(hostname)

for key, value in host_items:
    print 'Set %s "%s"' % (color(key), value)
    os.system('git config %s "%s"' % (key, value))
