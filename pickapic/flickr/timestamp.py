from datetime import datetime


def flickr_get_min_timestamp(context):
    conn = context.connection()
    cur = conn.cursor()

    timestamp = None

    cur.execute("SELECT timestamp FROM flickr_min_timestamp WHERE profile_id = ?", (context.profile_id(),))
    conn.commit()
    row = cur.fetchone()
    if row:
        timestamp = row[0]

    conn.close()

    return timestamp


def flickr_set_min_timestamp(context, timestamp):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT profile_id FROM flickr_min_timestamp WHERE profile_id = ?", (context.profile_id(),))
    conn.commit()

    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO flickr_min_timestamp (profile_id, timestamp) VALUES (?, ?)",
                    (context.profile_id(), timestamp))
    else:
        cur.execute("UPDATE flickr_min_timestamp SET timestamp = ? WHERE profile_id = ?",
                    (timestamp, context.profile_id(),))

    conn.commit()
    conn.close()


def flickr_dump_min_timestamp(context):
    timestamp = flickr_get_min_timestamp(context)
    if timestamp is not None:
        print(datetime.fromtimestamp(timestamp))
    else:
        print("No stored Flickr min timestamp for the current profile")


def flickr_reset_min_timestamp(context):
    conn = context.connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM flickr_min_timestamp WHERE profile_id = ?", (context.profile_id(),))

    conn.commit()
    conn.close()

    print("Min timestamp was reset")
