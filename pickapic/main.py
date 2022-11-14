from .cliapi import parse_args


def pickapic():
    args = parse_args()
    if args.version:
        print("0.1.0")
        return
