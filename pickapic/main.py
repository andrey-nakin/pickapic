from .cliapi import parse_args
from .context import Context
from .profile import create_profile
from .profile import delete_profile
from .tag import add_tags
from .tag import remove_tags
from .tag import list_tags
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
    if args.delete_profile:
        delete_profile(context, args.delete_profile)
    if args.add_tags:
        add_tags(context, args.add_tags)
    if args.remove_tags:
        remove_tags(context, args.remove_tags)
    if args.list_tags:
        list_tags(context)
