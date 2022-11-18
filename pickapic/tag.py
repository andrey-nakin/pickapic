def tag_exists(context, tag):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM tag WHERE profile_id = ? AND name = ?", (context.profile_id(), tag,))
    conn.commit()

    row = cur.fetchone()
    result = False if not row else True

    conn.close()
    return result


def add_tags(context, tags, is_stop):
    conn = context.connection()
    cur = conn.cursor()

    for tag in tags:
        cur.execute("DELETE FROM tag WHERE profile_id = ? AND name = ?", (context.profile_id(), tag,))
        cur.execute("INSERT INTO tag (profile_id, name, is_stop) VALUES (?, ?, ?)",
                    (context.profile_id(), tag, 1 if is_stop else 0,))

    conn.commit()
    conn.close()


def remove_tags(context, tags, is_stop):
    conn = context.connection()
    cur = conn.cursor()

    for tag in tags:
        cur.execute("DELETE FROM tag WHERE profile_id = ? AND name = ? AND is_stop = ?",
                    (context.profile_id(), tag, 1 if is_stop else 0))

    conn.commit()
    conn.close()


def list_tags(context, is_stop):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM tag WHERE profile_id = ? AND is_stop = ? ORDER BY name",
                (context.profile_id(), 1 if is_stop else 0,))
    conn.commit()

    rows = cur.fetchall()
    for row in rows:
        print(row[0])

    conn.close()
