#!/usr/bin/env python3
"""
Generate countries.json from available impact_paths.json files.
This script scans all subdirectories for impact_paths.json files and
creates a list of available country codes.
"""

import json
import os
from pathlib import Path

def generate_countries_json():
    """Scan directories and generate countries.json file."""
    
    # Get the script's directory
    base_dir = Path(__file__).parent
    
    # Find all directories with impact_paths.json files
    countries = []
    
    for item in base_dir.iterdir():
        if item.is_dir():
            # Check if this directory has an impact_paths.json file
            impact_file = item / 'impact_paths.json'
            if impact_file.exists():
                # Directory name is the country code
                country_code = item.name.lower()
                countries.append(country_code)
                print(f"Found: {country_code}")
    
    # Sort the countries alphabetically
    countries.sort()
    
    # Write to countries.json
    output_file = base_dir / 'countries.json'
    with open(output_file, 'w') as f:
        json.dump(countries, f, indent=2)
    
    print(f"\nGenerated countries.json with {len(countries)} countries")
    print(f"Output file: {output_file}")
    
    # Also generate a human-readable list for verification
    readme_content = f"# Available Countries\n\nTotal: {len(countries)} countries\n\n"
    readme_content += "## Country Codes:\n"
    for i, country in enumerate(countries, 1):
        readme_content += f"{i:3}. {country}\n"
    
    readme_file = base_dir / 'COUNTRIES.md'
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    print(f"Also generated COUNTRIES.md for reference")
    
    return countries

if __name__ == "__main__":
    countries = generate_countries_json()
    
    # Verify the file was created correctly
    with open('countries.json', 'r') as f:
        loaded = json.load(f)
        assert loaded == countries, "Verification failed: saved data doesn't match"
        print("\n✓ Verification passed: countries.json is valid")