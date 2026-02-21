# Metasploit DB Mirror

This repository contains a continuously updated CVE-indexed mirror of the [Metasploit DB](https://docs.metasploit.com/docs/modules.html), available in JSON format.

Data is refreshed every hour and organized in multiple formats for easier access and analysis.

## Repository Structure

CVE data is available in the following formats:

1. **All data in a single file**  
   Get all exploits &rarr; https://lucacapacci.github.io/metasploit/modules_metadata_base.json

2. **Files grouped by year**  
   Example: get all CVEs starting with "CVE-2025-" &rarr; https://lucacapacci.github.io/metasploit/data_years/2025.json
   
3. **Single file per CVE**  
   Example: get CVE-2021-44228 &rarr;
   https://lucacapacci.github.io/metasploit/data_single/2021/CVE-2021-44228.json

---

## Usage Examples

### Using `curl`

```bash
curl -L https://lucacapacci.github.io/metasploit/data_single/2021/CVE-2021-44228.json
```

---

## Update Frequency

Data is automatically updated every hour, providing near real-time CVE tracking.
