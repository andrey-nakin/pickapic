from .driver import flickr


def process(context, num_of_images):
    flickr.doit(context)
