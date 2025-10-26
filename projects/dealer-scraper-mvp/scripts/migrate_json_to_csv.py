#!/usr/bin/env python3
"""
Migrate existing tesla_premier_collected.json to new CSV format
"""

import json
import csv
import os

JSON_FILE = "output/tesla_premier_collected.json"
CSV_FILE = "output/tesla_premier_installers.csv"

HEADERS = [
    "name", "phone", "website", "domain", "email",
    "tier", "certifications", "oem_source",
    "scraped_from_zip", "state", "collection_date"
]

if os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)

    installers = data.get("installers", [])
    collection_date = data.get("collection_date", "")

    # Add state and collection_date to each installer
    for installer in installers:
        zip_code = installer.get("scraped_from_zip", "")

        # Determine state from ZIP
        if zip_code.startswith("02"):
            installer["state"] = "MA"
        elif zip_code.startswith("94"):
            installer["state"] = "CA"
        else:
            installer["state"] = ""

        installer["collection_date"] = collection_date

    # Write to CSV
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(installers)

    print(f"✓ Migrated {len(installers)} installers from JSON to CSV")
    print(f"  Output: {CSV_FILE}")
else:
    print(f"⚠ No JSON file found at {JSON_FILE}")
