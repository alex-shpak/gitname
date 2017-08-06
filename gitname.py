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


def getname():
    status, remote = commands.getstatusoutput('git remote get-url origin')

    if status is not 0:
        logger.info('No remote found in')
        os.system('git config --list')
        quit()

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
        logger.info('No properties found for %s' % color(remote_host))

    for key, value in items.iteritems():
        logger.info('Set %s "%s"' % (color(key), value))
        os.system('git config %s "%s"' % (key, value))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Updates git config based on ~/.gitname.')
    parser.add_argument(
        '--quiet',
        action="store_true",
        help='Run without output'
    )

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(message)s"  # hide level
    )

    getname()