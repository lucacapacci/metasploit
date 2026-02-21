import json
import os
import re

def process_metasploit():
    # Load the raw data
    with open('modules_metadata_base.json', 'r') as f:
        data = json.load(f)

    # Prepare directories
    dirs = ['data_years', 'data_single']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    year_map = {}

    for module_key, info in data.items():
        references = info.get('references', [])
        path = info.get('path', 'unknown')
        
        # Find all CVEs in the references list
        cves = [ref for ref in references if ref.startswith('CVE-')]
        
        for cve in cves:
            # Extract year from CVE-YYYY-NNNN
            match = re.search(r'CVE-(\d{4})-', cve)
            if not match:
                continue
            year = match.group(1)

            entry = {
                "cve": cve,
                "module": module_key,
                "path": path,
                "name": info.get('name')
            }

            # Individual CVE files
            single_path = f"data_single/{cve}.json"
            # If multiple modules exploit the same CVE, we append to a list
            if os.path.exists(single_path):
                with open(single_path, 'r+') as sf:
                    existing = json.load(sf)
                    existing.append(entry)
                    sf.seek(0)
                    json.dump(existing, sf, indent=2)
            else:
                with open(single_path, 'w') as sf:
                    json.dump([entry], sf, indent=2)

            # Year-based grouping
            if year not in year_map:
                year_map[year] = []
            year_map[year].append(entry)

    # Write year files
    for year, entries in year_map.items():
        with open(f"data_years/{year}.json", 'w') as yf:
            json.dump(entries, yf, indent=2)

if __name__ == "__main__":
    process_metasploit()
