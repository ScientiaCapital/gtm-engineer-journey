"""
Add OEM Overlap Analysis to Contractor Lists

Adds two columns:
- number_of_overlap: Count of other contractors sharing at least one OEM
- list_of_overlap: Comma-separated list of shared OEMs with other contractors
"""
import pandas as pd
from pathlib import Path
from collections import Counter
import sys

def parse_oems(oem_string):
    """Parse OEM Sources column into list of OEMs"""
    if pd.isna(oem_string) or oem_string == '':
        return []
    # Split by comma and clean whitespace
    return [oem.strip() for oem in str(oem_string).split(',') if oem.strip()]

def calculate_oem_overlap(df):
    """Calculate OEM overlap for each contractor"""
    # Parse all OEM lists
    df['oem_list'] = df['OEM Sources'].apply(parse_oems)

    # Get all unique OEMs across all contractors
    all_oems = set()
    for oem_list in df['oem_list']:
        all_oems.update(oem_list)

    print(f"Found {len(all_oems)} unique OEMs: {sorted(all_oems)}")

    # For each contractor, count how many others share each OEM
    overlap_counts = []
    overlap_lists = []

    for idx, row in df.iterrows():
        contractor_oems = set(row['oem_list'])
        if not contractor_oems:
            overlap_counts.append(0)
            overlap_lists.append('')
            continue

        # Count contractors sharing each OEM
        oem_overlap_counts = {}
        for oem in contractor_oems:
            # Count how many OTHER contractors have this OEM
            count = sum(1 for other_oems in df['oem_list'] if oem in other_oems) - 1  # -1 to exclude self
            if count > 0:
                oem_overlap_counts[oem] = count

        # Total unique contractors with overlap (may share multiple OEMs)
        contractors_with_overlap = set()
        for oem in contractor_oems:
            for other_idx, other_row in df.iterrows():
                if other_idx != idx and oem in other_row['oem_list']:
                    contractors_with_overlap.add(other_idx)

        num_overlap = len(contractors_with_overlap)

        # Format overlap list: "OEM1 (X), OEM2 (Y)" where X,Y are contractor counts
        if oem_overlap_counts:
            overlap_str = ', '.join(f"{oem} ({count})" for oem, count in sorted(oem_overlap_counts.items(), key=lambda x: x[1], reverse=True))
        else:
            overlap_str = ''

        overlap_counts.append(num_overlap)
        overlap_lists.append(overlap_str)

    # Add overlap columns
    df['number_of_overlap'] = overlap_counts
    df['list_of_overlap'] = overlap_lists

    # Add multi-OEM indicator column
    df['is_multi_oem'] = df['oem_list'].apply(lambda x: 'YES' if len(x) > 1 else 'NO')
    df['oem_count_verified'] = df['oem_list'].apply(len)

    # Add OEM diversity score (useful for prioritization)
    # Higher score = more unique OEM combinations (less common)
    oem_tuple_list = [tuple(sorted(oems)) for oems in df['oem_list']]
    oem_combo_counts = Counter(oem_tuple_list)
    df['oem_diversity_score'] = [100 - min(99, oem_combo_counts[tuple(sorted(oems))])
                                  for oems in df['oem_list']]

    # Drop temporary column
    df = df.drop(columns=['oem_list'])

    return df

def main():
    base_path = Path('/Users/tmkipper/Desktop/tk_projects/gtm-engineer-journey/projects/dealer-scraper-mvp/output/gtm/executive_package_20251025')

    # Process MASTER_CONTRACTOR_DATABASE
    master_file = base_path / 'MASTER_CONTRACTOR_DATABASE.csv'
    print(f"\nProcessing {master_file.name}...")
    df_master = pd.read_csv(master_file)
    print(f"Loaded {len(df_master)} contractors")

    # Calculate overlaps
    df_master = calculate_oem_overlap(df_master)

    # Save updated master file
    output_master = base_path / 'MASTER_CONTRACTOR_DATABASE_with_overlap.csv'
    df_master.to_csv(output_master, index=False)
    print(f"✓ Saved {output_master.name} ({len(df_master)} rows)")

    # Create TOP 200 list (by ICP Fit Score)
    print("\nCreating TOP 200 list...")
    df_top200 = df_master.nlargest(200, 'ICP Fit Score')
    output_top200 = base_path / 'TOP_200_CONTRACTORS_with_overlap.csv'
    df_top200.to_csv(output_top200, index=False)
    print(f"✓ Saved {output_top200.name} ({len(df_top200)} rows)")

    # Summary statistics
    print("\n=== OEM Overlap Summary ===")
    print(f"Master Database:")
    print(f"  - Total contractors: {len(df_master)}")
    print(f"  - Multi-OEM contractors: {(df_master['is_multi_oem'] == 'YES').sum()}")
    print(f"  - Single-OEM contractors: {(df_master['is_multi_oem'] == 'NO').sum()}")
    print(f"  - Avg OEMs per contractor: {df_master['oem_count_verified'].mean():.2f}")
    print(f"  - Avg overlap per contractor: {df_master['number_of_overlap'].mean():.1f}")
    print(f"  - Max overlap: {df_master['number_of_overlap'].max()}")
    print(f"  - Contractors with no overlap: {(df_master['number_of_overlap'] == 0).sum()}")

    print(f"\nTop 200:")
    print(f"  - Multi-OEM contractors: {(df_top200['is_multi_oem'] == 'YES').sum()}")
    print(f"  - Single-OEM contractors: {(df_top200['is_multi_oem'] == 'NO').sum()}")
    print(f"  - Avg OEMs per contractor: {df_top200['oem_count_verified'].mean():.2f}")
    print(f"  - Avg overlap per contractor: {df_top200['number_of_overlap'].mean():.1f}")
    print(f"  - Max overlap: {df_top200['number_of_overlap'].max()}")
    print(f"  - Contractors with no overlap: {(df_top200['number_of_overlap'] == 0).sum()}")

    # Top 10 multi-OEM contractors
    multi_oem_contractors = df_master[df_master['is_multi_oem'] == 'YES']
    if len(multi_oem_contractors) > 0:
        print(f"\nTop 10 Multi-OEM contractors (by OEM count):")
        top_multi = multi_oem_contractors.nlargest(10, 'oem_count_verified')[['Contractor Name', 'OEM Sources', 'oem_count_verified', 'oem_diversity_score']]
        print(top_multi.to_string(index=False))
    else:
        print("\n⚠ No multi-OEM contractors found in current dataset")
        print("  This will change as you add more OEM scrapers (Kohler, Cummins, etc.)")

    # Top 10 contractors by overlap
    print("\nTop 10 contractors by overlap count:")
    top_overlap = df_master.nlargest(10, 'number_of_overlap')[['Contractor Name', 'OEM Sources', 'number_of_overlap', 'list_of_overlap']]
    print(top_overlap.to_string(index=False))

if __name__ == '__main__':
    main()
