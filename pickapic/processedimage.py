def add_image_to_processed(context, image_id):
    conn = context.connection()
    cur = conn.cursor()

    cur.execute("SELECT profile_id FROM processed_image WHERE profile_id = ? AND image_id = ?",
                (context.profile_id(), image_id,))
    conn.commit()

    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO processed_image (profile_id, image_id) VALUES (?, ?)",
                    (context.profile_id(), image_id))

    conn.commit()
    conn.close()


def is_image_processed(context, image_id):
    conn = context.connection()
    cur = conn.cursor()

    cur.execute("SELECT profile_id FROM processed_image WHERE profile_id = ? AND image_id = ?",
                (context.profile_id(), image_id,))
    conn.commit()

    row = cur.fetchone()
    result = True if row else False

    conn.commit()
    conn.close()

    return result
