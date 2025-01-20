import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd
import streamlit as st
from pathlib import Path


from spotipy.oauth2 import SpotifyOAuth

# Define your Spotify API credentials
CLIENT_ID = "bfe88e1d1bed423690dd20fdad80096f"
CLIENT_SECRET = "81b385aa9b5748a89edc22341a204211"
REDIRECT_URI = "https://open.spotify.com/"

# Define the scope (permissions)
SCOPE = "user-library-read user-read-playback-state playlist-modify-public playlist-modify-private"
# SCOPE = "user-library-read user-read-playback-state"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


spotify_liked = Path(__file__).parent.parent / "sources" / "spotify_liked.csv"
data = pd.read_csv(spotify_liked, sep=',')
spotify_liked_tracks = data['spotify:track:Spotify - id'].to_list()
spotify_liked_tracks
# Fetch user profile information to confirm login
# user_info = sp.current_user()
# track = sp.track('5TJOAIWHRYW8pRBpnvLUo1')
# track
for liked_track in spotify_liked_tracks:
    track = sp.playlist_add_items('',[liked_track])
# track
# print(f"Logged in as: {user_info['display_name']}")

