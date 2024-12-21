import plistlib
import csv

def extract_album_data(itunes_xml_path, output_csv):
    """
    Extract album information (Album Title, Album Artist, Release Date) from the iTunes XML file
    and save it to a CSV file.
    """
    # Load the iTunes XML file
    with open(itunes_xml_path, 'rb') as file:
        itunes_data = plistlib.load(file)

    # Get the tracks dictionary
    tracks = itunes_data.get('Tracks', {})

    # Prepare data for CSV
    album_data = {}
    for track_id, track_info in tracks.items():
        album_title = track_info.get('Album', 'Unknown Album')
        album_artist = track_info.get('Album Artist', track_info.get('Artist', 'Unknown Artist'))
        release_date = track_info.get('Year', 'Unknown')  # iTunes stores the year as an integer

        # Use album title and album artist as the unique key to avoid duplicate entries
        key = (album_title, album_artist)
        if key not in album_data:
            album_data[key] = release_date

    # Write data to the CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Album Title', 'Artist', 'Release Date'])

        for (album_title, album_artist), release_date in album_data.items():
            writer.writerow([album_title, album_artist, release_date])

    print(f"Album data exported to {output_csv}")


# Example usage
itunes_xml_path = 'iTunes Music Library.xml'  # Path to your iTunes XML file
output_csv = 'album_data.csv'  # Output CSV file

extract_album_data(itunes_xml_path, output_csv)
