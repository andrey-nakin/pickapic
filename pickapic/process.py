from .driver import flickr
import os
from .image import resize_and_crop


def process(context, num_of_images):
    while num_of_images > 0:
        images = flickr.process(context, num_of_images)
        num_of_images = num_of_images - len(images)
        if len(images) == 0:
            break

        for image in images:
            _process_image(context, image)


def _process_image(context, image):
    resize_and_crop(image.filename, image.destname, context.min_dimensions())
    os.unlink(image.filename)

    print(image.title)
    print(image.image_page_url)
    print(image.author_desc.name)
    print(image.author_desc.page_url)
    print(image.license_desc.name)
    print(image.license_desc.page_url)
