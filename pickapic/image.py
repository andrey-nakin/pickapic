import math
from PIL import Image
from PIL import ImageFile


def resize_and_crop(srcfile, destfile, target_dimensions):
    original = Image.open(srcfile)
    width, height = original.size
    target_width, target_height = target_dimensions

    aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height

    ImageFile.LOAD_TRUNCATED_IMAGES = True
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
    cropped.save(destfile)
