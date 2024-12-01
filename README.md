# Google Photos JSON to XMP Converter

This script converts metadata from JSON files in a Google Photos library (e.g., from Google Takeout) into XMP sidecar files. These sidecar files can be used by photo management software to associate metadata with the corresponding media files.

## Features

- Converts JSON metadata into XMP format, including:
  - Title
  - Description
  - Date and time the photo was taken
  - GPS location (latitude, longitude, and reference directions)
- Handles `.jpg`, `.jpeg`, `.png`, and `.mp4` file types.
- Processes directories recursively, including subdirectories.
- Supports parallel execution with multiple `exiftool` processes for faster performance.
- Displays a live progress indicator while processing files.

## Requirements

- **Python 3.7 or higher**: Download and install from [python.org](https://www.python.org/).
- **ExifTool**: Install from [exiftool.org](https://exiftool.org/).

## Installation

1. Clone or download this repository.
2. Install Python and ExifTool if not already installed.
3. Ensure `exiftool` is in your system's `PATH`.

## Usage

Run the script with the following command:

```bash
python json_to_xmp.py <directory> [-n NUM_WORKERS]
```

### Arguments

- `<directory>`: The root directory containing the Google Photos files.
- `-n` or `--num-workers`: (Optional) Number of parallel ExifTool processes to use. Default is 4.

### Example

To process a Google Photos library in `/path/to/google_photos_takeout` using 8 parallel processes:

```bash
python json_to_xmp.py /path/to/google_photos_takeout -n 8
```

### Output

For each media file, an XMP sidecar file will be created in the same directory with the same base filename, e.g.:

```
IMG_1234.jpg -> IMG_1234.xmp
```

### Progress Indicator

The script displays a live progress indicator in the terminal:

```
Processed 50/100
```

## Error Handling

- Invalid timestamps or GPS values are skipped with warnings logged to the console.
- Any file that fails to process will not stop the script; an error message will be displayed, and processing will continue.

## Notes

- The script validates metadata before writing to XMP to avoid generating invalid files.
- Files with no corresponding JSON metadata are ignored.
- Only valid GPS and date/time values are written to the XMP files.

## Performance

- The script supports multi-threaded execution with the `-n` option to optimize performance.
- The optimal number of workers depends on your system's CPU and disk I/O capacity. Experiment with different values for best results.

## Troubleshooting

### ExifTool Not Found

Ensure that `exiftool` is installed and added to your system's `PATH`. To verify, run:

```bash
exiftool -ver
```

If it is not installed, download and install it from [ExifTool Downloads](https://exiftool.org/).

### Slow Processing

- Increase the number of workers with the `-n` option (e.g., `-n 8`).
- Ensure the script is running on a system with sufficient resources (CPU, disk I/O).

## License

This script is open-source and available under the [MIT License](LICENSE).

## Contributions

Feel free to submit issues or pull requests to enhance the script!
