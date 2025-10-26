#!/usr/bin/env python3
"""
Tesla Premier Installer Collection
Collects ONLY Premier Certified Installers (highest quality leads)

Based on working MCP Playwright workflow:
- Navigate to Tesla page
- Type ZIP into combobox
- Click autocomplete option
- Wait for results to load
- Extract Premier installers only
- Save incrementally with resume support
"""

import sys
import os
import json
import csv
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from config import WEALTHY_ZIPS_NATIONWIDE

# Configuration
TESLA_URL = "https://www.tesla.com/support/certified-installers?productType=powerwall"
PROGRESS_FILE = "output/tesla_premier_progress.json"
OUTPUT_DIR = "output"
BATCH_SIZE = 20

# Premier-only extraction script
EXTRACTION_SCRIPT = """
() => {
    const cards = document.querySelectorAll('.styles_ciContainer__58zW_');

    const installers = Array.from(cards)
        .map(card => {
            const text = card.innerText;
            const lines = text.split('\\n').filter(l => l.trim());

            // Extract tier first to filter
            const tier = lines[0] || '';

            // ONLY process Premier Installers
            if (!tier.includes('Premier')) {
                return null;
            }

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

            return {
                name: name,
                phone: formattedPhone,
                website: website,
                domain: domain,
                email: email,
                tier: tier,
                certifications: 'Premier Certified Installer; Powerwall',
                oem_source: 'Tesla'
            };
        })
        .filter(installer => installer !== null);

    return installers;
}
"""


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"completed_zips": [], "current_batch": 0, "total_collected": 0}


def save_progress(progress):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def save_batch_csv(batch_num, installers):
    filename = f"{OUTPUT_DIR}/tesla_premier_batch_{batch_num:03d}.csv"

    if not installers:
        return filename

    fieldnames = ['name', 'phone', 'website', 'domain', 'email', 'tier',
                  'certifications', 'scraped_from_zip', 'oem_source']

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(installers)

    print(f"  ✓ Saved {len(installers)} Premier installers to {filename}")
    return filename


def merge_all_batches():
    batch_files = sorted(Path(OUTPUT_DIR).glob("tesla_premier_batch_*.csv"))

    if not batch_files:
        print("⚠ No batch files to merge")
        return 0, None

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
        final_filename = f"{OUTPUT_DIR}/tesla_premier_{timestamp}.csv"

        fieldnames = ['name', 'phone', 'website', 'domain', 'email', 'tier',
                      'certifications', 'scraped_from_zip', 'oem_source']

        with open(final_filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_installers)

        print(f"\n✓ Merged {len(batch_files)} batch files")
        print(f"  Total unique Premier installers: {len(final_installers)}")
        print(f"  Output: {final_filename}")
        return len(final_installers), final_filename

    return 0, None


def scrape_zip(page, zip_code):
    """Scrape Tesla Premier installers for a single ZIP"""
    try:
        # Navigate to Tesla page
        print(f"    Navigating to Tesla page...")
        page.goto(TESLA_URL, timeout=60000, wait_until='domcontentloaded')
        time.sleep(4)

        # Wait for network idle
        page.wait_for_load_state("networkidle", timeout=60000)
        time.sleep(2)

        # Wait for ZIP input
        print(f"    Waiting for ZIP input...")
        page.wait_for_selector('input[role="combobox"]', state='visible', timeout=60000)
        time.sleep(1)

        # Type ZIP code
        zip_input = page.locator('input[role="combobox"]')
        zip_input.fill(zip_code)
        time.sleep(1.5)

        print(f"    Typed ZIP: {zip_code}")

        # Click autocomplete option
        try:
            page.wait_for_selector('div[role="listbox"]', state='visible', timeout=5000)
            time.sleep(1)

            first_option = page.locator('div[role="listbox"] div[role="option"]').first
            first_option.click()
            print(f"    Clicked autocomplete")
        except:
            # Fallback: press Enter
            print(f"    Pressing Enter (no autocomplete)")
            zip_input.press('Enter')

        # Wait for results to load (critical timing!)
        print(f"    Waiting for results...")
        time.sleep(8)

        # Extract Premier installers only
        print(f"    Extracting Premier installers...")
        installers = page.evaluate(EXTRACTION_SCRIPT)

        # Add ZIP to each
        for installer in installers:
            installer['scraped_from_zip'] = zip_code

        print(f"    ✓ Found {len(installers)} Premier installers")
        return installers

    except Exception as e:
        print(f"    ✗ Error: {e}")
        return []


def run_collection():
    """Main collection workflow"""
    # Get all ZIPs
    all_zips = []
    for state_zips in WEALTHY_ZIPS_NATIONWIDE.values():
        all_zips.extend(state_zips)

    print("=" * 70)
    print("TESLA PREMIER INSTALLER COLLECTION - 179 ZIP CODES")
    print("=" * 70)
    print(f"Total ZIPs: {len(all_zips)}")
    print(f"Filter: PREMIER INSTALLERS ONLY (highest quality)")
    print()

    # Load progress
    progress = load_progress()
    remaining_zips = [z for z in all_zips if z not in progress["completed_zips"]]

    if len(remaining_zips) < len(all_zips):
        print(f"📋 RESUMING: {len(progress['completed_zips'])} ZIPs completed")
        print(f"   Remaining: {len(remaining_zips)} ZIPs")
        print()

    if not remaining_zips:
        print("✅ All ZIPs completed!")
        merge_all_batches()
        return

    # Start browser
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()

        batch_installers = []
        batch_num = progress["current_batch"] + 1

        try:
            for i, zip_code in enumerate(remaining_zips):
                print(f"\n[{i + 1}/{len(remaining_zips)}] Scraping ZIP {zip_code}...")

                installers = scrape_zip(page, zip_code)

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

                # Delay between ZIPs
                if i < len(remaining_zips) - 1:
                    delay = 3
                    print(f"  ⏱  Waiting {delay}s...")
                    time.sleep(delay)

            # Save final batch
            if batch_installers:
                save_batch_csv(batch_num, batch_installers)

        finally:
            browser.close()

    # Merge results
    print("\n" + "=" * 70)
    print("MERGING RESULTS")
    print("=" * 70)
    total, final_file = merge_all_batches()

    print("\n" + "=" * 70)
    print("TESLA PREMIER COLLECTION COMPLETE")
    print("=" * 70)
    print(f"Total ZIPs: {len(progress['completed_zips'])}")
    print(f"Unique Premier installers: {total}")
    print(f"Output: {final_file}")
    print("=" * 70)


if __name__ == "__main__":
    try:
        run_collection()
    except KeyboardInterrupt:
        print("\n\n⏸ Collection paused - progress saved")
        print("Run again to resume")
