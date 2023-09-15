import caribou
import os

from pickapic.cliapi import parse_args
from pickapic.context import Context
from pickapic.profile import create_profile, delete_profile, list_profiles
from pickapic.tag import add_tags, remove_tags, list_tags
from pickapic.dimension import get_min_width, set_min_width, set_min_height, get_min_height
from pickapic.process import process
from pickapic.processedimage import print_num_of_processed, reset_processed_images
from pickapic.flickr.cli import flickr_main


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
    if args.list_profiles:
        list_profiles(context)

    if args.add_tags:
        add_tags(context, args.add_tags, False)
    if args.remove_tags:
        remove_tags(context, args.remove_tags, False)
    if args.list_tags:
        list_tags(context, False)

    if args.add_stop_tags:
        add_tags(context, args.add_stop_tags, True)
    if args.remove_stop_tags:
        remove_tags(context, args.remove_stop_tags, True)
    if args.list_stop_tags:
        list_tags(context, True)

    if args.get_min_width:
        get_min_width(context)
    if args.set_min_width is not None:
        set_min_width(context, args.set_min_width)
    if args.get_min_height:
        get_min_height(context)
    if args.set_min_height is not None:
        set_min_height(context, args.set_min_height)

    if args.get_num_of_processed:
        print_num_of_processed(context)
    if args.reset_processed:
        reset_processed_images(context)

    flickr_main(context, args)

    if args.image_number:
        process(context, args.image_number)
