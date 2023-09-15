import sqlite3
from pickapic.profile import find_profile_id_by_name
from pickapic.utils import panic
from pickapic.dimension import get_min_dimensions
from pickapic.tag import get_tags


class Context:

    def __init__(self, args):
        self.args = args
        self.cached_profile_id = None
        self.cached_min_width = None
        self.cached_min_height = None
        self.cached_tags = None
        self.cached_stop_tags = None

    def connection(self):
        return sqlite3.connect(self.args.config)

    def profile_id(self):
        if self.cached_profile_id is None:
            if self.args.profile is None:
                panic("Current profile is not specified")
            self.cached_profile_id = find_profile_id_by_name(self, self.args.profile, True)

        return self.cached_profile_id

    def min_dimensions(self):
        if self.cached_min_width is None:
            self.cached_min_width, self.cached_min_height = get_min_dimensions(self)
        return self.cached_min_width, self.cached_min_height

    def tags(self):
        if self.args.tags is not None:
            return self.args.tags
        if self.cached_tags is None:
            self.cached_tags = get_tags(self, False)
        return self.cached_tags

    def stop_tags(self):
        if self.cached_stop_tags is None:
            self.cached_stop_tags = get_tags(self, True)
        return self.cached_stop_tags
