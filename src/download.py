import spotipy

def fetch_library(connection: spotipy.Spotify):
    '''Takes all songs from users library and returns them as List: [(id,name,artist), ... ]'''
    result_list = []

    # fetch library
    done = False
    offset = 0

    # iterate over library
    while not done:
        results = connection.current_user_saved_tracks(limit=50,offset=offset)
        print(offset)
        if len(results["items"]) < 50:
            done = True
        
        for song in results["items"]:
            track = song["track"]
            # Todo: concentrate artists into one string
            result_list.append((track["id"],track["name"],track["artists"][0]["name"]))
        offset += 50

    return result_list

def fetch_playlists(connection: spotipy.Spotify):
    '''Returns a list of the users created playlists'''