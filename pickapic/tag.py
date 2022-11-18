def tag_exists(context, tag):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM tag WHERE profile_id = ? AND name = ?", (context.profile_id(), tag,))
    conn.commit()

    row = cur.fetchone()
    result = False if not row else True

    conn.close()
    return result


def add_tags(context, tags):
    conn = context.connection()
    cur = conn.cursor()

    for tag in tags:
        if not tag_exists(context, tag):
            cur.execute("INSERT INTO tag (profile_id, name) VALUES (?, ?)", (context.profile_id(), tag))

    conn.commit()
    conn.close()


def remove_tags(context, tags):
    conn = context.connection()
    cur = conn.cursor()

    for tag in tags:
        cur.execute("DELETE FROM tag WHERE profile_id = ? AND name = ?", (context.profile_id(), tag))

    conn.commit()
    conn.close()


def list_tags(context):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM tag WHERE profile_id = ? ORDER BY name", (context.profile_id(),))
    conn.commit()

    rows = cur.fetchall()
    for row in rows:
        print(row[0])

    conn.close()
