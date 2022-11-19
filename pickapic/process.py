from .driver import flickr
from PIL import Image
import math


def process(context, num_of_images):
    while num_of_images > 0:
        images = flickr.doit(context, num_of_images)
        num_of_images = num_of_images - len(images)
        if len(images) == 0:
            break

        for image in images:
            _process_image(context, image)


def _process_image(context, image):
    original = Image.open(image.filename)
    width, height = original.size
    target_width, target_height = context.min_dimensions()
    if width >= target_width and height >= target_height:
        aspect_ratio = width / height
        target_aspect_ratio = target_width / target_height

        if aspect_ratio >= target_aspect_ratio:
            original.thumbnail((math.floor(aspect_ratio * target_height), target_height),
                               Image.Resampling.LANCZOS)
        else:
            original.thumbnail((target_width, math.floor(target_width / aspect_ratio)),
                               Image.Resampling.LANCZOS)

        width, height = original.size
        min_x = math.floor((width - target_width) / 2)
        min_y = math.floor((height - target_height) / 2)
        cropped = original.crop((min_x, min_y, min_x + target_width, min_y + target_height))
        cropped.save("cropped.jpg")

    print(image)
