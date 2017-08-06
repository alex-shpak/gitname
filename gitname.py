#!/usr/bin/python

import commands
import ConfigParser
import logging
import os
import re
import argparse
from urlparse import urlparse


logger = logging.getLogger('gitname')


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


def gitname(args):
    status, remote = commands.getstatusoutput('git remote get-url origin')

    if status is not 0:
        logger.warning('No remote found in')
        os.system('git config --list')
        return

    if '://' not in remote:
        remote = 'scheme://%s' % remote

    remote_items = re.split('://|@|:', remote)[2:]
    remote_host = remote_items[0]
    remote_repository = '/'.join(remote_items)

    config = ConfigParser.SafeConfigParser()
    config.read('%s/.gitname' % os.path.expanduser('~'))

    items = merge_sections(
        config,
        remote_host,
        remote_repository
    )
    
    if not items:
        logger.warning('No properties found for %s' % color(remote_host))
        return

    for key, value in items.iteritems():
        status, current = commands.getstatusoutput('git config %s' % key)
        if current == value:
            continue

        logger.info('Set %s "%s"' % (color(key), value))
        os.system('git config %s "%s"' % (key, value))

def reminder():
    status, name = commands.getstatusoutput('git config user.name')
    status, email = commands.getstatusoutput('git config user.email')

    author = color('%s <%s>' % (name, email))
    logger.warning('Commiting as %s' % author)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Updates git config based on ~/.gitname.')
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Run without output'
    )
    parser.add_argument(
        '--no-reminder',
        action='store_true',
        help='Run without output'
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format='%(message)s'  # hide level
    )

    gitname(args)
    if not args.no_reminder:
        reminder()