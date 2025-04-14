import sqlite3
from time import perf_counter
import tkinter as tk

class SpotifyApp:
    def __init__(self, db):
        self._db = db
    
    def most_listened_songs(self, start_date:str="2010-01-01", end_date:str="2999-12-31", limit:int=5) -> None:
        """Get the most listened to song by the user for a specified data range"""
        start_time = perf_counter()
        print(f"Here are your Top {limit} songs from {start_date} to {end_date}")

        # Create the Connection
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        # Find top songs in that date range - returns (track, artist, total_ms)
        songs = cursor.execute("""SELECT s.track, s.artist, SUM(p.ms_played) AS total_ms
                          FROM song_data AS s JOIN play_time AS p
                          ON s.id = p.s_id
                          WHERE timestamp BETWEEN ? AND ?
                          GROUP BY s.id, s.track
                          ORDER BY total_ms DESC
                          LIMIT ?;""", (start_date, end_date, limit)).fetchall()
        
        # Print the most listened to songs
        for n, song in enumerate(songs):
            print(f"{n+1}. {song[0]} by {song[1]} for {song[2] // 60000} minutes")

        # Close the connection
        conn.close()
        end_time = perf_counter()
        print("Time Taken: ", end_time - start_time, "seconds\n")

    def most_listened_artists(self, start_date:str="2010-01-01", end_date:str="2999-12-31", limit:int=5) -> None:
        """Get the most listened to artists by the user during the specified period"""
        start_time = perf_counter()
        print(f"Here are your Top {limit} artists from {start_date} to {end_date}")

        # Create the Connection
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        # Find top artists in that date range - returns (artist, total_ms)
        artists = cursor.execute("""SELECT s.artist, SUM(p.ms_played) AS total_ms
                                FROM song_data AS s JOIN play_time AS p
                                ON s.id = p.s_id
                                WHERE p.timestamp BETWEEN ? AND ?
                                GROUP BY s.artist
                                ORDER BY total_ms DESC
                                LIMIT ?;""", (start_date, end_date, limit)).fetchall()
        
        # Print the most listened to sartists
        for n, artist in enumerate(artists):
            print(f"{n+1}. {artist[0]} for {artist[1] // 60000} minutes")

        # Close the connection
        conn.close()
        end_time = perf_counter()
        print("Time Taken: ", end_time - start_time, "seconds\n")

    def most_listened_albums(self, start_date:str="2010-01-01", end_date:str="2999-12-31", limit:int=5) -> None:
        start_time = perf_counter()
        print(f"Here are your Top {limit} albums from {start_date} to {end_date}")

        # Create the Connection
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        # Find top albums in that date range - returns (album, total_ms)
        albums = cursor.execute("""SELECT s.album, SUM(p.ms_played) AS total_ms
                                FROM song_data AS s JOIN play_time AS p
                                ON s.id = p.s_id
                                WHERE p.timestamp BETWEEN ? AND ?
                                GROUP BY s.album
                                ORDER BY total_ms DESC
                                LIMIT ?;""", (start_date, end_date, limit)).fetchall()
        
        # Print the most listened to songs
        for n, album in enumerate(albums):
            print(f"{n+1}. {album[0]} for {album[1] // 60000} minutes")

        # Close the connection
        conn.close()
        end_time = perf_counter()
        print("Time Taken: ", end_time - start_time, "seconds\n")




if __name__ == "__main__":
    s = SpotifyApp("spotify_data.db")
    start = input("Enter start data: ")
    end = input("Enter end data: ")
    s.most_listened_songs(start, end, limit=10)
    s.most_listened_artists(start, end, limit=10)
    s.most_listened_albums(start, end, limit=5)

