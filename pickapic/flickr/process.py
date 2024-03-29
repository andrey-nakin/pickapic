import math
import webbrowser

import flickrapi
from urllib.parse import urlparse
import pathlib
import hashlib
import os
import urllib.request
from tempfile import mkstemp
from time import sleep
from datetime import datetime

from pickapic.utils import panic
from pickapic.utils import orientation_matches
from pickapic.utils import intersection
from pickapic.imagedescriptor import ImageDescriptor
from pickapic.authordescriptor import AuthorDescriptor
from pickapic.licensedescriptor import LicenseDescriptor
from pickapic.processedimage import is_image_processed

from pickapic.flickr.apikey import flickr_get_api_key
from pickapic.flickr.license import flickr_get_license_ids, flickr_load_license_info
from pickapic.flickr.timestamp import flickr_get_min_timestamp, flickr_set_min_timestamp

MAX_PHOTOS_PER_PAGE = 500


def flickr_process(context, num_of_images):
    api_key, api_secret = flickr_get_api_key(context)
    min_width, min_height = context.min_dimensions()
    # tags = ','.join(context.tags() + list(map(lambda x: '-' + x, context.stop_tags())))
    tags = ','.join(context.tags())
    # print(tags)

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    if not flickr.token_valid(perms='read'):
        # Get a request token
        flickr.get_request_token(oauth_callback='oob')

        # Open a browser at the authentication URL. Do this however
        # you want, as long as the user visits that URL.
        authorize_url = flickr.auth_url(perms='read')
        webbrowser.open_new_tab(authorize_url)

        # Get the verifier code from the user. Do this however you
        # want, as long as the user gives the application the code.
        verifier = str(input('Verifier code: '))

        # Trade the request token for an access token
        flickr.get_access_token(verifier)

    licenses = dict({})
    for lic in flickr_load_license_info(context):
        licenses[str(lic['id'])] = lic
    # print(licenses)

    page = 0
    per_page = min(MAX_PHOTOS_PER_PAGE, num_of_images * 10)
    result = []
    authors = dict({})
    processed_photo_ids = []
    statistics = {'found': 0}
    max_found_timestamp = 0

    sort_mode = context.args.sort
    if not sort_mode:
        sort_mode = 'date-posted-asc'

    tag_mode = 'any'
    if context.args.all_tags:
        tag_mode = 'all'
    print("Flickr: searching for images tagged by:", tags, "with mode", tag_mode, "sort mode", sort_mode)

    min_search_timestamp = flickr_get_min_timestamp(context)
    if min_search_timestamp is None:
        min_search_timestamp = 0
    else:
        print("Flickr: searching for images with upload time greater than",
              datetime.fromtimestamp(min_search_timestamp))

    license_ids = flickr_get_license_ids(context)

    while num_of_images > statistics['found']:
        page = page + 1
        photos = flickr.photos.search(tags=tags, tag_mode=tag_mode, privacy_filter=1, safe_search=3, content_types=0,
                                      media='photos', extras='license, date_upload, o_dims, url_o, tags',
                                      sort='date-posted-asc',
                                      license=','.join(license_ids) if len(license_ids) > 0 else None,
                                      per_page=per_page,
                                      page=page, min_upload_date=min_search_timestamp)

        # print(photos)
        if photos['stat'] != 'ok':
            panic("Flickr: error searching photos")
        print("Flickr: loading", per_page, "photos from page", page, "total", photos['photos']['total'])

        if len(photos['photos']['photo']) == 0:
            break  # no more photos

        for photo in photos['photos']['photo']:
            photo_id = photo['id']
            if photo_id in processed_photo_ids:
                continue
            processed_photo_ids.append(photo_id)
            _update_statistics(statistics, 'total')

            if min_width > 0:
                if 'width_o' not in photo or photo['width_o'] < min_width:
                    _update_statistics(statistics, 'size-mismatch')
                    continue
            if min_height > 0:
                if 'height_o' not in photo or photo['height_o'] < min_height:
                    _update_statistics(statistics, 'size-mismatch')
                    continue
            if min_width > 0 and min_height > 0:
                if not orientation_matches((photo['width_o'], photo['height_o']), (min_width, min_height)):
                    _update_statistics(statistics, 'orientation-mismatch')
                    continue
            if 'tags' not in photo:
                _update_statistics(statistics, 'no-tags')
                continue
            if 'dateupload' not in photo:
                _update_statistics(statistics, 'no-tags')
                continue
            photo_tags = str(photo['tags']).split()
            if len(intersection(photo_tags, context.tags())) == 0:
                _update_statistics(statistics, 'tag-mismatch')
                continue
            if len(intersection(photo_tags, context.stop_tags())) > 0:
                _update_statistics(statistics, 'stop-tags')
                continue

            descriptor = _process_photo(context, flickr, photo, authors, licenses, statistics)
            if descriptor:
                result.append(descriptor)
                _update_statistics(statistics, 'found')
                timestamp = int(photo['dateupload'])
                if max_found_timestamp < timestamp:
                    max_found_timestamp = timestamp
                if num_of_images <= statistics['found']:
                    break

    print("Flickr: statistics")
    print("Total photos processed:", statistics['total'])
    _print_statistics(statistics, 'size-mismatch', 'Excluded due to size mismatch:')
    _print_statistics(statistics, 'orientation-mismatch', 'Excluded due to orientation mismatch:')
    _print_statistics(statistics, 'no-tags', 'Excluded due to missing tags:')
    _print_statistics(statistics, 'tag-mismatch', 'Excluded due to tag mismatch:')
    _print_statistics(statistics, 'stop-tags', 'Excluded due to stop tags:')
    _print_statistics(statistics, 'no-author-info', 'Excluded due to absence of author info:')
    _print_statistics(statistics, 'no-license-info', 'Excluded due to absence of license info:')
    _print_statistics(statistics, 'found', 'Found:')

    if sort_mode == 'date-posted-asc':
        flickr_set_min_timestamp(context, max_found_timestamp)

    return result


