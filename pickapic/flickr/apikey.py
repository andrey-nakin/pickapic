from pickapic.profile import get_profile_hierarchy


def flickr_get_api_key(context):
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


def flickr_set_api_key(context, api_key, api_secret):
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
