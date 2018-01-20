#!/usr/bin/python

import ConfigParser
import argparse
import commands
import logging
import os
import re

logger = logging.getLogger('gitname')


def color(text, color='\033[0;32m'):
    return '%s%s\033[0m' % (color, text)


def merge_sections(config, urlparts):
    items = dict()

    for index in range(len(urlparts)):
        section = '/'.join(urlparts[:index+1])

        if config.has_section(section):
            items.update(
                {item[0]: item[1] for item in config.items(section)}
            )

    return items


def gitname(args):
    status, remote = commands.getstatusoutput('git remote get-url %s' % args.remote)

    if args.logging == logging.DEBUG:
        os.system('git remote -v')
        print

    if status is not 0:
        logger.warning('Remote %s not found' % color(args.remote))
        return

    if '://' not in remote:
        remote = 'scheme://%s' % remote

    remote_items = re.split('://|@|:|/', remote)[2:]
    remote_host = remote_items[0]

    config = ConfigParser.SafeConfigParser()
    config.read('%s/.gitname' % os.path.expanduser('~'))

    items = merge_sections(
        config,
        remote_items
    )

    if not items:
        logger.warning('No properties found for %s' % color(remote_host))
        return

    for key, value in items.iteritems():
        status, current = commands.getstatusoutput('git config %s' % key)
        if current == value:
            continue

        logger.debug('Set %s to "%s"' % (color(key), value))
        os.system('git config %s "%s"' % (key, value))


def reminder():
    status, name = commands.getstatusoutput('git config user.name')
    status, email = commands.getstatusoutput('git config user.email')

    author = color('%s <%s>' % (name, email))
    logger.info('Committing as %s' % author)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Updates git config based on ~/.gitname.')
    parser.add_argument(
        '-v',
        '--verbose',
        dest='logging',
        default=logging.INFO,
        action='store_const',
        const=logging.DEBUG,
        help='print debugging output'
    )
    parser.add_argument(
        '-q',
        '--quiet',
        dest='logging',
        action='store_const',
        const=logging.WARNING,
        help='run without output'
    )
    parser.add_argument(
        '-r',
        '--remote',
        default='origin',
        help='sets remote for lookup'
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=args.logging,
        format='%(message)s'  # hide logging level
    )

    gitname(args)
    reminder()
