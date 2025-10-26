#!/usr/bin/env python3
"""
Tesla Manual Collection Helper
Combines manual navigation with automated extraction

Usage:
    python3 scripts/tesla_manual_collection.py

Process:
    1. Script opens browser and shows you next ZIP code
    2. YOU: Enter ZIP manually on Tesla page, wait for results
    3. YOU: Press Enter when results are loaded
    4. SCRIPT: Extracts all installers automatically
    5. Repeat for all 179 ZIPs

Resume support:
    - Progress saved after each ZIP
    - Can stop/restart anytime
    - Skips already-collected ZIPs
"""

import sys
import os
import json
import csv
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from config import WEALTHY_ZIPS_NATIONWIDE

# Configuration
TESLA_URL = "https://www.tesla.com/support/certified-installers?productType=powerwall"
PROGRESS_FILE = "output/tesla_manual_progress.json"
OUTPUT_DIR = "output"
BATCH_SIZE = 20  # Save to CSV every 20 ZIPs

# JavaScript extraction script (same as automated scraper)
EXTRACTION_SCRIPT = """
() => {
    const cards = document.querySelectorAll('.styles_ciContainer__58zW_');

    const installers = Array.from(cards).map(card => {
        const text = card.innerText;
        const lines = text.split('\\n').filter(l => l.trim());

        // Extract data from card lines
        const tier = lines[0] || '';
        const name = lines[1] || '';
        const phone = lines[2] || '';
        const website = lines[3] || '';
        const email = lines[4] || '';

        // Extract domain from website URL
        let domain = '';
        if (website && website.startsWith('http')) {
            try {
                const url = new URL(website);
                domain = url.hostname.replace('www.', '');
            } catch (e) {
                domain = '';
            }
        }

        // Format phone number
        let formattedPhone = phone;
        if (phone && phone.length === 10 && /^\\d{10}$/.test(phone)) {
            formattedPhone = `(${phone.substring(0,3)}) ${phone.substring(3,6)}-${phone.substring(6,10)}`;
        }

        // Determine certifications
        const certifications = [];
        if (tier.includes('Premier')) {
            certifications.push('Premier Certified Installer');
            certifications.push('Powerwall');
        } else {
            certifications.push('Certified Installer');
            certifications.push('Powerwall');
        }

        return {
            name: name,
            phone: formattedPhone,
            website: website,
            domain: domain,
            email: email,
            tier: tier,
            certifications: certifications.join('; '),
            oem_source: 'Tesla'
        };
    });

    return installers;
}
"""


def load_progress():
    """Load progress from JSON file"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"completed_zips": [], "current_batch": 0, "total_collected": 0}


def save_progress(progress):
    """Save progress to JSON file"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def save_batch_csv(batch_num, installers):
    """Save batch results to CSV"""
    filename = f"{OUTPUT_DIR}/tesla_manual_batch_{batch_num:03d}.csv"

    if not installers:
        return filename

    fieldnames = ['name', 'phone', 'website', 'domain', 'email', 'tier',
                  'certifications', 'scraped_from_zip', 'oem_source']

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(installers)

    print(f"  ✓ Saved {len(installers)} installers to {filename}")
    return filename


def merge_all_batches():
    """Merge all batch CSV files into final output"""
    batch_files = sorted(Path(OUTPUT_DIR).glob("tesla_manual_batch_*.csv"))

    if not batch_files:
        print("⚠ No batch files to merge")
        return 0

    all_installers = []
    for batch_file in batch_files:
        with open(batch_file, 'r') as f:
            reader = csv.DictReader(f)
            all_installers.extend(list(reader))

    # Deduplicate by phone
    unique_installers = {}
    for installer in all_installers:
        phone = installer.get('phone', '').replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        if phone and phone not in unique_installers:
            unique_installers[phone] = installer

    final_installers = list(unique_installers.values())

    if final_installers:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"{OUTPUT_DIR}/tesla_manual_{timestamp}.csv"

        fieldnames = ['name', 'phone', 'website', 'domain', 'email', 'tier',
                      'certifications', 'scraped_from_zip', 'oem_source']

        with open(final_filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_installers)

        print(f"\n✓ Merged {len(batch_files)} batch files")
        print(f"  Total unique installers: {len(final_installers)}")
        print(f"  Output: {final_filename}")
        return len(final_installers)

    return 0


def run_manual_collection():
    """Main manual collection workflow"""
    # Get all wealthy ZIPs
    all_zips = []
    for state_zips in WEALTHY_ZIPS_NATIONWIDE.values():
        all_zips.extend(state_zips)

    print("=" * 70)
    print("TESLA MANUAL COLLECTION - 179 WEALTHY ZIP CODES")
    print("=" * 70)
    print(f"Total ZIPs to collect: {len(all_zips)}")
    print()

    # Load progress
    progress = load_progress()
    remaining_zips = [z for z in all_zips if z not in progress["completed_zips"]]

    if len(remaining_zips) < len(all_zips):
        print(f"📋 RESUMING: {len(progress['completed_zips'])} ZIPs already completed")
        print(f"   Remaining: {len(remaining_zips)} ZIPs")
        print()

    if not remaining_zips:
        print("✅ All ZIPs completed!")
        merge_all_batches()
        return

    # Start browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Opening Tesla page...")
        page.goto(TESLA_URL, wait_until='domcontentloaded')
        print("✓ Browser ready\n")

        batch_installers = []
        batch_num = progress["current_batch"] + 1

        try:
            for i, zip_code in enumerate(remaining_zips):
                print("=" * 70)
                print(f"[{i + 1}/{len(remaining_zips)}] ZIP CODE: {zip_code}")
                print("=" * 70)
                print()
                print("YOUR TURN:")
                print(f"  1. Enter ZIP code: {zip_code}")
                print("  2. Wait for results to load completely")
                print("  3. Scroll down to see all installer cards")
                print("  4. Press Enter when ready for extraction")
                print()

                input("Press Enter when results are loaded... ")

                # Extract installers
                print("\nExtracting installers...")
                try:
                    installers = page.evaluate(EXTRACTION_SCRIPT)

                    # Add ZIP code to each
                    for installer in installers:
                        installer['scraped_from_zip'] = zip_code

                    print(f"✓ Extracted {len(installers)} installers")

                    batch_installers.extend(installers)
                    progress["completed_zips"].append(zip_code)
                    progress["total_collected"] += len(installers)

                    save_progress(progress)

                    # Save batch every 20 ZIPs
                    if len(batch_installers) >= BATCH_SIZE:
                        save_batch_csv(batch_num, batch_installers)
                        batch_installers = []
                        batch_num += 1
                        progress["current_batch"] = batch_num
                        save_progress(progress)

                    print()

                except Exception as e:
                    print(f"✗ Error extracting: {e}")
                    print("Skipping this ZIP...\n")
                    continue

            # Save final batch
            if batch_installers:
                save_batch_csv(batch_num, batch_installers)

        finally:
            browser.close()

    # Merge all batches
    print("\n" + "=" * 70)
    print("COLLECTION COMPLETE - MERGING RESULTS")
    print("=" * 70)
    total = merge_all_batches()

    print("\n" + "=" * 70)
    print("TESLA MANUAL COLLECTION COMPLETE")
    print("=" * 70)
    print(f"Total ZIPs collected: {len(progress['completed_zips'])}")
    print(f"Unique installers: {total}")
    print("=" * 70)


if __name__ == "__main__":
    try:
        run_manual_collection()
    except KeyboardInterrupt:
        print("\n\n⏸ Collection paused - progress saved")
        print("Run this script again to resume from where you left off")