def _update_statistics(statistics, key):
    if key not in statistics:
        statistics[key] = 1
    else:
        statistics[key] = statistics[key] + 1


def _print_statistics(statistics, key, title):
    if key in statistics:
        print(title, statistics[key], '(', "{0:.1%}".format(statistics[key] / statistics['total']), ')')


def _process_photo(context, flickr, photo, authors, licenses, statistics):
    image_id = 'flickr:' + photo['id']
    if is_image_processed(context, image_id):
        return None

    author = None
    if 'owner' in photo:
        if photo['owner'] in authors:
            author = authors[photo['owner']]  # use cached inf0
        else:
            authors[photo['owner']] = author = _get_author_info(flickr, photo['owner'])
    if author is None:
        _update_statistics(statistics, 'no-author-info')
        return None

    license_desc = None
    if 'license' in photo:
        lic_id = str(photo['license'])
        if lic_id in photo['license'] in licenses:
            lic_info = licenses[lic_id]
            license_desc = LicenseDescriptor(name=lic_info['name'], page_url=lic_info['url'])
    if license_desc is None and len(licenses) > 0:
        _update_statistics(statistics, 'no-license-info')
        return None

    image_page_url = None
    if not context.args.dry_run:
        info = flickr.photos.getInfo(photo_id=photo['id'], secret=photo['secret'])
        # print(info)
        if info['stat'] != 'ok':
            panic("Flickr: error getting photo info")

        if 'photo' in info and 'urls' in info['photo'] and 'url' in info['photo']['urls']:
            for url in info['photo']['urls']['url']:
                if 'type' in url and url['type'] == 'photopage':
                    image_page_url = url['_content']

    # print(photo)

    if 'url_o' not in photo:
        print("No link to origin size, ignoring photo")
        return None

    parsed_url = urlparse(photo['url_o'])
    destname = hashlib.md5(photo['url_o'].encode('utf-8')).hexdigest() + pathlib.Path(
        parsed_url.path).suffix

    if not context.args.dry_run:
        fd, filename = mkstemp()
        os.close(fd)

        print("Flickr: downloading from", photo['url_o'], "to", filename)
        urllib.request.urlretrieve(photo['url_o'], filename)
    else:
        filename = 'none'

    return ImageDescriptor(id=image_id, filename=filename, destname=destname, width=photo['width_o'],
                           height=photo['height_o'], title=photo['title'], image_page_url=image_page_url,
                           author_desc=author, license_desc=license_desc)


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
