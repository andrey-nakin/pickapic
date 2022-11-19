import flickrapi
from pickapic.profile import get_profile_hierarchy


def doit(context):
    api_key, api_secret = get_api_key(context)
    min_width, min_height = context.min_dimensions()

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    licenses = flickr.photos.licenses.getInfo()
    # print(licenses)

    photos = flickr.photos.search(tags='krasnodar', tag_mode='any', privacy_filter=1, safe_search=1, content_type=1,
                                  media='photos',
                                  extras='license, owner_name, tags, machine_tags, date_upload, o_dims, url_o',
                                  sort='date-posted-asc',
                                  license='1,2,3,4,5,6,7,9,10',
                                  min_upload_date=1607437583,
                                  per_page='10')
    print(photos)
    print(flickr.photos.getSizes(photo_id='50699751858'))
    print("")
    print(flickr.photos.getInfo(photo_id='50699751858', secret='d04d7e5535'))
    print("doit done")


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
