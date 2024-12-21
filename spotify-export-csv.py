import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

# Spotify API credentials
CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'
REDIRECT_URI = 'http://localhost:8888/callback'

# Scope to read the user's saved albums
SCOPE = 'user-library-read'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def fetch_saved_albums():
    """Fetch all saved albums from the user's Spotify library."""
    albums = []
    results = sp.current_user_saved_albums(limit=50)
    while results:
        for item in results['items']:
            album = item['album']
            album_title = album['name']
            album_artist = ', '.join([artist['name'] for artist in album['artists']])
            release_date = album.get('release_date', 'Unknown')
            albums.append((album_title, album_artist, release_date))

        # Check if there's another page of results
        if results['next']:
            results = sp.next(results)
        else:
            break
    return albums

def export_albums_to_csv(albums, output_csv):
    """Export album data to a CSV file."""
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Album Title', 'Artist', 'Release Date'])
        writer.writerows(albums)
    print(f"Exported {len(albums)} albums to {output_csv}")

# Fetch albums and export to CSV
output_csv = 'spotify_albums.csv'
saved_albums = fetch_saved_albums()
export_albums_to_csv(saved_albums, output_csv)
