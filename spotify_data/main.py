import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from song_model import Song
from song_dao import dao_get_all_songs, dao_save_songs
from db import create_tables
from typing import List

client_id = "715cc0d435f146178be1c2641db5dec4"
client_secret = "3c4390bbd3fd4ffcbd90e5093feedbea"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_songs(query: str) -> List[Song]:
    results = sp.search(query, limit=10)
    songs = []
    for track in results["tracks"]["items"]:
        song = Song(
            title=track["name"],
            artist=track["artists"][0]["name"],
            album=track["album"]["name"],
            spotify_id=track["id"]
        )
        songs.append(song)
    return songs

def save_songs(songs: List[Song]):
    dao_save_songs(songs)

if __name__ == '__main__':
    create_tables()
    
    while True:
        selection = input('''
                         Select:
                         s - to search
                         g - to print all the songs from the database
                         q - to quit
                         ''')
        selection = selection.lower()
        if selection == 'q':
            break
        elif selection == 'g':
            print("All the songs from the database:")
            all_songs = dao_get_all_songs()
            for song in all_songs:
                print(f"Title: {song.title} Artist: {song.artist} Album: {song.album}")
        elif selection == 's':
            search_query = input("Enter your search:")
            songs = search_songs(search_query)
            
            if len(songs) > 0:
                print(f"Songs found: {len(songs)}")
                for i, song in enumerate(songs, 1):
                    print(f"{i}: Title: {song.title} Artist: {song.artist} Album: {song.album}")
                save_choice = input('Press Y to save these songs\nPress any other key to not save: ')
                if save_choice.lower() == 'y':
                    save_songs(songs)
                    print("Songs saved")
                else:
                    print("Songs not saved")
            else:
                print("No songs were found")
