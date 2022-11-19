from pickapic.profile import get_profile_hierarchy


def get_min_width(context):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT min_width FROM dimension WHERE profile_id = ?", (context.profile_id(),))
    conn.commit()

    row = cur.fetchone()
    result = row[0] if row else 0

    conn.close()
    print(result)


def set_min_width(context, value):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT profile_id FROM dimension WHERE profile_id = ?", (context.profile_id(),))
    conn.commit()

    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO dimension (profile_id, min_width) VALUES (?, ?)", (context.profile_id(), value,))
    else:
        cur.execute("UPDATE dimension SET min_width = ? WHERE profile_id = ?", (value, context.profile_id(),))

    conn.commit()
    conn.close()


def get_min_height(context):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT min_height FROM dimension WHERE profile_id = ?", (context.profile_id(),))
    conn.commit()

    row = cur.fetchone()
    result = row[0] if row else 0

    conn.close()
    print(result)


def set_min_height(context, value):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT profile_id FROM dimension WHERE profile_id = ?", (context.profile_id(),))
    conn.commit()

    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO dimension (profile_id, min_height) VALUES (?, ?)", (context.profile_id(), value,))
    else:
        cur.execute("UPDATE dimension SET min_height = ? WHERE profile_id = ?", (value, context.profile_id(),))

    conn.commit()
    conn.close()


def get_min_dimensions(context):
    profile_ids = get_profile_hierarchy(context)

    conn = context.connection()
    cur = conn.cursor()

    min_width = 0
    min_height = 0

    for profile_id in profile_ids:
        cur.execute("SELECT min_width, min_height FROM dimension WHERE profile_id = ?", (profile_id,))
        conn.commit()
        row = cur.fetchone()
        if row:
            if row[0] > 0:
                min_width = row[0]
            if row[1] > 0:
                min_height = row[1]

    conn.close()

    return min_width, min_height
