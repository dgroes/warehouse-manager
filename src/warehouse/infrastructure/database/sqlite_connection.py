import sqlite3


class SQLiteConnection:

    def __init__(self, database_path: str):
        self._database_path = database_path

    def connect(self):
        conn =  sqlite3.connect(self._database_path)
        return conn