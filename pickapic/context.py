import sqlite3
from .profile import find_profile_id_by_name


class Context:

    def __init__(self, args):
        self.args = args
        self.cached_profile_id = None

    def connection(self):
        return sqlite3.connect(self.args.config)

    def profile_id(self):
        if self.cached_profile_id is None:
            assert self.args.profile is not None

            self.cached_profile_id = find_profile_id_by_name(self, self.args.profile, True)

            conn = self.connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM profile WHERE name = ?", (self.args.profile,))
            conn.commit()

            row = cur.fetchone()
            if not row:
                cur.execute("INSERT INTO profile (name) VALUES (?)", (self.args.profile,))
                conn.commit()
                self.cached_profile_id = cur.lastrowid
            else:
                self.cached_profile_id = row[0]

            conn.close()

        return self.cached_profile_id
