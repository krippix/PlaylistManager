# external
# python native
import logging
import oracledb
from oracledb.exceptions import OperationalError, DatabaseError
# project
from Gustelfy.database import interface
from Gustelfy.objects import album, artist, playlist, track, user
from Gustelfy.util import config

class OracleCon(interface.Interface):
    """Connection to oracle database
    """

    # ---- Getter Functions ----

    def get_album(self, id: str) -> album.Album | None:
        """Returns album filled with tracks from the database

        Args:
            id (str): spotify id of the album

        Returns:
            album.Album | None: Album, or None if no result found
        """
        album_result = self.cursor.execute("SELECT id_pkey,name,image_url,timestamp,release_date FROM ALBUMS WHERE id_pkey=:id", id=id).fetchall()
        if not album_result:
            return None
        result = album.Album(
            id=album_result[0][0],
            name=album_result[0][1],
            tracks=self.__get_album_tracks(id),
            artists=self.__get_album_artists(id),
            timestamp=album_result[0][3]
        )
        result.set_image_url(album_result[0][2])
        result.set_release_date(album_result[0][4])
        return result

    def __get_album_artists(self, album_id: str) -> list[artist.Artist]:
        """Gets list of artists associated with the given ID from the database

        Args:
            album_id (str): album's spotify ID

        Returns:
            list[artist.Artist]: list of Artist objects
        """
        db_result = self.cursor.execute("SELECT artists_id_fkey FROM album_artists WHERE album_id_fkey=:album_id",album_id=album_id).fetchall()
        artist_list = []
        for db_artist in db_result:
            artist_list.append(self.get_artist(db_artist[0]))
        return artist_list

    def __get_album_tracks(self, album_id: str) -> list[track.Track]:
        """Returns list associated with the given Album ID from the database

        Args:
            album_id (str): Spotify API is String

        Returns:
            list[track.Track]: list of track objects
        """
        db_result = self.cursor.execute("SELECT tracks_id_fkey FROM album_content WHERE albums_id_fkey = :album_id",album_id=album_id).fetchall()
        track_list = []
        for trk in db_result:
            track_list.append(self.get_track(trk[0]))
        return track_list

    def get_artist(self, id) -> artist.Artist | None:
        result = self.cursor.execute("SELECT id_pkey,name,image_url,timestamp FROM artists WHERE id_pkey=:id_pkey",id_pkey=id).fetchall()
        if not result:
            return None
        artist_result = artist.Artist(
            id=result[0][0],
            name=result[0][1],
            genres=self.__get_artist_genres(id),
            timestamp=result[0][3]
        )
        artist_result.set_image_url(result[0][2])
        return artist_result

    def __get_artist_genres(self, artist_id) -> list[str]:
        result = self.cursor.execute("SELECT genres_id_fkey FROM artist_genres WHERE artists_id_fkey=:artist_id",artist_id=artist_id)
        genre_list = []
        for genre in result:
            genre_list.append(genre[0])
        return genre_list

    def get_favorites(self, user_id) -> list[track.Track]:
        pass

    def get_genres(self, artist_id) -> list[str]:
        pass

    def get_playlist(self, id) -> playlist.Playlist:
        pass

    def get_track(self, id: str) -> track.Track | None:
        pass    

    def get_user(self, id: str) -> user.User | None:
        pass

    # ---- Setter Functions ----

    def __set_artist_genres(self, artist: artist.Artist):
        """Sets genres associated with the given artist to the values defined in the given object

        Args:
            artist (Artist): artist object
        """
        result = self.cursor.execute("SELECT genres_id_fkey FROM artist_genres WHERE artists_id_fkey=:id",id=artist.get_id()).fetchall()
        db_genres = []
        for genre in result:
            db_genres.append(genre[0])
        
        # Check if on- and offline version are equal
        overlap = [db_genre for db_genre in db_genres for online_genre in artist.get_genres() if db_genre == online_genre]
        if len(overlap) == len(artist.get_genres()):
            return
        
        # Reset association
        self.cursor.execute("DELETE FROM artist_genres WHERE artists_id_fkey = :id",id=artist.get_id())

        # Put new ones in
        for genre in artist.get_genres():
            self.cursor.execute("INSERT INTO artist_genres (artists_id_fkey,genres_id_fkey) VALUES (:artist_id,:genre)",artist_id=artist.get_id(),genre=genre)
        self.connection.commit()
        
    # ---- Other Functions ----

    def connect_database(self):

        # There has to be a better way
        # https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html#ic_winx64_inst
        oracledb.init_oracle_client(lib_dir="C:\Program Files\Oracle\instantclient_21_8")
        try:
            self.logger.info("Connecting to oracle database...")
            self.connection = oracledb.connect(
                user=self.settings.get_config("ORACLEDB","username"),
                password=self.settings.get_config("ORACLEDB","password"),
                host=self.settings.get_config("ORACLEDB","host"),
                port=int(self.settings.get_config("ORACLEDB","port")),
                sid=self.settings.get_config("ORACLEDB","sid")
            )
            self.logger.info("Connection successful!")
        except OperationalError as e:
            self.logger.critical(f"Failed to connect to oracle database: {e}")
            exit()
        except DatabaseError as e:
            self.logger.critical(f"Failed to connect to oracle database: {e}")
            exit()
        self.cursor = self.connection.cursor()


    # -- add --

    def add_album(self, album: album.Album):
        """Adds Album, it's tracks and artists into the database

        Args:
            album (album.Album): Spotify Album object
        """
        # Add artists and track into the database
        for artist in album.get_artists():
            self.add_artist(artist)
        for track in album.get_tracks():
            self.add_track(track)
        # Check if existing album is the same
        if self.get_album(album.get_id()) is not None:
            self.__update_album(album)
            return
        # Add new album and associations into the database
        self.cursor.execute(
            "INSERT INTO albums (id_pkey,name,image_url,timestamp,release_date) VALUES (:id,:name,:url,:timestamp,:release_date)",
            id=album.get_id(),
            name=album.get_name(),
            url=album.get_image_url(),
            timestamp=album.get_timestamp(),
            release_date=album.get_release_date()
        )
        # Add tracks to album
        for trk in album.get_tracks():
            self.connection.commit(
                "INSERT INTO album_content (albums_id_fkey,tracks_id_fkey) VALUES (:album_id,:track_id)",
                album_id=album.get_id(),
                track_id=trk.get_id()
            )
        for art in album.get_artists():
            self.connection.commit(
                "INSERT INTO album_artists (albums_id_fkey,artists_id_fkey) VALUES (:album_id,:artist_id)",
                album_id=album.get_id(),
                artist_id=art.get_id()
            )
        self.conneciton.commit()

    def add_artist(self, artist: artist.Artist):
        """adds artist and their accociated genre into the database.

        Args:
            artist (artist.Artist): Spotify Artist object
        """
        # Ensure genres exist in the database
        for genre in artist.get_genres():
            self.add_genre(genre)

        # Check if artist is already in the database
        if self.get_artist is not None:
            self.__update_artist(artist)
            return
        
        # Write artist into the database
        self.cursor.execute(
            "INSERT INTO artists (id_pkey,name,image_url,timestamp) VALUES (:id_pkey,:name,:image_url,:timestamp)",
            id_pkey=artist.get_id(),
            name=artist.get_name(),
            image_url=artist.get_image_url(),
            timestamp=artist.get_timestamp()
        )
        # Set artist <-> genres association
        self.__set_artist_genres(artist)

        # commit changes
        self.connection.commit()

    def add_favorite(self, user: user.User, track: track.Track):
        """Adds favorite track association into database, and track if it isn't there yet.

        Args:
            user (user.User): User who likes that track
            track (track.Track): track that the user likes
        """
        self.add_track(track)
        result = self.cursor.execute("SELECT (tracks_id_fkey) FROM favorites WHERE users_id_fkey = :user_id",user_id=user.get_id()).fetchall()
        id_list = []
        for favorite in result:
            id_list.append(favorite[0])
        if track.get_id() in id_list:
            return
        self.cursor.execute("INSERT INTO favorites (tracks_id_fkey,users_id_fkey) VALUES (:track_id,:user_id)",track_id=track.get_id(),user_id=user.get_id())
        self.connection.commit()

    def add_genre(self, genre: str):
        # Check if genre already exists
        if self.cursor.execute("SELECT * FROM GENRES WHERE name = :name",name=genre).fetchall():
            return
        else:
            self.cursor.execute("INSERT INTO GENRES (name) VALUES (:genre)",genre=genre)
            self.connection.commit()

    def add_playlist(self, playlist: playlist.Playlist):
        """Adds Playlist to the database, updates existing one.

        Args:
            playlist (playlist.Playlist): Playlist to save locally
        """
        # Check if playlist already exists
        if self.get_playlist(playlist.get_id()) is not None:
            self.__update_playlist(playlist)
            return
        # Check if user exists
        if self.get_user is None:
            self.add_user(playlist.get_owner_id())
        # Add playlist to the database
        self.cursor.execute(
            "INSERT INTO playlists (id_pkey,users_id_fkey,name,description,image_url,timestamp,is_managed) VALUES (:id,:owner_id,:name,:desc,:url,:timestamp,:is_managed)",
            id=playlist.get_id(),
            owner_id=playlist.get_owner_id(),
            name=playlist.get_name(),
            desc=playlist.get_description(),
            url=playlist.get_image_url(),
            timestamp=playlist.get_description(),
            is_managed=playlist.is_managed()
        )
        # Add tracks to the playlist
        for track in playlist.get_tracks():
            self.add_track()
            self.cursor.execute(
                "INSERT INTO favorites (users_id_fkey,tracks_id_fkey) VALUES (:user_id,:track_id)",
                user_id=playlist.get_owner_id(),
                track_id=track.get_id()
            )
        self.connection.commit()

    def add_track(self, track: track.Track):
        # Check if track already exists
        if self.cursor.execute("SELECT (id_pkey) FROM tracks WHERE id_pkey=:id_pkey",id_pkey=track.get_id()):
            #update track
            pass
        else:
            self.cursor.execute(
                "INSERT INTO tracks (id_pkey,name,duration_ms,disc_number,explicit,timestamp) VALUES (:id_pkey,:name,:duration_ms,:disc_number,:explicit,:timestamp)",
                id_pkey=track.get_id(),
                name=track.get_name(),
                duration_ms=track.get_duration(),
                disc_number=track.get_disc_number(),
                explicit=track.is_explicit(),
                timestamp=track.get_timestamp()
            )
        for artist in track.get_artists():
            add_artist(artist)
            # Check if artist <-> track relation already exists
            if self.cursor.execute("SELECT * from track_artists WHERE tracks_id_fkey=:track_id AND artists_id_fkey=:artist_id",track_id=track.get_id(),artist_id=artist.get_id()):
                continue
            else:
                self.cursor.execute(
                    "INSERT INTO tracks_artists (artists_id_fkey,tracks_id_fkey) VALUES (:artist_id,:track_id)",
                    artist_id=artist.get_id(),
                    track_id=track.get_id()
                )
        self.connection.commit()

    def add_user(self, user: user.User):
        """Adds user to the database

        Args:
            user (user.User): Spotify user object
        """
        # Handle actual user object
        if self.cursor.execute("SELECT * FROM users WHERE id_pkey = :id",id=user):
            self.__update_user(user)
            return
        # Input new user object
        self.cursor.execute(
            "INSERT INTO users (id_pkey,display_name,image_url,api_token,expires_at,email,timestamp)"+
            "VALUES (:id,:display_name,:image_url,:api_token,:expires_at,:email:,:timestamp)",
            id=user.get_id(),
            display_name=user.get_display_name(),
            image_url=user.get_image_url(),
            api_token=user.get_api_token(),
            expires_at=user.get_expires_at(),
            email=user.get_email(),
            timestamp=user.get_timestamp()
        )
        self.connection.commit()

    # -- Update --

    def __update_album(self, album: album.Album):
        if album == self.get_album(album.get_id()):
            #update timestamp
            self.cursor.execute("UPDATE albums SET timestamp=:time WHERE id_pkey=:id",time=album.get_timestamp(),id=album.get_id())
            self.conection.commit()
        else:
            # delete existing entries
            self.cursor.execute("DELETE FROM album_content WHERE album_id_fkey=:id",id=album.get_id())
            self.cursor.execute("DELETE FROM album_artists WHERE album_id_fkey=:id",id=album.get_id())
            self.cursor.execute("DELETE FROM albums WHERE id_pkey=:id",id=album.get_id())
            self.conection.commit()
            self.add_album(album)
        

    def __update_artist(self, artist: artist.Artist):
        self.cursor.execute(
            "UPDATE artists SET id_pkey=:id_pkey,name=:name,image_url=:image_url,timestamp=:timestamp",
            id_pkey=artist.get_id(),
            name=artist.get_name(),
            image_url=artist.get_image_url(),
            timestamp=artist.get_timestamp()
        )
        self.__set_artist_genres(artist)
        self.connection.commit()

    def __update_playlist(self, playlist: playlist.Playlist):
        pass

    def __update_track(self, track: track.Track):
        pass

    def update_favorites(self, delta: tuple[list[track.Track], list[track.Track]]):
        pass

    # -- Database integrity --

    def check(self):
        pass

    def create_database(self):
        pass

    def table_exists(self, table: str) -> bool:
        result = self.cursor.execute("SELECT table_name FROM user_tables WHERE table_name = :name", name=table).fetchall()
        if len(result) != 0:
            return True
        else:
            return False