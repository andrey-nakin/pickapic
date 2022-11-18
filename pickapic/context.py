import sqlite3
from .profile import find_profile_id_by_name
from .utils import panic


class Context:

    def __init__(self, args):
        self.args = args
        self.cached_profile_id = None

    def connection(self):
        return sqlite3.connect(self.args.config)

    def profile_id(self):
        if self.cached_profile_id is None:
            if self.args.profile is None:
                panic("Current profile is not specified")
            self.cached_profile_id = find_profile_id_by_name(self, self.args.profile, True)

        return self.cached_profile_id
