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
    # getter

    def get_track(self, track: str | objects.track.Track) -> objects.track.Track | None:
        '''Returns track with provided id. Tracks within db are expected to contain artist information!'''

        if not isinstance(track, str):
            id = track.get_id()
        else:
            id = track

        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM tracks WHERE id_pkey=?",(id,)).fetchall()
        

        if len(db_result) == 0:
            return None

        result = objects.track.Track(id=db_result[0][0],name=db_result[0][1],timestamp=db_result[0][2],artists=self.get_track_artists(id))
        result.set_artists(self.get_track_artists(result))


    def get_track_artists(self, track: objects.track.Track | str) -> list[objects.artist.Artist]:
        '''Returns artists involved with given track'''
        result_list = []

        if not isinstance(track, str):
            id = track.get_id()
        else:
            id = track

        db_result = self.db_cur.execute("SELECT artists_id_fkey from tracks_artists WHERE tracks_id_fkey=?",(id,)).fetchall()

        for item in db_result:
            next_result = self.get_artist(item[0])
            next_result.set_genres(next_result)
            result_list.append(next_result)
        
        return result_list


    def get_artist(self, id: str) -> objects.artist.Artist | None:
        '''Returns artist in database based on spotify id. Empty string for all artists.'''
        
        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM artists WHERE id_pkey == ?", (id,)).fetchall()
        
        if len(db_result) == 1:
            return objects.artist.Artist(id=db_result[0][0], name=db_result[0][1], timestamp=db_result[0][2])
        else:
            return None
    
    def get_all_artists(self) -> list[objects.artist.Artist]:
        '''Returns all artists present in the database.'''
        result_list = []
        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM artists").fetchall()
        
        for item in db_result:
            next_artist = objects.artist.Artist(id=item[0], name=item[1], timestamp=item[2])
            next_artist.set_genres(self.get_artist_genres())
            result_list.append(next_artist)
        

    def get_artist_genres(self, artist: objects.artist.Artist) ->  list[str]:
        '''Returns genres of provided artist in database.'''
        result_list = []
        db_result = self.db_cur.execute("SELECT genres.name FROM genres JOIN genres ON genres.id_pkey=artists_genres.genres_id_fkey WHERE artists.id_pkey=?", (artist.get_id(),)).fetchall()
        for item in db_result:
            print(f"Found genre: {item}")
            result_list.append(item)

        return result_list


    def get_library(self, user_id: str) -> list[objects.track.Track]:
        '''Returns song in provided users library'''
        #db_result = self.db_cur.execute("SELECT tracks.id_pkey,tracks.name").fetchall()

    ################
    # modifications

    def add_artist(self, artist: objects.artist.Artist):
        '''Adds artist to the database. Updates if artist already exists.'''
        timestamp = int(time.time())

        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM artists WHERE id_pkey == ?", (artist.get_id(),)).fetchall()

        if len(db_result) == 0:
            self.db_cur.execute("INSERT INTO artists (id_pkey,name,timestamp) VALUES (?,?,?)",(artist.get_id(), artist.get_name(), timestamp))
        else:
            self.db_cur.execute("UPDATE artists SET name = ?, timestamp = ? WHERE id_pkey = ?",(artist.get_name(), timestamp, artist.get_id()))
        
        # TODO handle genres for provided artist

        self.db_con.commit()


    def attach_artist(self, track: objects.track.Track) -> objects.track.Track:
        '''Takes song object and adds (local) artist information to it.'''
        #TODO db_result = self.db_cur.execute("SELECT ").fetchall()


    def add_track(self, track: objects.track.Track):
        '''Adds track to the database. Updates if it already exists. Artist data must be provided!'''
        timestamp = int(time.time())

        # attempt to pull track with given track id from database
        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM tracks WHERE id_pkey == ?", (track.get_id(),)).fetchall()

        # if nothing is found, simply add the new song into the db, else update entry
        if len(db_result) == 0:
            self.db_cur.execute("INSERT INTO tracks (id_pkey,name,timestamp) VALUES (?,?,?)", (track.get_id(), track.get_name(), timestamp))
        else:
            self.db_cur.execute("UPDATE tracks SET name = ?, timestamp = ? WHERE id_pkey = ?", (track.get_name(), timestamp, track.get_id()))
        
        # now ensure all involved artists also exist within the database
        rebuild_track_artists = False
        db_result = self.db_cur.execute("SELECT artists_id_fkey FROM tracks_artists WHERE tracks_id_fkey=?",(track.get_id(),)).fetchall()
        
        for artist in track.get_artists():
            self.add_artist(artist)

            # Check if song has same amount of artists
            if len(db_result) == len(track.get_artists()):
                if artist.get_id() not in db_result:
                    rebuild_track_artists = True
            else:
                rebuild_track_artists = True

        if rebuild_track_artists:
            self.db_cur.execute("DELETE FROM tracks_artists WHERE tracks_id_fkey=?",(track.get_id(),))
            for artist in track.get_artists():
                self.db_cur.execute("INSERT INTO tracks_artists (tracks_id_fkey,artists_id_fkey) VALUES (?,?)",(track.get_id(),artist.get_id()))
        self.db_con.commit()

        
    def add_user(self, user_id: str, display_name: str):
        '''Adds user to the database'''

    def add_playlist(self, playlist: objects.playlist.Playlist):
        '''Adds playlist to the database'''


if __name__ == "__main__":
    logging.error("This file is not supposed to be executed.")
    exit()