#!/usr/bin/env python

from cliapi import parse_args
from pickapic import __version__


def main():
    args = parse_args
    if args.version:
        print(__version__)
        return


if __name__ == '__main__':
    main()
