import spotipy
import spotipy.oauth2 as oauth2
from random import randrange

credentials = oauth2.SpotifyClientCredentials(
        client_id="246f1cd67f374c84807d5fd48f25de80",
        client_secret="816db100c39d4d39928047ec9366989e")

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

# get song ids from list of playlist ids
def GetSongs(playlists):
    song_names = []
    song_links = []
    for i in playlists:
        try:
            for j in spotify.user_playlist('spotify', i)['tracks']['items']:
                song_names.append(j['track']['name'])
                song_links.append(j['track']['external_urls']['spotify'])
        except:
            pass

    ret = {"song_names" : song_names, "song_links" : song_links}
    return ret

def GetByMood(mood,songsnumber=3):
    mood = mood.lower()
    if (mood == "happy"):
        playlists = ["spotify:user:spotify:playlist:37i9dQZF1DWTpgpHHF8zH5","spotify:user:spotify:playlist:37i9dQZF1DX7KNKjOK0o75"]
    elif (mood == "sad"):
        playlists = ["spotify:track:13HVjjWUZFaWilh2QUJKsP","spotify:user:spotify:playlist:37i9dQZF1DWU0ScTcjJBdj"]
    elif (mood == "angry"):
        playlists = ["spotify:user:spotify:playlist:37i9dQZF1DX1tyCD9QhIWF","spotify:user:revadastv:playlist:71Xpaq3Hbpxz6w9yDmIsaH"]
    elif (mood == "fear"):
        playlists = ["spotify:user:spotify:playlist:37i9dQZF1DXa2PsvJSPnPf","spotify:user:spotify:playlist:37i9dQZF1DX2pSTOxoPbx9"]
    elif (mood == "neutral"):
        playlists = ["spotify:user:spotify:playlist:37i9dQZF1DX4ALYsOGumV8","spotify:user:spotify:playlist:37i9dQZF1DX3PIPIT6lEg5"]
    elif (mood == "surprise"):
        playlists = ["spotify:user:spotify:playlist:37i9dQZF1DX3rxVfibe1L0","spotify:user:spotify:playlist:37i9dQZF1DX9XIFQuFvzM4"]
    elif (mood == "disgust"):
        playlists = ["spotify:user:spotify:playlist:37i9dQZF1DWSf2RDTDayIx","spotify:user:spotify:playlist:37i9dQZF1DXdsy92d7BLpC"]

    songs = GetSongs(playlists)
    selected_index = []
    ret_songs = []
    ret_links = []

    while len(selected_index) < songsnumber:
        random_index = randrange(0,len(songs["song_names"]))
        if (random_index not in selected_index):
            selected_index.append(random_index)
            ret_songs.append(songs["song_names"][random_index])
            ret_links.append(songs["song_links"][random_index])

    ret = {"song_names" : ret_songs, "song_links" : ret_links}
    return ret