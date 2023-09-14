from pickapic.flickr.apikey import flickr_set_api_key
from pickapic.flickr.license import flickr_add_licenses, flickr_remove_licenses, flickr_list_licenses, \
    flickr_dump_licenses
from pickapic.flickr.timestamp import flickr_dump_min_timestamp, flickr_reset_min_timestamp


def flickr_main(context, args):
    if args.flickr_api_key:
        flickr_set_api_key(context, args.flickr_api_key[0], args.flickr_api_key[1])

    if args.flickr_add_licenses:
        flickr_add_licenses(context, args.flickr_add_licenses)
    if args.flickr_remove_licenses:
        flickr_remove_licenses(context, args.flickr_remove_licenses)
    if args.flickr_list_licenses:
        flickr_list_licenses(context)
    if args.flickr_dump_licenses:
        flickr_dump_licenses(context)
    if args.flickr_dump_min_timestamp:
        flickr_dump_min_timestamp(context)
    if args.flickr_reset_min_timestamp:
        flickr_reset_min_timestamp(context)


def flickr_add_argument(parser):
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
