from .cliapi import parse_args
import caribou


def pickapic():
    args = parse_args()
    if args.version:
        print("0.1.0")
        return

    db_path = args.config
    migrations_path = '/home/andrey/workspace/pickapic/pickapic/migrations'

    # upgrade to most recent version
    caribou.upgrade(db_path, migrations_path)
