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

    def get_favorites(self, user_id: str) -> list[track.Track]:
        """Returns list of favorites listed in the offline db

        Args:
            user_id (str): Spotify user ID

        Returns:
            list[track.Track]: List of favorites
        """
        result = self.cursor.execute("SELECT tracks_id_fkey FROM favorites WHERE users_id_fkey=:id",id=user_id).fetchall()
        tracks = []
        for id in result:
            tracks.append(self.get_track(id[0]))
        return tracks

    def get_playlist(self, id: str, user_id: str) -> playlist.Playlist:
        """Returns a user playlist from local database

        Args:
            id (str): Spotify ID of the Playlist
            user_id (str): Spotify ID of the user using the playlist

        Returns:
            playlist.Playlist: Spotify Playlist object
        """
        # Get Playlist data from db
        db_playlist = self.cursor.execute(
            "SELECT creator_id,name,description,image_url,timestamp FROM playlists WHERE id_pkey=:id AND users_id_fkey=:user_id",
            id=id,
            user_id=user_id
        ).fetchall()
        if not db_playlist:
            return None
        # Get managed status for the playlist
        status = self.cursor.execute("SELECT is_managed FROM user_playlists WHERE playlists_id_fkey=:id AND users_id_fkey=:user_id",id=id, user_id=user_id).fetchall()
        # Get Playlist tracks from db
        db_tracks = self.cursor.execute(
            "SELECT tracks_id_pkey FROM playlist_content WHERE playlists_id_fkey=:id",
            id=id
        ).fetchall()
        tracks = []
        for track in db_tracks:
            tracks.append(self.get_track(track[0]))
        # Get Playlist genres from db
        genres = []
        db_genres = self.cursor.execute("SELECT genres_id_fkey FROM playlist_genres WHERE playlists_id_fkey=:id",id=id).fetchall()
        for genre in db_genres:
            genres.append(genre[0])
        # Create Playlist object
        playlist_result = playlist.Playlist(
            id=id,
            name=db_playlist[0][1],
            user_id=user_id,
            creator_id=db_playlist[0][0],
            tracks=tracks,
            managed=status[0][0],
            timestamp=db_playlist[0][4],
            description=db_playlist[0][2],
            image_url=db_playlist[0][3],
            genres=genres
        )
        return playlist_result

    def get_track(self, id: str) -> track.Track:
        """Returns Spotify Track object with its artists

        Args:
            id (str): Spotify ID of the track

        Returns:
            track.Track: Spotify Track object
        """
        # Get track from the database
        track_result = self.cursor.execute(
            "SELECT name,duration_ms,disc_number,explicit,timestamp FROM tracks WHERE id_pkey=:id",
            id=id
        ).fetchall()
        if not track_result:
            return None
        # Retrieve artists associated with this track
        artists_result = self.cursor.execute(
            "SELECT artists_id_fkey FROM track_artists WHERE tracks_id_fkey=:id",
            id=id
        ).fetchall()
        artists = []
        for artist_id in artists_result:
            artists.append(self.get_artist(artist_id[0]))
        # Create track object to return
        result = track.Track(
            id=id,
            name=track_result[0][0],
            artists=artists,
            timestamp=track_result[0][4],
            duration_ms=track_result[0][1],
            disc_number=track_result[0][2],
            explicit=track_result[0][3]
        )
        return result
        

    def get_user(self, id: str) -> user.User | None:
        """Returns Spotify user from database, None if they dont exist

        Args:
            id (str): Spotify ID

        Returns:
            user.User | None: Spotify user object
        """
        # Pull user from database
        db_result = self.cursor.execute(
            "SELECT display_name,image_url,api_token,expires_at,email,timestamp FROM users WHERE id_pkey=:id",
            id=id
        ).fetchall()
        if not db_result:
            return None
        user = user.User(
            id=id,
            display_name=db_result[0][0],
            email=db_result[0][4],
            expires_at=db_result[0][3],
            api_token=db_result[0][2],
            image_url=db_result[0][1],
            timestamp=db_result[0][5]
        )
        return user

    def get_token(self, user_id: str) -> dict | None:
        """Gets access token for spotify api

        Args:
            user_id (str): _description_

        Returns:
            dict | None: _description_
        """
        result = self.cursor.execute(
            "SELECT access_token,token_type,expires_in,scope,expires_at,refresh_token FROM users "+
            "WHERE id_pkey=:id",
            id=user_id
        ).fetchone()
        token = {
            "access_token": result[0],
            "token_type": result[1],
            "expires_in": result[2],
            "scope": result[3],
            "expires_at": result[4],
            "refresh_token": result[5]
        }
        for key in token.keys():
            if token[key] is None:
                return None
        return token

    # ---- Setter Functions ----
    
    def set_token(self, user_id: str, token_info: dict):
        """Writes Authentication API token into database

        Args:
            user_id (str): _description_
            token_info (dict): _description_
        """
        result = self.cursor.execute("SELECT * FROM users WHERE id_pkey=:id",id=user_id).fetchall()
        if result:
            self.cursor.execute(
                "UPDATE users SET access_token=:access_token,token_type=:token_type,expires_in=:expires_in,scope=:scope,expires_at=:expires_at,refresh_token=:refresh_token",
                access_token=token_info["access_token"],
                token_type=token_info["token_type"],
                expires_in=token_info["expires_in"],
                scope=token_info["scope"],
                expires_at=token_info["expires_at"],
                refresh_token=token_info["refresh_token"]
            )
        else:
            self.cursor.execute(
                "INSERT INTO users (id_pkey,access_token,token_type,expires_in,scope,expires_at,refresh_token) VALUES (:id_pkeyaccess_token,:token_type,:expires_in,:scope,:expires_at,:refresh_token)",
                id_pkey=user_id,
                access_token=token_info["access_token"],
                token_type=token_info["token_type"],
                expires_in=token_info["expires_in"],
                scope=token_info["scope"],
                expires_at=token_info["expires_at"],
                refresh_token=token_info["refresh_token"]
            )
        self.connection.commit()
        return

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
        # Check if artist is already in the database
        if self.get_artist(artist.get_id()) is not None:
            self.__update_artist(artist)
            return
        
        # Get artists genres
        for genre in artist.get_genres():
            self.add_genre(genre)
        
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
        if self.get_playlist(playlist.get_id(),playlist.get_user_id()) is not None:
            self.__update_playlist(playlist)
            return
        # Add playlist to the database
        self.cursor.execute(
            "INSERT INTO playlists (id_pkey,users_id_fkey,creator_id,name,description,image_url,timestamp) VALUES (:id,:user_id,:creator_id,:name,:desc,:url,:timestamp)",
            id=playlist.get_id(),
            user_id=playlist.get_user_id(),
            creator_id=playlist.get_creator_id(),
            name=playlist.get_name(),
            desc=playlist.get_description(),
            url=playlist.get_image_url(),
            timestamp=playlist.get_description(),
        )
        # Add user association
        self.cursor.execute(
            "INSERT INTO user_playlists (playlists_id_fkey,users_id_fkey,is_managed) VALUES (:id,:user_id,:managed)",
            id=playlist.get_id(),
            user_id=playlist.get_user_id(),
            is_managed=playlist.is_managed()
        )
        # Add tracks to the playlist
        for track in playlist.get_tracks():
            self.add_track()
            self.cursor.execute(
                "INSERT INTO playlist_content (playlists_id_fkey,tracks_id_fkey) VALUES (:id,:track_id)",
                id=playlist.get_id(),
                track_id=track.get_id()
            )
        self.connection.commit()
        return

    def add_track(self, track: track.Track):
        # Check if track already exists
        if self.cursor.execute("SELECT (id_pkey) FROM tracks WHERE id_pkey=:id_pkey",id_pkey=track.get_id()).fetchall():
            self.__update_track(track)
            return
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
            self.add_artist(artist)
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
        return

    def add_user(self, user: user.User):
        """Adds user to the database

        Args:
            user (user.User): Spotify user object
        """
        # Handle actual user object
        if self.cursor.execute("SELECT * FROM users WHERE id_pkey = :id",id=user.get_id()).fetchall():
            self.__update_user(user)
            return
        # Input new user object
        self.cursor.execute(
            "INSERT INTO users (id_pkey,display_name,image_url,api_token,expires_at,email,timestamp) "+
            "VALUES (:user_id,:display_name,:image_url,:api_token,:expr,:mail,:wurzel)",
            user_id=user.get_id(),
            display_name=user.get_display_name(),
            image_url=user.get_image_url(),
            api_token=user.get_api_token(),
            expr=user.get_expires_at(),
            mail=user.get_email(),
            wurzel=user.get_timestamp()
        )
        self.connection.commit()
        return

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
        return
        

    def __update_artist(self, artist: artist.Artist):
        self.cursor.execute(
            "UPDATE artists SET name=:name,image_url=:image_url,timestamp=:timestamp WHERE id_pkey=:id_pkey",
            id_pkey=artist.get_id(),
            name=artist.get_name(),
            image_url=artist.get_image_url(),
            timestamp=artist.get_timestamp()
        )
        self.__set_artist_genres(artist)
        self.connection.commit()
        return

    def __update_playlist(self, playlist: playlist.Playlist):
        """Updates existing playlist database entry

        Args:
            playlist (playlist.Playlist): Spotify Playlist object to update with
        """
        # Update timestamp if they are the same
        if playlist == self.get_playlist(playlist.get_id()):
            self.cursor.execute("UPDATE playlists SET timestamp=:timestamp",timestamp=playlist.get_timestamp())
            self.connection.commit()
            return
        # Replace entire playlist
        self.cursor.execute("DELETE FROM playlist_content WHERE playlists_id_fkey=:id",id=playlist.get_id())
        self.cursor.execute("DELETE FROM playlists WHERE id_pkey=:id",id=playlist.get_id())
        self.cursor.execute("DELETE FROM user_playlists WHERE users_id_fkey=:user_id AND playlists_id_fkey=:playlist_id",user_id=playlist.get_user_id(),playlist_id=playlist.get_id())
        self.cursor.execute(
            "INSERT INTO PLAYLISTS (id_pkey,creator_id,name,description,image_url,timestamp) "+
            "VALUES (:id,:user_id,:name,:desc,:url,:timestamp)",
            id=playlist.get_id(),
            user_id=playlist.get_creator_id(),
            name=playlist.get_name(),
            desc=playlist.get_description(),
            url=playlist.get_image_url(),
            timestamp=playlist.get_timestamp()
        )
        for track in playlist.get_tracks:
            self.cursor.execute(
                "INSERT INTO playlist_content (playlists_id_fkey,tracks_id_fkey) "+
                "VALUES (:playlist_id,:track_id)",
                playlist_id=playlist.get_id(),
                track_id=track.get_id()
                )
        self.cursor.execute(
            "INSERT INTO user_playlists (users_id_fkey,playlists_id_fkey,is_managed) VALUES (:user_id,:playlist_id,:managed)",
            user_id=playlist.get_user_id(),
            playlist_id=playlist.get_id(),
            managed=playlist.is_managed()
            )
        self.connection.commit()
        return

    def __update_track(self, track: track.Track):
        db_track = self.get_track(track.get_id())
        # Update timestamp if same
        if db_track == track:
            self.cursor.execute("UPDATE tracks SET timestamp=:time WHERE id_pkey=:id",time=track.get_timestamp(),id=track.get_id())
            self.connection.commit()
            return
        for art in track.get_artists():
            self.add_artist(art)
        # Update entire entry otherwise
        self.cursor.execute(
            "UPDATE tracks SET name=:name,duration_ms=:duration_ms,disc_number=:disc_number,explicit=:explicit,timestamp=timestamp",
            name=track.get_name(),
            duration_ms=track.get_duration(),
            disc_number=track.get_disc_number(),
            explicit=track.is_explicit()
        )
        # Update artist connections
        self.cursor.execute("DELETE FROM track_artists WHERE tracks_id_fkey=:id",id=track.get_id())
        for artist in track.get_artists():
            self.cursor.execute(
                "INSERT INTO track_artists (tracks_id_fkey,artists_id_fkey) "+
                "VALUES (:track_id,:artist_id)",
                track_id=track.get_id(),
                artist_id=artist.get_id()
            )
        self.connection.commit()
        return

    def update_favorites(self, user_id: str, delta: tuple[list[track.Track], list[track.Track]]):
        """Update favorites of user, database content is expected to be known! so no error handling!

        Args:
            delta (tuple[list[track.Track], list[track.Track]]): (added,removed)
        """
        for removed_track in delta[1]:
            self.cursor.execute(
                "DELETE FROM favorites WHERE tracks_id_fkey=:track_id AND users_id_fkey=:user_id",
                track_id=removed_track.get_id(),
                user_id=user_id
            )
        for added_track in delta[0]:
            self.cursor.execute(
                "INSERT INTO favorites (tracks_id_fkey,users_id_fkey) VALUES (:track_id,:user_id)",
                track_id=added_track.get_id(),
                user_id=user_id
            )
        self.connection.commit()
        return

    def __update_user(self, user: user.User):
        self.cursor.execute(
            "UPDATE users SET display_name=:display_name,image_url=:image_url,api_token=:api_token,expires_at=:expires_at,email=:email,timestamp=:timestamp",
            display_name=user.get_display_name(),
            image_url=user.get_image_url(),
            api_token=user.get_api_token(),
            expires_at=user.get_expires_at(),
            email=user.get_email(),
            timestamp=user.get_timestamp()
        )
        self.connection.commit()
        return

    # -- Remove --

    def remove_playlist(self, playlist: playlist.Playlist):
        """Deletes user's playlist from database

        Args:
            playlist_id (playlist.Playlist): Spotify Playlist object
        """
        self.cursor.execute("DELETE FROM user_playlists WHERE users_id_fkey=:user_id AND playlists_id_fkey=:",user_id=playlist.get_user_id(),id=playlist.get_id())
        self.connection.commit()
        # If playlist no longer in use, remove from database
        if not self.cursor.execute("SELECT * FROM user_playlists WHERE playlists_id_fkey=:id",id=playlist.get_id()).fetchall():
            self.cursor.execute("DELETE FROM playlist_content WHERE playlists_id_fkey=:id",id=playlist.get_id())
            self.cursor.execute("DELETE FROM playlist_genres WHERE playlists_id_fkey=:id",id=playlist.get_id())
            self.cursor.execute("DELETE FROM playlists WHERE id_pkey=:id",id=playlist.get_id())
        self.connection.commit()
        return

    def remove_user(self, user_id: str):
        self.cursor.execute("DELETE FROM user_playlists WHERE users_id_fkey=:id",id=user_id)
        self.cursor.execute("DELETE FROM favorites WHERE users_id_fkey=:id",id=user_id)
        self.cursor.execute("DELETE FROM users WHERE id_pkey=:id",id=user_id)
        self.connection.commit()
        return

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