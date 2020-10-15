#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

Usage:
  bigbuild deploy app <user-id> <app-id> <image> <port> [-r <num>]
  bigbuild get port <user-id> <app-id>
  bigbuild (describe|destroy|log) app <user-id> <app-id>
  bigbuild list apps <user-id>
  bigbuild scale <user-id> <app-id> [-r <num>]
  bigbuild test

  bigbuild -h | --help
  bigbuild --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -r <num>      Number of replicas [default: 3].
'''

# TODO: accept multiple ports & types when deploying,

from __future__ import unicode_literals, print_function
from docopt import docopt

from . import commands

__version__ = "0.2.0"
__author__ = "Won Jung"
__license__ = "MIT"


def main():
    '''Main entry point for the bigbuild CLI.'''
    args = docopt(__doc__, version=__version__)
    commands.process_args(args)

if __name__ == '__main__':
    main()
