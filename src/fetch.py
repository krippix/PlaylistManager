# external
import spotipy
# python native
import logging
# project
import objects.artist, objects.track, objects.playlist, util.database

def fetch_library(connection: spotipy.Spotify) -> list[objects.track.Track()]:
    '''Takes all tracks from users library and returns them as List of song objects'''
    result_list = []

    # fetch library
    done = False
    offset = 0

    # iterate over library
    while not done:
        results = connection.current_user_saved_tracks(limit=50,offset=offset)

        if len(results["items"]) < 50:
            done = True
        
        for track in results["items"]:
            track = track["track"]
            
            # put artists into one list
            artists = []
            for artist in track["artists"]:
                artists.append(objects.artist.Artist(artist["id"],artist["name"]))
            
            result_list.append(objects.track.Track(id=track["id"],name=track["name"],artists=artists))
        offset += 50

    return result_list

def fetch_playlists(connection: spotipy.Spotify):
    '''Returns a list of the users created playlists.'''
    result_list = []
    current_user_id = connection.current_user()["id"]

    # fetch all playlists
    done = False
    offset = 0

    # iterate over playlist collection
    while not done:
        results = connection.current_user_playlists(limit=50,offset=offset)

        if len(results["items"]) < 50:
            done = True

        for item in results["items"]:
            if item["owner"]["id"] == current_user_id:
                result_list.append(objects.playlist.Playlist(id=item["id"], name=item["name"], owner_id=current_user_id))

    return result_list

#def fetch_artist(spotify_con: spotipy.Spotify, ):
    