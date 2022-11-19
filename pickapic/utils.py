import sys


def panic(error_msg):
    print(error_msg, file=sys.stderr)
    exit(1)


def orientation_matches(image_dimensions, target_dimensions):
    image_orientation = orientation(image_dimensions)
    target_orientation = orientation(target_dimensions)
    return image_orientation == 'Square' or target_orientation == 'Square' or image_orientation == target_orientation


def orientation(dimensions):
    width, height = dimensions
    if width > height * 1.4:
        return 'Landscape'
    if width * 1.4 < height:
        return 'Portrait'
    return 'Square'


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
