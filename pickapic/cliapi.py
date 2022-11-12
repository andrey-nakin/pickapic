import argparse


def get_parser():
    parser = argparse.ArgumentParser("pickapic")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument("--config", "-c", help="Path to configuration database file (default: pickapic.db)",
                        default="pickapic.db")
    parser.add_argument("--search-profile", "-p", help="Search profile to use")
    parser.add_argument("--add-tag", nargs=2, metavar=('profile', 'tag'), help="Add search tag to a profile")
    parser.add_argument("--remove-tag", nargs=2, metavar=('profile', 'tag'), help="Remove search tag from a profile")
    parser.add_argument("--list-tags", nargs=1, metavar='profile', help="List profile search tags")
    parser.add_argument("--add-global-stop-tag", nargs=1, metavar='tag', help="Add tag to global black list")
    parser.add_argument("--remove-global-stop-tag", nargs=1, metavar='tag', help="Remove tag from global black list")
    parser.add_argument("--list-global-stop-tags", action="store_true", help="List global black list tags")
    return parser


def parse_args():
    parser = get_parser()
    return parser.parse_args()
