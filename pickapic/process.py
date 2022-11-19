from .driver import flickr


def process(context, num_of_images):
    while num_of_images > 0:
        images = flickr.doit(context, num_of_images)
        num_of_images = num_of_images - len(images)
        if len(images) == 0:
            break

        for image in images:
            _process_image(context, image)


def _process_image(context, image):
    print(image)
