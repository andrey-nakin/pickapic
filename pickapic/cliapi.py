import argparse


def get_parser():
    parser = argparse.ArgumentParser("ae.py")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument("--config", "-c", help="Path to configuration database file (default: pickapic.db)",
                        default="pickapic.db")
    parser.add_argument("--search-profile", "-p", help="Search profile to use")
    return parser


def parse_args():
    parser = get_parser()
    return parser.parse_args()
