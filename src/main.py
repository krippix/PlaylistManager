# external
import spotipy
# python native
import logging
# project
import util.database, util.config
import objects.artist, objects.track
import spotify_api

def main():
    ''''''
    logging.basicConfig(encoding='utf-8', level=logging.ERROR)
    # prepare project configuration
    settings = util.config.Config()
    settings.checkConfig()

    # Database init
    db_con = util.database.Database()
    db_con.ensure_default_tables()
    
    # spotify api connection
    spotify = spotify_api.Spotify_api().get_connection()
    


    # Test Print user tracks
    #print(spotify.current_user())
    #print(connection.user())
    
    #list = fetch.fetch_playlists(connection)

    #db_con.add_artist(objects.artist.Artist("1337420lel", "MC ARSCHWASSEr"))

if __name__ == "__main__":
    main()