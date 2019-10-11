import sqlite3


class AbstractModel():

    def __init__(self):
        self.db = sqlite3.connect("db/dev1.db")
        self._ensure_tables()

    def _ensure_tables(self):
        pass
