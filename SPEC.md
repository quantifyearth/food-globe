# Impact Data JSON Specification

This document describes the structure and format of the agricultural commodity impact data stored in JSON files within this dataset.

## Overview

The dataset contains impact values for agricultural commodity production across different countries. The data is structured as a three-level hierarchy: **destination country** → **commodity** → **source country** → **impact value**.

## File Structure

### Aggregate File
- **File**: `impact_paths_all_results.json` (4.1MB)
- **Description**: Contains impact data for all countries in a single file
- **Structure**: `{destination_country: {commodity: {source_country: impact_value}}}`

### Individual Country Files
- **Pattern**: `{country_code}/impact_paths.json`
- **Description**: Contains impact data for a specific destination country
- **Structure**: `{commodity: {source_country: impact_value}}`
- **Count**: 176 countries with data files out of 249 total country directories

## Data Schema

### Top Level (Aggregate File)
```json
{
  "destination_country_code": {
    // Country-specific commodity data
  }
}
```

### Country Level
```json
{
  "commodity_name": {
    // Source country impact data
  }
}
```

### Commodity Level
```json
{
  "source_country_code": impact_value
}
```

### Complete Example
```json
{
  "EGY": {
    "Wheat": {
      "RUS": 0.0071585307087605,
      "ROU": 0.0081872001726948,
      "EGY": 0.0176100458708308,
      "UKR": 0.0892136051155044
    },
    "Barley": {
      "UKR": 0.0018635972501755,
      "FRA": 0.0025981524485445
    }
  }
}
```

## Data Types

### Country Codes
- **Format**: ISO 3166-1 alpha-3 country codes
- **Case**: Lowercase (e.g., `usa`, `gbr`, `deu`, `fra`, `chn`)
- **Count**: 249 total codes (176 with data)
- **Examples**:
  - `usa`: United States
  - `gbr`: United Kingdom  
  - `deu`: Germany
  - `fra`: France
  - `chn`: China

### Commodity Names
- **Format**: String descriptors, often with qualifiers
- **Count**: 153 unique commodities
- **Categories**: Grains, fruits, vegetables, meat, dairy, nuts, spices, etc.
- **Examples**:
  - `"Wheat"`
  - `"Meat; cattle"`
  - `"Almonds; with shell"`
  - `"Milk; whole fresh cow"`
  - `"Coffee; green"`
  - `"Chillies and peppers; green"`

### Impact Values
- **Type**: Float (double precision)
- **Range**: Varies significantly (from ~1e-11 to ~1.12)
- **Scientific Notation**: Small values may use scientific notation (e.g., `1.234e-06`)
- **Zero Values**: Explicitly represented as `0.0`

## Key Characteristics

### Hierarchical Structure
1. **Destination Country**: The country receiving/importing the commodity
2. **Commodity**: The specific agricultural product
3. **Source Country**: The country producing/exporting the commodity
4. **Impact Value**: The numerical impact measure

### Data Completeness
- Not all countries have data for all commodities
- Not all commodities have data from all potential source countries
- Some countries may have zero impact values for certain source countries

### File Organization
- Individual country files contain the same structure as their corresponding section in the aggregate file
- Country directories without `impact_paths.json` files exist but contain no data
- All JSON files are properly formatted and can be parsed by standard JSON libraries

## Usage Patterns

### Loading All Data
```python
import json

with open('impact_paths_all_results.json') as f:
    all_data = json.load(f)
    
# Access: all_data[destination_country][commodity][source_country]
impact = all_data['EGY']['Wheat']['RUS']  # 0.0071585307087605
```

### Loading Individual Country Data
```python
import json

with open('usa/impact_paths.json') as f:
    usa_data = json.load(f)
    
# Access: usa_data[commodity][source_country] 
impact = usa_data['Wheat']['CAN']  # 0.0115289038534545
```

### Iterating Through Data
```python
# All countries and commodities
for dest_country, commodities in all_data.items():
    for commodity, sources in commodities.items():
        for source_country, impact_value in sources.items():
            print(f"{dest_country} <- {commodity} <- {source_country}: {impact_value}")
```

## Validation Rules

1. **Country codes** must be 3-character lowercase strings
2. **Commodity names** are descriptive strings, may contain semicolons and spaces
3. **Impact values** must be non-negative numeric values
4. **JSON structure** must maintain the three-level hierarchy
5. **File encoding** should be UTF-8

## Data Quality Notes

- Zero values are explicitly stored rather than omitted
- Very small values are preserved in scientific notation
- Missing combinations (country-commodity-source) are simply not present in the data structure
- Individual country files are consistent subsets of the aggregate file data