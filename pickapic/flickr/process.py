import flickrapi
from urllib.parse import urlparse
import pathlib
import hashlib
import os
import urllib.request
from tempfile import mkstemp
from time import sleep

from pickapic.utils import panic
from pickapic.utils import orientation_matches
from pickapic.utils import intersection
from pickapic.imagedescriptor import ImageDescriptor
from pickapic.authordescriptor import AuthorDescriptor
from pickapic.licensedescriptor import LicenseDescriptor

from .apikey import flickr_get_api_key
from .license import flickr_get_license_ids, flickr_load_license_info

MAX_PHOTOS_PER_PAGE = 500


def flickr_process(context, num_of_images):
    api_key, api_secret = flickr_get_api_key(context)
    min_width, min_height = context.min_dimensions()
    # tags = ','.join(context.tags() + list(map(lambda x: '-' + x, context.stop_tags())))
    tags = ','.join(context.tags())
    # print(tags)

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    licenses = dict({})
    for lic in flickr_load_license_info(context):
        licenses[str(lic['id'])] = lic
    # print(licenses)

    found_photos = 0
    page = 0
    per_page = min(MAX_PHOTOS_PER_PAGE, num_of_images * 10)
    result = []
    authors = dict({})

    while num_of_images > found_photos:
        page = page + 1
        photos = flickr.photos.search(tags=tags, tag_mode='any', privacy_filter=1, safe_search=1, content_type=1,
                                      media='photos', extras='license, date_upload, o_dims, url_o, tags',
                                      sort='date-posted-asc', license=','.join(flickr_get_license_ids(context)),
                                      per_page=per_page, page=page)
        # print(photos)
        if photos['stat'] != 'ok':
            panic("Flickr: error searching photos")
        print("Flickr: loading", per_page, "photos from page", page, "total", photos['photos']['total'])

        if len(photos['photos']['photo']) == 0:
            break  # no more photos

        for photo in photos['photos']['photo']:
            if 'width_o' not in photo or photo['width_o'] < min_width:
                continue
            if 'height_o' not in photo or photo['height_o'] < min_height:
                continue
            if not orientation_matches((photo['width_o'], photo['height_o']), (min_width, min_height)):
                continue
            if 'tags' not in photo:
                continue
            photo_tags = str(photo['tags']).split()
            if len(intersection(photo_tags, context.tags())) == 0:
                continue
            if len(intersection(photo_tags, context.stop_tags())) > 0:
                continue

            descriptor = _process_photo(flickr, photo, authors, licenses)
            if descriptor:
                result.append(descriptor)
                found_photos = found_photos + 1
                if num_of_images <= found_photos:
                    break

        sleep(1)

    return result


def _process_photo(flickr, photo, authors, licenses):
    author = None
    if 'owner' in photo:
        if photo['owner'] in authors:
            author = authors[photo['owner']]  # use cached inf0
        else:
            authors[photo['owner']] = author = _get_author_info(flickr, photo['owner'])
    if author is None:
        return None

    license_desc = None
    if 'license' in photo:
        lic_id = str(photo['license'])
        if lic_id in photo['license'] in licenses:
            lic_info = licenses[lic_id]
            license_desc = LicenseDescriptor(name=lic_info['name'], page_url=lic_info['url'])
    if license_desc is None:
        return None

    info = flickr.photos.getInfo(photo_id=photo['id'], secret=photo['secret'])
    # print(info)
    if info['stat'] != 'ok':
        panic("Flickr: error getting photo info")

    image_page_url = None
    if 'photo' in info and 'urls' in info['photo'] and 'url' in info['photo']['urls']:
        for url in info['photo']['urls']['url']:
            if 'type' in url and url['type'] == 'photopage':
                image_page_url = url['_content']

    # print(photo)

    if not photo['url_o']:
        print("No link to origin size, ignoring photo")
        return None

    fd, filename = mkstemp()
    os.close(fd)

    print("Flickr: downloading from", photo['url_o'], "to", filename)
    urllib.request.urlretrieve(photo['url_o'], filename)

    parsed_url = urlparse(photo['url_o'])
    destname = hashlib.md5(photo['url_o'].encode('utf-8')).hexdigest() + pathlib.Path(
        parsed_url.path).suffix

    return ImageDescriptor(filename=filename, destname=destname, width=photo['width_o'], height=photo['height_o'],
                           title=photo['title'], image_page_url=image_page_url, author_desc=author,
                           license_desc=license_desc)


def _get_author_info(flickr, user_id):
    info = flickr.people.getInfo(user_id=user_id)
    if info['stat'] != 'ok':
        panic("Flickr: error getting people info")
    person = info['person']
    name = None
    page_url = None

    if person:
        if 'realname' in person:
            name = person['realname']['_content']
        else:
            name = person['username']['_content']

        if 'profileurl' in person:
            page_url = person['profileurl']['_content']
        elif 'photosurl' in person:
            page_url = person['photosurl']['_content']
        elif 'mobileurl' in person:
            page_url = person['mobileurl']['_content']

    return AuthorDescriptor(name=name, page_url=page_url)