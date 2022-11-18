import argparse


def get_parser():
    parser = argparse.ArgumentParser("pickapic")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument("--config", "-c", help="Path to configuration database file (default: pickapic.db)",
                        default="pickapic.db")
    parser.add_argument("--profile", "-p", help="Profile to use")

    parser.add_argument("--create-profile", nargs='*', metavar=('profile', 'parent'), help="Create new profile")
    parser.add_argument("--delete-profile", help="Delete existing profile")

    parser.add_argument("--add-tag", nargs='?', metavar=('tag'), help="Add search tag to profile")
    parser.add_argument("--remove-tag", nargs='?', metavar=('tag'), help="Remove search tag from profile")
    parser.add_argument("--list-tags", action="store_true", help="List profile's search tags")

    parser.add_argument("--add-stop-tag", nargs='?', metavar=('tag'), help="Add tag to profile black list")
    parser.add_argument("--remove-stop-tag", nargs='?', metavar=('tag'), help="Remove tag from profile black list")
    parser.add_argument("--list-stop-tags", action="store_true", help="List profile's black list tags")

    parser.add_argument("--get-min-width", help="Get profile's minimal image width")
    parser.add_argument("--set-min-width", help="Set profile's minimal image width")
    parser.add_argument("--get-min-height", help="Set profile's minimal image height")
    parser.add_argument("--set-min-height", help="Set profile's minimal image height")

    parser.add_argument("--image-number", "-n", help="Number of images to download")
    parser.add_argument("--dest-dir", "-d", help="Destination directory", default=".")

    return parser


def parse_args():
    parser = get_parser()
    return parser.parse_args()
