import connectors.snowflake_connection as snow_con
import connectors.spotify_connection as spot_con
import streamlit as st
import pandas as pd
import re
from pathlib import Path
from jinja2 import Template

# st.title('Spotify Playlist Tracker')

def get_playlist_name(playlist_id):
    playlist_name = spot_con.get_playlist_name(sp, playlist_id)
    playlist_name = re.sub(r'[^a-zA-Z0-9 ]', '', playlist_name)
    playlist_name = playlist_name.replace(' ','_')
    return playlist_name

def get_playlist_table(playlist_id):
    playlist_tracks = spot_con.get_playlist_tracks(sp, playlist_id)
    playlist_table = session.create_dataframe(playlist_tracks)
    return playlist_table

def setup_snowflake_db_schema():
    create_database = session.sql('CREATE DATABASE IF NOT EXISTS SPOTIFY;').collect()
    use_database = session.sql('USE DATABASE SPOTIFY;').collect()
    create_schema = session.sql('CREATE SCHEMA IF NOT EXISTS PLAYLISTS;').collect()
    use_database = session.sql('USE SCHEMA PLAYLISTS;').collect()

#Create required connections
session  = snow_con.create_session()
sp = spot_con.create_spotify_connection()


playlist_id = '0lcGUwmkwQfCEnbdz5h2z0'
if playlist_id != '':
    playlist_name = get_playlist_name(playlist_id)
    playlist_table = get_playlist_table(playlist_id)
    playlist_table
    setup_snowflake_db_schema()
    playlist_table.write.save_as_table(f'STA_{playlist_name}', mode='overwrite')

    setup_sql = Path(__file__).parent / "scripts" / "setup.sql"
    with open(setup_sql) as f:
        sql_template = f.read()
    template = Template(sql_template)
    rendered_sql = template.render(table_name=playlist_name)

    queries = [query.strip() for query in rendered_sql.split(";") if query.strip()]

    for query in queries:
        result = session.sql(query).collect()

    df = session.table(playlist_name).collect()


