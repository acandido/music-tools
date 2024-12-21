import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Spotify API credentials
CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'
REDIRECT_URI = 'http://localhost:8888/callback'


# Scope to save albums to the user's library
SCOPE = 'user-library-modify user-library-read'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# File paths for output logs
NOT_FOUND_FILE = 'spotify_not_found.txt'
ADDED_FILE = 'spotify_added.txt'
EXISTS_FILE = 'spotify_exists.txt'

# Clear previous file contents
for file in [NOT_FOUND_FILE, ADDED_FILE, EXISTS_FILE]:
    with open(file, 'w') as f:
        f.write('')

def search_album(album_title, artist_name):
    """Search for an album on Spotify and return its ID."""
    query = f'album:{album_title} artist:{artist_name}'
    results = sp.search(q=query, type='album', limit=1)
    albums = results.get('albums', {}).get('items', [])
    if albums:
        return albums[0]['id']
    return None

def album_exists_in_library(album_id):
    """Check if an album already exists in the user's Spotify library."""
    results = sp.current_user_saved_albums_contains([album_id])
    return results[0]  # Returns True if the album is already saved, False otherwise

def log_to_file(file_path, message):
    """Write a message to a file."""
    with open(file_path, 'a') as f:
        f.write(message + '\n')

def add_album_to_library(album_id, album_title, artist_name):
    """Add an album to the user's Spotify library."""
    sp.current_user_saved_albums_add([album_id])
    message = f"Added '{album_title}' by {artist_name}"
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
    log_to_file(ADDED_FILE, message)

def process_albums_from_csv(csv_file):
    """Process a CSV file containing album data and add each album to Spotify."""
    # Load the CSV file
    album_data = pd.read_csv(csv_file)

    # Iterate over each row in the CSV
    for _, row in album_data.iterrows():
        album_title = row['Album Title']
        artist_name = row['Artist']
        release_date = row['Release Date']  # You can use this if needed, though it's not used in the Spotify search

        # Search for the album on Spotify
        album_id = search_album(album_title, artist_name)
        if not album_id:
            message = f"Album not found: '{album_title}' by {artist_name}"
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")
            log_to_file(NOT_FOUND_FILE, message)
            continue

        # Check if the album already exists in the library
        if album_exists_in_library(album_id):
            message = f"Album already in library: '{album_title}' by {artist_name}"
            print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
            log_to_file(EXISTS_FILE, message)
        else:
            add_album_to_library(album_id, album_title, artist_name)

# Example usage
csv_file_path = 'album_data.csv'  # Replace with your CSV file path
process_albums_from_csv(csv_file_path)
