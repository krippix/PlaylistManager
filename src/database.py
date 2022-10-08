import logging, sqlite3
from util import config

class Database:
    '''This class manages the database of this Project'''
    
    db_con: sqlite3.Connection
    db_cur: sqlite3.Cursor
    

    def __init__(self, settings: config.Config):
        '''Connects to the existing database, or creates it anew.'''
        self.db_con = sqlite3.connect(settings.get_dbpath())
        self.db_cur = self.db_con.cursor()

        if not self.is_valid():
            self._create_default_tables()
    

    def is_valid(self):
        '''Checks if the database contains all required tables'''
        return False # lol
    

    def _create_default_tables(self):
        '''Creates default tables for database'''
        # users
        self.db_cur.execute("CREATE TABLE users(id_pkey TEXT NOT NULL PRIMARY KEY, displayname TEXT)")
        # songs
        self.db_cur.execute("CREATE TABLE songs(id_pkey TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL)")
        # playlists
        self.db_cur.execute("CREATE TABLE playlists(id_pkey TEXT NOT NULL PRIMARY KEY, users_id_fkey TEXT NOT NULL, name TEXT NOT NULL, genres_id_fkey, isgenreplaylist INTEGER, FOREIGN KEY (users_id_fkey) REFERENCES users (id_pkey), FOREIGN KEY (genres_id_fkey) REFERENCES genres (id_pkey))")
        # genres
        self.db_cur.execute("CREATE TABLE genres(id_pkey INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL UNIQUE)")
        #library
        self.db_cur.execute("CREATE TABLE libraries(users_id_fkey TEXT NOT NULL, songs_id_fkey TEXT NOT NULL, FOREIGN KEY (users_id_fkey) REFERENCES users (id_pkey), FOREIGN KEY (songs_id_fkey) REFERENCES songs (id_pkey))")
        # playlists_content
        self.db_cur.execute("CREATE TABLE playlists_content(playlists_id_fkey TEXT, songs_id_fkey, FOREIGN KEY (playlists_id_fkey) REFERENCES playlists (id_pkey), FOREIGN KEY (songs_id_fkey) REFERENCES songs (id_pkey))")
        # playlist_genres
        self.db_cur.execute("CREATE TABLE playlists_genres(playlists_id_fkey TEXT, genres_id_fkey INTEGER, FOREIGN KEY (playlists_id_fkey) REFERENCES playlists (id_pkey), FOREIGN KEY (genres_id_fkey) REFERENCES genres (id_pkey))")


    def exists_table(self, tablename):
        '''Checks if table exist within database'''
        result = self.db_cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name = ?;", (tablename,))
        result_list = result.fetchall()

        if len(result_list) == 0:
            return False
        if len(result_list) == 1:
            return True
        logging.critical("Table appears to exist multiple times. Database may be inconsistent.")


    def test(self):
        #print("creating test table with content")
        #self.db_cur.execute("CREATE TABLE test(eins,zwei,drei)")
        #self.db_cur.execute("INSERT INTO test (eins,zwei,drei) VALUES (1,2,3)")

        #print("pulling from test table")
        #result = self.db_cur.execute("SELECT * FROM test")
        #list = result.fetchall()
        #print(list)

        if self.exists_table("Test"):
            print("Yeet")
        else:
            print("Nicht yeet :(")


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()