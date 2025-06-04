# 🌡️ Weather Station Data Processor

## ETL AND PROJECT STRUCTURE

This project is a lightweight ETL pipeline developed in Python, designed to process large-scale weather station data from a CSV file. It performs ingestion, cleaning, calculation of basic statistics, formatting of results, and logging — all in a simple yet extensible architecture.

📁 /data/
└── weather_stations.csv # Input CSV with temperature readings
📁 /logs/
└── log_python.csv # Auto-generated log of execution steps
📄 create_measurements.py # (Optional) script to generate synthetic input
📄 process_weather_data.py # Main processing script (this project)


---

## ABOUT THE PROJECT

The script reads a CSV file containing temperature measurements per weather station (in the format `station_name;temperature`). It computes the **minimum**, **mean**, and **maximum** temperature for each station, formats the values to two decimal places, and logs each step of the process in a structured way.

---

## PIPELINE FLOW

```text
[CSV File] → [Ingest Data] → [Validate + Clean Rows] → [Compute Stats] → [Format Results] → [Show Sample] → [Log Each Step]
```

Each major function logs its status to /logs/log_python.csv with timestamps and visual success indicators (✅).

BUSINESS PROBLEM
Organizations dealing with environmental monitoring, infrastructure planning, or agricultural logistics often handle large-scale weather data, but need quick insights per station for decision-making.

HOW YOUR SOLUTION ADDRESSES THIS PROBLEM
This solution:

Processes millions of lines in seconds using in-memory structures.

Aggregates essential statistics (min, mean, max) by station.

Logs the full pipeline flow for auditing and debugging.

Allows for seamless expansion into dashboards, APIs, or data exports.

GETTING STARTED
Prerequisites
Python 3.10+

Basic shell environment (Linux/macOS/WSL)

Installation and Setup
bash
Copiar
Editar
git clone https://github.com/andrematiello/billion_challenge.git
cd billion_challenge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # if using one
How to run the project:
bash
Copiar
Editar
python process_weather_data.py
If the file data/weather_stations.csv exists, the script will process it and show results in terminal + log to logs/log_python.csv.

TECHNOLOGIES USED
🐍 Python 3.11

🧠 Basic ETL architecture

📁 File-based logging

🧩 Modular script design

LIBRARIES USED
csv — for parsing and writing CSV files

collections.defaultdict — for efficient grouping of temperatures

pathlib — for safe file path operations

time, datetime — for execution time and timestamp logging

os — to ensure folders exist or fetch user-level info (if needed)

ABOUT THE DATA
The input file is a CSV where each line contains:

php-template
Copiar
Editar
<station_name>;<temperature>
Example:

Copiar
Editar
Berlin;12.4
Kigali;24.6
São Paulo;19.3
You can create your own using create_measurements.py or import real weather station datasets from public repositories.

SIMPLE CLEANING AND TRANSFORMATIONS WERE PERFORMED
Lines with fewer than 2 columns are skipped.

Temperatures are cast to float, with invalid rows ignored.

Aggregations use native min, max, and sum / len for performance.

COMMENTS
Logs are appended automatically to /logs/log_python.csv on each run.

You can configure the output to be saved in CSV or JSON easily.

The script prints the top 5 results by station name after processing.

MAIN TECHNICAL FEATURES
✅ Modular function design (read, calculate, format, log)
✅ Log file with timestamps and emojis for readability
✅ Automatic folder creation for logs
✅ Fast performance with native Python (no Pandas or NumPy required)
✅ Friendly CLI usage, expandable to larger systems

📣 Future ideas:
Add median and standard deviation

Export results to .csv or .json

Create a Flask API or dashboard with Streamlit or Dash

Schedule processing via cron or Airflow
