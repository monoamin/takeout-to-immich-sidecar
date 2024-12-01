import os
import json
import subprocess
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse

def create_xmp_from_json(json_path, image_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    xmp_data = []

    # Map JSON metadata to XMP tags
    if 'title' in metadata:
        xmp_data.append(f'-XMP:Title={metadata["title"]}')
    if 'description' in metadata and metadata['description']:
        xmp_data.append(f'-XMP:Description={metadata["description"]}')
    if 'photoTakenTime' in metadata and 'timestamp' in metadata['photoTakenTime']:
        try:
            # Convert timestamp to a proper datetime
            timestamp = int(metadata['photoTakenTime']['timestamp'])
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            formatted_date = dt.strftime('%Y:%m:%d %H:%M:%S')
            xmp_data.append(f'-XMP:DateTimeOriginal={formatted_date}')
        except (ValueError, OSError):
            print(f"Warning: Invalid timestamp {metadata['photoTakenTime']['timestamp']} in {json_path}")

    # Handle GPS data
    if 'geoData' in metadata:
        geo = metadata['geoData']
        if geo.get('latitude') != 0.0 or geo.get('longitude') != 0.0:
            xmp_data.append(f'-XMP:GPSLatitude={abs(geo["latitude"])}')
            xmp_data.append(f'-XMP:GPSLongitude={abs(geo["longitude"])}')
            xmp_data.append(f'-XMP:GPSLatitudeRef={"N" if geo["latitude"] >= 0 else "S"}')
            xmp_data.append(f'-XMP:GPSLongitudeRef={"E" if geo["longitude"] >= 0 else "W"}')

    # Create XMP sidecar file using ExifTool
    xmp_path = f'{os.path.splitext(image_path)[0]}.xmp'
    if xmp_data:
        command = ['exiftool', '-o', xmp_path] + xmp_data + [image_path]
        subprocess.run(command, check=True)
    else:
        print(f"Warning: No valid metadata found for {image_path}")

def process_file(json_image_pair):
    json_path, image_path = json_image_pair
    try:
        create_xmp_from_json(json_path, image_path)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_directory(directory, num_workers):
    # Collect all JSON-image pairs
    json_image_pairs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4')):
                image_path = os.path.join(root, file)
                json_path = f'{image_path}.json'
                if os.path.exists(json_path):
                    json_image_pairs.append((json_path, image_path))

    total_files = len(json_image_pairs)
    print(f"Found {total_files} files to process.")

    # Process files in parallel using a thread pool
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for idx, _ in enumerate(executor.map(process_file, json_image_pairs), 1):
            print(f"Processed {idx}/{total_files}", end="\r")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Google Photos JSON metadata to XMP sidecar files.')
    parser.add_argument('directory', help='Directory containing images and JSON files')
    parser.add_argument('-n', '--num-workers', type=int, default=4, help='Number of parallel ExifTool processes (default: 4)')
    args = parser.parse_args()
    process_directory(args.directory, args.num_workers)
