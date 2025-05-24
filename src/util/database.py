import logging, sqlite3
from typing import Tuple
from util import config

class Database:
    '''This class manages the database of this Project'''
    
    db_con: sqlite3.Connection
    db_cur: sqlite3.Cursor
    

    def __init__(self, settings: config.Config):
        '''Connects to the existing database, or creates it anew.'''
        self.db_con = sqlite3.connect(settings.get_dbpath())
        self.db_cur = self.db_con.cursor()

        self._ensure_default_tables()
    

    def is_valid(self):
        '''Checks if the database contains all required tables'''
        return False # lol
    

    def _ensure_default_tables(self):
        '''Checks if (default)table exists within database, creates it if it was missing.'''
        default_tables = {
            # 1st layer (no dependencies)
            "users": "CREATE TABLE users(id_pkey TEXT NOT NULL PRIMARY KEY, displayname TEXT)", # ToDo: include spotify authentication
            "songs": "CREATE TABLE songs(id_pkey TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL)",
            "artists": "CREATE TABLE artists(id_pkey TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL)",
            "genres": "CREATE TABLE genres(id_pkey INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL UNIQUE)",
            # 2nd layer (regular dependencies)
            "playlists": "CREATE TABLE playlists(id_pkey TEXT NOT NULL PRIMARY KEY, users_id_fkey TEXT NOT NULL, name TEXT NOT NULL, genres_id_fkey, isgenreplaylist INTEGER, FOREIGN KEY (users_id_fkey) REFERENCES users (id_pkey), FOREIGN KEY (genres_id_fkey) REFERENCES genres (id_pkey))",
            # intersection tables
            "libraries": "CREATE TABLE libraries(users_id_fkey TEXT NOT NULL, songs_id_fkey TEXT NOT NULL, FOREIGN KEY (users_id_fkey) REFERENCES users (id_pkey), FOREIGN KEY (songs_id_fkey) REFERENCES songs (id_pkey))",
            "playlists_content": "CREATE TABLE playlists_content(playlists_id_fkey TEXT, songs_id_fkey, FOREIGN KEY (playlists_id_fkey) REFERENCES playlists (id_pkey), FOREIGN KEY (songs_id_fkey) REFERENCES songs (id_pkey))",
            "playlists_genres": "CREATE TABLE playlists_genres(playlists_id_fkey TEXT, genres_id_fkey INTEGER, FOREIGN KEY (playlists_id_fkey) REFERENCES playlists (id_pkey), FOREIGN KEY (genres_id_fkey) REFERENCES genres (id_pkey))",
            "songs_artists": "CREATE TABLE songs_artists(songs_id_fkey TEXT, artists_id_fkey TEXT, FOREIGN KEY (songs_id_fkey) REFERENCES songs (id_pkey), FOREIGN KEY (artists_id_fkey) REFERENCES artists (id_pkey))",
            "artists_genres": "CREATE TABLE artists_genres(artists_id_fkey TEXT, genres_id_fkey INTEGER, FOREIGN KEY (artists_id_fkey) REFERENCES artists (id_pkey), FOREIGN KEY (genres_id_fkey) REFERENCES genres (id_pkey))"
        }
        
        for table in default_tables.keys():
            if not self.exists_table(table):
                logging.info("Table {table} is missing. Creating...")
                self.db_cur.execute(default_tables[table])
        
        
    def exists_table(self, tablename):
        '''Checks if table exist within database'''
        result = self.db_cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name = ?;", (tablename,))
        result_list = result.fetchall()

        if len(result_list) == 0:
            return False
        if len(result_list) == 1:
            return True
        logging.critical("Table appears to exist multiple times. Database may be inconsistent.")


    def add_song(self, song: Tuple):
        '''Adds song to the "songs" database. (overwrites if it already exists)'''
        


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()