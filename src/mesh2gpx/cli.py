"""Convert a Meshtastic position log CSV to GPX for import into Reitti."""

import argparse
import csv
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree


def csv_to_gpx(csv_path: str, gpx_path: str) -> None:
    gpx = Element(
        "gpx",
        version="1.1",
        creator="meshtastic-convert",
        xmlns="http://www.topografix.com/GPX/1/1",
    )
    trk = SubElement(gpx, "trk")
    trk_name = SubElement(trk, "name")
    trk_name.text = "Meshtastic Track"
    trkseg = SubElement(trk, "trkseg")

    count = 0
    with open(csv_path) as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            r = {k.strip().lower(): v.strip() for k, v in row.items()}

            lat = r.get("latitude") or r.get("lat")
            lon = r.get("longitude") or r.get("lon") or r.get("long")
            if not lat or not lon:
                continue

            trkpt = SubElement(trkseg, "trkpt", lat=lat, lon=lon)

            ts = r.get("timestamp") or r.get("time") or r.get("date")
            if ts:
                time_el = SubElement(trkpt, "time")
                try:
                    dt = datetime.strptime(ts, "%m/%d/%y %H:%M")
                    time_el.text = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    time_el.text = ts

            alt = r.get("altitude") or r.get("alt") or r.get("elevation")
            if alt:
                ele = SubElement(trkpt, "ele")
                ele.text = alt

            count += 1

    ElementTree(gpx).write(gpx_path, xml_declaration=True, encoding="unicode")
    print(f"Wrote {count} trackpoints to {gpx_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Meshtastic position log CSV to GPX"
    )
    parser.add_argument("csv", help="Path to the Meshtastic CSV export")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output GPX file path (default: input filename with .gpx extension)",
    )
    args = parser.parse_args()
    output = args.output or str(Path(args.csv).with_suffix(".gpx"))
    csv_to_gpx(args.csv, output)


if __name__ == "__main__":
    main()
