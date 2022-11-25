import flickrapi

from pickapic.utils import panic
from pickapic.profile import get_profile_hierarchy

from pickapic.flickr.apikey import flickr_get_api_key


def flickr_add_licenses(context, license_ids):
    conn = context.connection()
    cur = conn.cursor()

    for license_id in license_ids:
        cur.execute("SELECT license_id FROM flickr_license WHERE profile_id = ? AND license_id = ?",
                    (context.profile_id(), license_id,))
        conn.commit()

        row = cur.fetchone()
        if not row:
            cur.execute("INSERT INTO flickr_license (profile_id, license_id) VALUES (?, ?)",
                        (context.profile_id(), license_id,))

        conn.commit()

    conn.close()


def flickr_remove_licenses(context, license_ids):
    conn = context.connection()
    cur = conn.cursor()

    for license_id in license_ids:
        cur.execute("DELETE FROM flickr_license WHERE profile_id = ? AND license_id = ?",
                    (context.profile_id(), license_id,))
        conn.commit()

    conn.close()


def flickr_list_licenses(context):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT license_id FROM flickr_license WHERE profile_id = ? ORDER BY license_id",
                (context.profile_id(),))
    conn.commit()

    rows = cur.fetchall()
    for row in rows:
        print(row[0])

    conn.close()


def flickr_get_license_ids(context):
    profile_ids = get_profile_hierarchy(context)

    conn = context.connection()
    cur = conn.cursor()
    result = []

    for profile_id in profile_ids:
        cur.execute("SELECT license_id FROM flickr_license WHERE profile_id = ?", (profile_id,))
        conn.commit()
        rows = cur.fetchall()
        for row in rows:
            result.append(row[0])

    conn.close()

    return list(set(result))


def flickr_load_license_info(context):
    api_key, api_secret = flickr_get_api_key(context)

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    license_info = flickr.photos.licenses.getInfo()
    if license_info['stat'] != 'ok':
        panic("Flickr: error getting license info")
    if 'licenses' not in license_info:
        panic("Flickr: no licenses element in license info")
    if 'license' not in license_info['licenses']:
        panic("Flickr: no license element in license info")

    return license_info['licenses']['license']


def flickr_dump_licenses(context):
    print(flickr_load_license_info(context))
