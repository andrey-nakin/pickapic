import os

from pickapic.flickr.process import flickr_process
from pickapic.image import resize_and_crop, set_exif_info

SEPARATOR = ' | '


def process(context, num_of_images):
    while num_of_images > 0:
        images = flickr_process(context, num_of_images)
        num_of_images = num_of_images - len(images)
        if len(images) == 0:
            break

        if not context.args.dry_run:
            for image in images:
                _process_image(context, image)

        break


def _process_image(context, image):
    destname = os.path.join(context.args.dest_dir, image.destname)
    resize_and_crop(image.filename, destname, context.min_dimensions())
    os.unlink(image.filename)

    # print(image.title)
    # print(image.image_page_url)
    # print(image.author_desc.name)
    # print(image.author_desc.page_url)
    # print(image.license_desc.name)
    # print(image.license_desc.page_url)

    image_info = None
    if image.title:
        image_info = image.title
        if image.image_page_url:
            image_info = image_info + SEPARATOR + image.image_page_url

    author_info = None
    if image.author_desc and image.author_desc.name:
        author_info = image.author_desc.name
        if image.author_desc.page_url:
            author_info = author_info + SEPARATOR + image.author_desc.page_url

    license_info = None
    if image.license_desc and image.license_desc.name:
        license_info = image.license_desc.name
        if image.license_desc.page_url:
            license_info = license_info + SEPARATOR + image.license_desc.page_url

    set_exif_info(destname, image_description=image_info, artist=author_info, copyright=license_info)
