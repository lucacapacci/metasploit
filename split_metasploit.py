import json
import os
import re
import shutil

def process_metasploit():
    # 1. Load the raw data
    source_file = 'modules_metadata_base.json'
    if not os.path.exists(source_file):
        print(f"Error: {source_file} not found.")
        return
        
    with open(source_file, 'r') as f:
        data = json.load(f)

    # 2. Clean and Recreate the data_single directory
    target_dir = 'data_single'
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir) # Prevents duplicates from previous runs
    os.makedirs(target_dir)

    for module_key, info in data.items():
        references = info.get('references', [])
        path = info.get('path', 'unknown')
        
        # Filter for unique CVEs in this specific module
        cves = list(set([ref for ref in references if ref.startswith('CVE-')]))
        
        for cve in cves:
            # Extract year (e.g., '2014' from 'CVE-2014-6041')
            match = re.search(r'CVE-(\d{4})-', cve)
            if not match:
                continue
            year = match.group(1)

            # Create the year directory inside data_single
            year_dir = os.path.join(target_dir, year)
            if not os.path.exists(year_dir):
                os.makedirs(year_dir)

            # Prepare the metadata entry
            entry = {
                "cve": cve,
                "module": module_key,
                "path": f"https://github.com/rapid7/metasploit-framework/blob/master{path}",
                "name": info.get('name'),
                "disclosure_date": info.get('disclosure_date')
            }

            # File path: data_single/YYYY/CVE-XXXX-YYYY.json
            file_path = os.path.join(year_dir, f"{cve}.json")

            # Check for existing data to handle cases where multiple modules exploit one CVE
            existing_data = []
            if os.path.exists(file_path):
                with open(file_path, 'r') as ef:
                    try:
                        existing_data = json.load(ef)
                    except json.JSONDecodeError:
                        existing_data = []

            # Append only if this module key isn't already in the file
            if not any(e['module'] == module_key for e in existing_data):
                existing_data.append(entry)
                with open(file_path, 'w') as wf:
                    json.dump(existing_data, wf, indent=2)

if __name__ == "__main__":
    process_metasploit()
