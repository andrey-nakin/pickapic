from .cliapi import parse_args
from .context import Context
import caribou


def pickapic():
    args = parse_args()
    if args.version:
        print("0.1.0")
        return

    migrations_path = '/home/andrey/workspace/pickapic/pickapic/migrations'

    # upgrade to most recent version
    caribou.upgrade(args.config, migrations_path)

    ctx = Context(args)
