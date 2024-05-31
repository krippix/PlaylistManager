import sqlite3

import json
from pathlib import Path


class Database:
    def __init__(self):
        self.DB_FOLDER = Path(__file__).parent.parent / 'data'
        print(self.DB_FOLDER / 'database.sqlite')
        self.conn = sqlite3.connect(self.DB_FOLDER / 'database.sqlite')
        self.__ensure_tables()

    def __ensure_tables(self):
        """
        Creates all missing tables in the database.
        """
        with open(self.DB_FOLDER / 'sqlite3_conf.json', 'r') as f:
            schema_dict = json.load(f)

        cur = self.conn.cursor()
        tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

        for key, value in schema_dict.items():
            if key not in [x[0] for x in tables]:
                cur.execute(value)
                print(f'Created table {key}')
        cur.close()
