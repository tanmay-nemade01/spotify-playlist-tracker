import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import json
import streamlit as st
from pathlib import Path


# Authenticate with Spotify API
def create_spotify_connection():
    spotify_json = Path(__file__).parent.parent / "configs" / "spotify.json"
    with open(spotify_json, 'r') as file:
        data = json.load(file)
    client_id = data['SPOTIFY'][0]['CLIENT_ID']
    client_secret = data['SPOTIFY'][1]['CLIENT_SECRET']
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))
    print('Spotify Connection Successful')
    return sp

# Function to get playlist name from a playlist
def get_playlist_name(sp, playlist_id):
    playlist_details = sp.playlist(playlist_id,fields='name')
    playlist_name = playlist_details["name"]
    return playlist_name

# Function to get all tracks from a playlist
def get_playlist_tracks(sp, playlist_id):
    tracks = []
    
    results = sp.playlist_tracks(playlist_id, limit = 10)
    for item in results['items']:
        track = item['track']
        if track:
            tracks.append({
                "name": track['name'],
                "artist": ", ".join([artist['name'] for artist in track['artists']]),
                "album": track['album']['name'],
                "url": track['external_urls']['spotify']
            })

    return tracks
