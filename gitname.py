#!/usr/bin/python

import commands
import ConfigParser
import os
import re
from urlparse import urlparse
from os.path import expanduser


def color(text, color='\033[0;32m'):
    return '%s%s\033[0m' % (color, text)


def merge_sections(config, *sections):
    items = dict()
    for section in sections:
        if config.has_section(section):
            items.update(
                {item[0]: item[1] for item in config.items(section)}
            )

    return items


def getname():
    status, remote = commands.getstatusoutput('git remote get-url origin')

    if status is not 0:
        print 'No remote found in'
        os.system('git config --list')
        quit()

    if '://' not in remote:
        remote = 'scheme://%s' % remote

    remote_items = re.split('://|@|:', remote)[2:]
    remote_host = remote_items[0]
    remote_repository = '/'.join(remote_items)

    config = ConfigParser.SafeConfigParser()
    config.read('%s/.gitname' % expanduser('~'))

    items = merge_sections(
        config,
        remote_host,
        remote_repository
    )
    
    if not items:
        print 'No properties found for %s' % color(remote_host)

    for key, value in items.iteritems():
        print 'Set %s "%s"' % (color(key), value)
        os.system('git config %s "%s"' % (key, value))


if __name__ == '__main__':
    getname()