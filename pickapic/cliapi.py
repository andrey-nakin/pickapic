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

    parser.add_argument("--get-min-width", dest='get_min_width', action="store_true",
                        help="Get current profile's minimal image width")
    parser.add_argument("--set-min-width", metavar='<min width>', dest='set_min_width', type=int,
                        help="Set current profile's minimal image width")
    parser.add_argument("--get-min-height", dest='get_min_height', action="store_true",
                        help="Set current profile's minimal image height")
    parser.add_argument("--set-min-height", metavar='<min height>', dest='set_min_height', type=int,
                        help="Set current profile's minimal image height")

    parser.add_argument("--image-number", "-n", dest='image_number', type=int, help="Number of images to download")
    parser.add_argument("--dest-dir", "-d", dest='dest_dir', help="Destination directory", default=".")
    parser.add_argument("--dry-run", dest='dry_run', action="store_true",
                        help="Do not actually download images, do search only")

    parser.add_argument("--flickr-api-key", nargs=2, metavar=('<api key>', '<api secret>'), dest='flickr_api_key',
                        help="Set API key and secret for the current profile")
    parser.add_argument("--flickr-add-license", nargs='+', metavar='<license ID>', dest='flickr_add_licenses',
                        help="Add Flickr license(s) to current profile")
    parser.add_argument("--flickr-remove-license", nargs='+', metavar='<license ID>', dest='flickr_remove_licenses',
                        help="Remove Flickr license(s) from current profile")
    parser.add_argument("--flickr-list-license", dest='flickr_list_licenses', action="store_true",
                        help="List Flickr licenses of current profile")
    parser.add_argument("--flickr-dump-licenses", dest='flickr_dump_licenses', action="store_true",
                        help="Dump all standard Flickr licenses in JSON format")
    parser.add_argument("--flickr-dump-min-timestamp", dest='flickr_dump_min_timestamp', action="store_true",
                        help="Dump the stored minimal image timestamp")
    parser.add_argument("--flickr-reset-min-timestamp", dest='flickr_reset_min_timestamp', action="store_true",
                        help="Reset the stored minimal image timestamp")

    return parser


def parse_args():
    parser = get_parser()
    return parser.parse_args()
