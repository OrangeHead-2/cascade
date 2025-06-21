# Water Quality Analyzer

A production-grade Cascade language project for analyzing water sensor data.

## Features

- Parses water sample CSVs for multiple sites
- Calculates robust statistics (avg, min, max, median, stddev)
- Configurable anomaly thresholds via JSON
- Logs warnings, errors, and info with context
- Outputs human-readable and CSV reports
- Handles malformed data gracefully

## Usage

1. Place your CSVs in `data/`. Each should have the format:  
   `timestamp,location,ph,turbidity,temperature`
2. Adjust anomaly thresholds in `config/anomaly_thresholds.json` as needed
3. Run via Cascade CLI or in your Cascade IDE

## Output

- Console report with statistics and anomaly list
- CSV file in `output/analysis_report.csv` with all detected anomalies