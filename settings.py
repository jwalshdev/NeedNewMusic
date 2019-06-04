from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sqlite3

rec_thresh = 1.0
(cid, cis) = ('d7b5acea9c8944cb9b9bccabe154a4a8', '157b4f1c306f42799ddafd12227443b4')
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=cis)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
conn = sqlite3.connect('dates.db')
