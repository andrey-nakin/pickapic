from .utils import panic


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


def create_profile(context, args):
    profile_name = args[0]
    parent_name = args[1] if len(args) > 1 else None

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

    print("Profile created:", profile_name)

    return profile_id


def delete_profile(context, profile_name):
    profile_id = find_profile_id_by_name(context, profile_name, True)

    conn = context.connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(id) FROM profile WHERE parent_id = ?", (profile_id,))
    conn.commit()
    row = cur.fetchone()
    if row[0] > 0:
        panic("Profile is used by other profiles: " + profile_name)

    cur.execute("DELETE FROM tag WHERE profile_id = ?", (profile_id,))
    cur.execute("DELETE FROM stop_tag WHERE profile_id = ?", (profile_id,))
    cur.execute("DELETE FROM min_dimension WHERE profile_id = ?", (profile_id,))
    cur.execute("DELETE FROM profile WHERE id = ?", (profile_id,))
    conn.commit()
    profile_id = cur.lastrowid
    conn.close()

    print("Profile deleted:", profile_name)

    return profile_id
