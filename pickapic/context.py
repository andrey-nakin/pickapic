import sqlite3


class Context:
    def __init__(self, args):
        self.args = args

    def connection(self):
        return sqlite3.connect(self.args.config)
