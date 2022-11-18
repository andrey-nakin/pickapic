from .cliapi import parse_args
from .context import Context
from .profile import create_profile
import caribou
import os


def pickapic():
    args = parse_args()
    if args.version:
        print("0.1.0")
        return

    # upgrade to most recent version
    caribou.upgrade(args.config, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'migrations'))

    context = Context(args)

    if args.create_profile:
        create_profile(context, args.create_profile)
