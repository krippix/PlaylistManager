# external
import spotipy
# python native
import logging,sqlite3,time
# project
import util.config
import objects.artist, objects.track, objects.playlist

class Database:
    '''This class manages the database of this Project'''
    
    db_con: sqlite3.Connection
    db_cur: sqlite3.Cursor
    
    ###############
    # initial setup
    ###############

    def __init__(self):
        '''Connects to the existing database, or creates it anew.'''
        settings = util.config.Config()
        self.db_con = sqlite3.connect(settings.get_dbpath())
        self.db_cur = self.db_con.cursor()
    

    def is_valid(self):
        '''Checks if the database contains all required tables'''
        return False # lol
    

    def ensure_default_tables(self):
        '''Checks if (default)table exists within database, creates it if it was missing.'''
        default_tables = {
            # 1st layer (no dependencies)
            "users": "CREATE TABLE users(id_pkey TEXT NOT NULL PRIMARY KEY, displayname TEXT, access_token TEXT, token_type TEXT, expires_in INTEGER, scope TEXT, expires_at INTEGER, refresh_token TEXT)",
            "tracks": "CREATE TABLE tracks(id_pkey TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL, timestamp INTEGER)",
            "artists": "CREATE TABLE artists(id_pkey TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL, timestamp INTEGER)",
            "genres": "CREATE TABLE genres(id_pkey INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL UNIQUE)",
            # 2nd layer (regular dependencies)
            "playlists": "CREATE TABLE playlists(id_pkey TEXT NOT NULL PRIMARY KEY, users_id_fkey TEXT NOT NULL, name TEXT NOT NULL, genres_id_fkey, isgenreplaylist INTEGER, FOREIGN KEY (users_id_fkey) REFERENCES users (id_pkey), FOREIGN KEY (genres_id_fkey) REFERENCES genres (id_pkey))",
            # intersection tables
            "libraries": "CREATE TABLE libraries(id_pkey INTEGER PRIMARY KEY, users_id_fkey TEXT NOT NULL, tracks_id_fkey TEXT NOT NULL, FOREIGN KEY (users_id_fkey) REFERENCES users (id_pkey), FOREIGN KEY (tracks_id_fkey) REFERENCES tracks (id_pkey))",
            "playlists_content": "CREATE TABLE playlists_content(id_pkey INTEGER PRIMARY KEY, playlists_id_fkey TEXT, tracks_id_fkey, FOREIGN KEY (playlists_id_fkey) REFERENCES playlists (id_pkey), FOREIGN KEY (tracks_id_fkey) REFERENCES tracks (id_pkey))",
            "playlists_genres": "CREATE TABLE playlists_genres(id_pkey INTEGER PRIMARY KEY, playlists_id_fkey TEXT, genres_id_fkey INTEGER, FOREIGN KEY (playlists_id_fkey) REFERENCES playlists (id_pkey), FOREIGN KEY (genres_id_fkey) REFERENCES genres (id_pkey))",
            "tracks_artists": "CREATE TABLE tracks_artists(id_pkey INTEGER PRIMARY KEY, tracks_id_fkey TEXT, artists_id_fkey TEXT, FOREIGN KEY (tracks_id_fkey) REFERENCES tracks (id_pkey), FOREIGN KEY (artists_id_fkey) REFERENCES artists (id_pkey))",
            "artists_genres": "CREATE TABLE artists_genres(id_pkey INTEGER PRIMARY KEY, artists_id_fkey TEXT, genres_id_fkey INTEGER, FOREIGN KEY (artists_id_fkey) REFERENCES artists (id_pkey), FOREIGN KEY (genres_id_fkey) REFERENCES genres (id_pkey))"
        }
        
        for table in default_tables.keys():
            if not self.exists_table(table):
                logging.error(f"Table {table} is missing. Creating...")
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


    ################
    # getter-ish
    ################

    def get_artist(self, id: str) -> objects.artist.Artist | None:
        '''Returns artist in database based on spotify id.'''
        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM artists WHERE id_pkey == ?", (id,)).fetchall()
        
        if len(db_result) == 1:
            return objects.artist.Artist(id=db_result[0][0], name=db_result[0][1], timestamp=db_result[0][2])
        else:
            return None


    ################
    # modifications
    ################

    def add_artist(self, artist: objects.artist.Artist):
        '''Adds artist to the database. Updates if artist already exists.'''
        timestamp = int(time.time())

        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM artists WHERE id_pkey == ?", (artist.get_id(),)).fetchall()

        if len(db_result) == 0:
            self.db_cur.execute("INSERT INTO artists (id_pkey,name,timestamp) VALUES (?,?,?)",(artist.get_id(), artist.get_name(), timestamp))
        else:
            self.db_cur.execute("UPDATE artists SET name = ?, timestamp = ? WHERE id_pkey = ?",(artist.get_name(), timestamp, artist.get_id()))
        
        self.db_con.commit()
        

    def add_track(self, track: objects.track.Track):
        '''Adds track to the database. Updates if it already exists'''
        timestamp = int(time.time())

        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM tracks WHERE id_pkey == ?", (track.get_id(),)).fetchall()

        if len(db_result) == 0:
            self.db_cur.execute("INSERT INTO tracks (id_pkey,name,timestamp) VALUES (?,?,?)", (track.get_id(), track.get_name(), timestamp))
        else:
            self.db_cur.execute("UPDATE tracks SET name = ?, timestamp = ? WHERE id_pkey = ?", (track.get_name(), timestamp, track.get_id()))
        
        # now ensure all involved artists also exist within the database


        
    def add_user(self, user_id: str, display_name: str):
        '''Adds user to the database'''

    def add_playlist(self, playlist: objects.playlist.Playlist):
        '''Adds playlist to the database'''

    def ensure_artists(self, track: objects.track.Track):
        '''Provides track file with artist information either from local db or spotify api.'''
        db_con = util.database.Database()

        for artist in track.get_artists:
            db_con.get_artist(track.get_arti)

if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()