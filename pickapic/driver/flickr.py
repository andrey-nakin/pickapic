import flickrapi
from time import sleep
from pickapic.profile import get_profile_hierarchy
from pickapic.utils import panic
from tempfile import mkstemp
import os
import urllib.request
from pickapic.imagedescriptor import ImageDescriptor


def doit(context, num_of_images):
    api_key, api_secret = get_api_key(context)
    min_width, min_height = context.min_dimensions()

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    licenses = flickr.photos.licenses.getInfo()
    # print(licenses)

    found_photos = 0
    page = 0
    per_page = min(500, num_of_images * 10)
    result = []

    while num_of_images > found_photos:
        page = page + 1
        print("Flickr: loading ", per_page, " photos from page", page)
        photos = flickr.photos.search(tags='krasnodar', tag_mode='any', privacy_filter=1, safe_search=1, content_type=1,
                                      media='photos',
                                      extras='license, date_upload, o_dims, url_o',
                                      sort='date-posted-asc',
                                      license='1,2,3,4,5,6,7,9,10',
                                      per_page=per_page, page=page)
        if photos['stat'] != 'ok':
            panic("Flickr: error searching photos")

        if len(photos['photos']['photo']) == 0:
            break  # no more photos

        for photo in photos['photos']['photo']:
            if not photo['width_o'] or photo['width_o'] < min_width:
                continue
            if not photo['height_o'] or photo['height_o'] < min_height:
                continue

            descriptor = _process_photo(context, photo)
            if descriptor:
                result.append(descriptor)
                found_photos = found_photos + 1
                if num_of_images <= found_photos:
                    break

        sleep(1)

    return result

    # print(photos)
    # print(flickr.photos.getSizes(photo_id='50699751858'))
    # print("")
    # print(flickr.photos.getInfo(photo_id='50699751858', secret='d04d7e5535'))
    # print("doit done")


def set_api_key(context, api_key, api_secret):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT profile_id FROM flickr_api WHERE profile_id = ?", (context.profile_id(),))
    conn.commit()

    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO flickr_api (profile_id, api_key, api_secret) VALUES (?, ?, ?)",
                    (context.profile_id(), api_key, api_secret))
    else:
        cur.execute("UPDATE flickr_api SET api_key = ?,api_secret = ? WHERE profile_id = ?",
                    (api_key, api_secret, context.profile_id(),))

    conn.commit()
    conn.close()


def get_api_key(context):
    profile_ids = get_profile_hierarchy(context)

    conn = context.connection()
    cur = conn.cursor()

    api_key = None
    api_secret = None

    for profile_id in profile_ids:
        cur.execute("SELECT api_key, api_secret FROM flickr_api WHERE profile_id = ? AND api_key <> ''", (profile_id,))
        conn.commit()
        row = cur.fetchone()
        if row:
            api_key = row[0]
            api_secret = row[1]

    conn.close()

    return api_key, api_secret


def _process_photo(context, photo):
    fd, filename = mkstemp()
    os.close(fd)

    print(photo)
    print("========================")

    if not photo['url_o']:
        print("No link to origin size, ignoring photo")
        return None

    print("downloading from", photo['url_o'], "to", filename)
    urllib.request.urlretrieve(photo['url_o'], filename)

    return ImageDescriptor(filename=filename, width=photo['width_o'], height=photo['height_o'])
