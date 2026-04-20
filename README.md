# mesh2gpx

Convert [Meshtastic](https://meshtastic.org) position log CSV exports to GPX track files.

## Installation

```bash
pip install .
```

## Usage

```bash
mesh2gpx positions.csv
mesh2gpx positions.csv -o track.gpx
```

The output defaults to the input filename with a `.gpx` extension.

## CSV Format

The CSV must contain latitude and longitude columns. The following column names are recognized (case-insensitive):

| Field     | Accepted names                        |
|-----------|---------------------------------------|
| Latitude  | `latitude`, `lat`                     |
| Longitude | `longitude`, `lon`, `long`            |
| Timestamp | `timestamp`, `time`, `date`           |
| Altitude  | `altitude`, `alt`, `elevation`        |

Timestamps are expected in `MM/DD/YY HH:MM` format. Rows missing lat/lon are skipped.

## Requirements

- Python 3.9+
- No third-party dependencies
