class Database_old:
    '''This class is used to read/write from/to the database.'''

    def get_all_artists(self) -> list[objects.artist.Artist]:
        '''Returns all artists present in the database.'''
        result_list = []
        db_result = self.db_cur.execute("SELECT id_pkey,name,timestamp FROM artists").fetchall()
        
        for item in db_result:
            next_artist = objects.artist.Artist(id=item[0], name=item[1], timestamp=item[2])
            next_artist.set_genres(self.get_artist_genres())
            result_list.append(next_artist)

    ################
    # modifications


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


    def update_library(self, user_id: str, delta: tuple[list[objects.track.Track],list[objects.track.Track]]):
        '''Takes list differences between local and online database and updates database based on that. (added,removed)'''
        self.logger.debug("update_library()")
        self.logger.info(f"Updating library for '{user_id}'")

        for track in delta[0]:
            self.db_con.execute("INSERT INTO libraries (users_id_fkey,tracks_id_fkey) VALUES (?,?)",(user_id,track.get_id()))

        for track in delta[1]:
            self.db_con.execute("DELETE FROM libraries WHERE tracks_id_fkey=?",(track.get_id(),))

        self.db_con.commit()