import argparse


def get_parser():
    parser = argparse.ArgumentParser("pickapic")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument("--config", "-c", help="Path to configuration database file (default: pickapic.db)",
                        default="pickapic.db")
    parser.add_argument("--profile", "-p", metavar='<profile>', help="Profile to use")

    parser.add_argument("--create-profile", nargs='*', metavar=('<profile>', '<parent profile>'), dest='create_profile',
                        help="Create new profile")
    parser.add_argument("--delete-profile", metavar='<profile>', dest='delete_profile', help="Delete existing profile")
    parser.add_argument("--list-profiles", dest='list_profiles', action="store_true", help="List all profiles")

    parser.add_argument("--add-tag", nargs='+', metavar='<tag>', dest='add_tags',
                        help="Add search tag(s) to current profile")
    parser.add_argument("--remove-tag", nargs='+', metavar='<tag>', dest='remove_tags',
                        help="Remove search tag(s) from current profile")
    parser.add_argument("--list-tags", dest='list_tags', action="store_true", help="List current profile's search tags")

    parser.add_argument("--add-stop-tag", nargs='+', metavar='<tag>', dest='add_stop_tags',
                        help="Add tag(s) to current profile's black list")
    parser.add_argument("--remove-stop-tag", nargs='+', metavar='<tag>', dest='remove_stop_tags',
                        help="Remove tag from current profile's black list")
    parser.add_argument("--list-stop-tags", dest='list_stop_tags', action="store_true",
                        help="List current profile's black list tags")

    parser.add_argument("--get-min-width", help="Get profile's minimal image width")
    parser.add_argument("--set-min-width", type=int, help="Set profile's minimal image width")
    parser.add_argument("--get-min-height", help="Set profile's minimal image height")
    parser.add_argument("--set-min-height", type=int, help="Set profile's minimal image height")

    parser.add_argument("--image-number", "-n", type=int, help="Number of images to download")
    parser.add_argument("--dest-dir", "-d", help="Destination directory", default=".")

    return parser


def parse_args():
    parser = get_parser()
    return parser.parse_args()
