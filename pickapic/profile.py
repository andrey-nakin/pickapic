from .utils import panic


def create_profile(context):
    profile_name = "global"
    parent_name = None

    if find_profile_id_by_name(context, profile_name) is not None:
        panic("Profile already exists: " + profile_name)

    if parent_name is None:
        parent_id = None
    else:
        parent_id = find_profile_id_by_name(context, parent_name, True)

    conn = context.connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO profile (parent_id, name) VALUES (?, ?)", (parent_id, profile_name,))
    conn.commit()
    profile_id = cur.lastrowid
    conn.close()

    return profile_id


def find_profile_id_by_name(context, name, required=False):
    conn = context.connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM profile WHERE name = ?", (name,))
    conn.commit()

    row = cur.fetchone()
    if not row:
        if required:
            panic("Profile does not exist: " + name)
        result = None
    else:
        result = row[0]

    conn.close()
    return result
