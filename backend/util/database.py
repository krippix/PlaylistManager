import dataclasses
from datetime import datetime
from datetime import timezone
import sqlite3

import json
from pathlib import Path

from backend.objects.user import User


class Cursor:
    """
    Wrapper around sqlite3 cursor, to allow 'with' syntax.
    """
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def __enter__(self) -> sqlite3.Cursor:
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, *_):
        self.cursor.close()
        self.conn.commit()


class Database:
    def __init__(self):
        self.DB_FOLDER = Path(__file__).parent.parent / 'data'
        self.conn = sqlite3.connect(self.DB_FOLDER / 'database.sqlite')
        self.__ensure_tables()

    def cursor(self):
        return Cursor(self.conn)

    def __ensure_tables(self):
        """
        Creates all missing tables in the database.
        """
        with open(self.DB_FOLDER / 'sqlite3_conf.json', 'r') as f:
            schema_dict = json.load(f)

        with Cursor(self.conn) as cur:
            tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

            for key, value in schema_dict.items():
                if key not in [table[0] for table in tables]:
                    cur.execute(value)
                    print(f'Created table {key}')

    # -- USER ----------------------------------------------------------------------------------------------------------
    def set_user(self, user_id, **kwargs):
        """
        Creates new user in spotify database, overwrites existing user settings.
        """
        # remove non-existent fields
        user_fields = [field.name for field in dataclasses.fields(User)]
        input_dict = {key: value for key, value in kwargs.items() if key in user_fields}

        # get existing user data and overwrite with provided information
        user_exists = False
        if user := self.get_user(user_id):
            user_exists = True
            user_dict = dataclasses.asdict(user)
        else:
            user_dict = {"user_id": user_id}
        user_dict.update(input_dict)

        # commit to database
        with Cursor(self.conn) as cur:
            if user_exists:
                update_str = ",".join([f"{key}=?" for key in user_dict.keys()])
                update_values = tuple(list(user_dict.values()) + [user_id])
                cur.execute(f'UPDATE users SET {update_str} WHERE user_id=?', update_values)
            else:
                user_fields = ",".join(list(user_dict.keys()))
                user_values = tuple(user_dict.values())
                cur.execute(
                    f'INSERT INTO users ({user_fields}) '
                    f'VALUES ({("?," * len(user_values))[:-1]})',
                    user_values
                )

    def get_user(self, user_id: str) -> User | None:
        with Cursor(self.conn) as cur:
            user_fields = [field.name for field in dataclasses.fields(User)]
            db_result = cur.execute(
                f'SELECT {",".join(user_fields)} FROM users WHERE user_id=?', (user_id,)).fetchone()
        if not db_result:
            return None
        return User(**dict(zip(user_fields, db_result)))

    # -- TOKEN ---------------------------------------------------------------------------------------------------------
    def set_token(self, user_id: str, token: dict):
        """
        Writes token to a user entry in the database.
        """
        if not self.get_user(user_id):
            raise ValueError(f"Failed to set token: User '{user_id}' does not exist.")
        data = token.copy()
        data['user_id'] = user_id
        with Cursor(self.conn) as cur:
            cur.execute(
                'UPDATE users SET access_token=:access_token, token_type=:token_type, expires_in=:expires_in, '
                'refresh_token=:refresh_token, scope=:scope, expires_at=:expires_at '
                'WHERE user_id=:user_id', data
            )

    def get_token(self, user_id: str) -> dict | None:
        """
        Returns auth dict if user exits
        """
        if not (user := self.get_user(user_id)):
            return None
        return {
            'access_token': user.access_token,
            'token_type': user.token_type,
            'expires_in': user.expires_in,
            'refresh_token': user.refresh_token,
            'scope': user.scope,
            'expires_at': user.expires_at,
        }

    # -- CALLBACK KEY --------------------------------------------------------------------------------------------------
    def set_callback_key(self, key: str, max_age: int):
        """
        Writes a one time use callback key into the database to confirm weather a user is allowed to use /callback
        """
        with Cursor(self.conn) as cur:
            cur.execute("INSERT INTO callbacks (callback_key, max_age) VALUES (?, ?)", (key, max_age))

    def valid_callback_key(self, key: str) -> bool:
        """
        Takes callback key as input and checks if it is valid.
        Deletes the key from the database.
        """
        with Cursor(self.conn) as cur:
            cur.execute("SELECT callback_key,max_age FROM callbacks WHERE callback_key=?", (key,))
            result = cur.fetchone()
        if not result:
            return False
        # Check if timestamp is valid
        current_time = int(datetime.now(timezone.utc).timestamp())
        if result[1] > current_time:
            self.__delete_callback_key(key)
            return False
        # delete entry from database
        self.__delete_callback_key(key)
        return True

    def __delete_callback_key(self, key: str):
        """
        Removes callback key from database.
        """
        with Cursor(self.conn) as cur:
            cur.execute("DELETE FROM callbacks WHERE callback_key=?", (key,))
