import sqlite3
import json

class SpotifyDatabase:
    def __init__(self, db):
        self._db = db

    def create_dbs(self):
        """Create the song and time databases"""

        print("Creating Database...")

        # Create the connection
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()

        # Create the databases
        cursor.execute("""
                        CREATE TABLE song_data(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        track VARCHAR(200),
                        artist VARCHAR(50),
                        album VARCHAR(50)
                        );""")
        
        cursor.execute("""
                        CREATE TABLE play_time(
                        occurrence_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        s_id INT,
                        timestamp CHAR(20),
                        ms_played INTEGER,
                        FOREIGN KEY (s_id) REFERENCES song_data(id) ON DELETE CASCADE
                        );""")
        
        # Close the connection
        conn.close()
        print("(+) Database created!")

    def parse_data(self, file) -> None:
        """Parse the JSON data and store in database"""

        # Load data
        with open(file, "r", encoding="utf-8") as json_file:
            dataset = json.load(json_file)

        # Connect to the database
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()
        print("Parsing data into database...")

        for item in dataset:
            # Initialise a variable to see if this song is already in the database
            in_db = False

            # Get the attributes for both databases
            data_atts = (item.get("master_metadata_track_name"), item.get("master_metadata_album_artist_name"), item.get("master_metadata_album_album_name"))
            time_atts = (item.get("ts"), item.get("ms_played"))

            # Check if the song is already in the database
            s_id = cursor.execute("""SELECT id FROM song_data
                                     WHERE track=? AND artist=?""", (item.get("master_metadata_track_name"), item.get("master_metadata_album_artist_name"))).fetchone()
            
            # If song is already in database
            if s_id is not None:
                s_id = s_id[0]  #s_id will be a tuple '(id, )' due to .fetchone() method
                in_db = True

            # Insert the data into the database
            if not in_db:
                cursor.execute("""INSERT INTO song_data(track, artist, album)
                                VALUES (?, ?, ?)""", data_atts)
                s_id = cursor.execute("""SELECT last_insert_rowid()""").fetchone()[0]

            cursor.execute("""INSERT INTO play_time(s_id, timestamp, ms_played)
                            VALUES (?, ?, ?)""", (s_id, *time_atts))
            
        # Commit the data
        conn.commit()
        print("(+) Data Commited!")

        # Close the Connection
        cursor.close()

    def remove_nulls(self):
        """Some items may include podcasts, so all the data will be null, this function removes those null values"""

        # Create the connection
        conn = sqlite3.connect(self._db)
        cursor = conn.cursor()
        print("Removing Null Values...")

        # Find the null value ids
        null_ids = cursor.execute("""SELECT id FROM song_data
                                        WHERE track IS NULL;""").fetchall()

        # Delete the null values from the database
        for id in null_ids:
            cursor.execute("""DELETE FROM song_data WHERE id = ?""", id)

        # Commit changes to database
        conn.commit()
        print("(+) Null values removed")

        # Close the connection
        conn.close()

if __name__ == "__main__":
    parser = SpotifyDatabase("spotify_data.db")
    parser.parse_data("2024 Data/Streaming_History_Audio_2018-2022_0.json")
    parser.parse_data("2024 Data/Streaming_History_Audio_2022-2023_1.json")
    parser.parse_data("2024 Data/Streaming_History_Audio_2023-2024_2.json")
    parser.parse_data("2024 Data/Streaming_History_Audio_2024-2025_3.json")
    parser.remove_nulls()