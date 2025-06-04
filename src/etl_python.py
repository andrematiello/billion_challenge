from csv import reader, writer
from collections import defaultdict
from pathlib import Path
from typing import Dict
import time
import datetime

# Constants
PATH_CSV = Path("data/weather_stations.csv")
LOG_PATH = Path("logs/log_python.csv")

# Ensure the logs directory exists
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_step(step: str, status: str) -> None:
    """
    Logs a processing step to a CSV log file, adding a green check emoji for success.
    """
    with LOG_PATH.open("a", newline="") as log_file:
        log_writer = writer(log_file)
        timestamp = datetime.datetime.now().isoformat()
        if status.lower().startswith("success") or status.lower().startswith(
            "completed"
        ):
            status = "✅ " + status
        log_writer.writerow([timestamp, step, status])


def read_temperatures(path_to_csv: Path) -> Dict[str, list[float]]:
    """
    Reads temperature data from a CSV file and groups it by weather station.
    """
    temperature_by_station = defaultdict(list)
    try:
        with path_to_csv.open("r", encoding="utf-8") as file:
            csv_reader = reader(file, delimiter=";")
            for row in csv_reader:
                if len(row) != 2:
                    continue  # Skip malformed rows
                try:
                    station_name = str(row[0])
                    temperature = float(row[1])
                    temperature_by_station[station_name].append(temperature)
                except ValueError:
                    continue  # Skip rows with invalid float conversion
        log_step("Read temperatures", "Success")
        print("✅ Temperatures read successfully.")
    except Exception as e:
        log_step("Read temperatures", f"Failed: {e}")
        raise
    return temperature_by_station


def calculate_statistics(
    temperature_data: Dict[str, list[float]],
) -> Dict[str, Dict[str, float]]:
    """
    Calculates min, mean, and max temperatures for each station.
    """
    results = {}
    for station, temperatures in temperature_data.items():
        results[station] = {
            "min": min(temperatures),
            "mean": sum(temperatures) / len(temperatures),
            "max": max(temperatures),
        }
    log_step("Calculate statistics", "Success")
    print("✅ Statistics calculated successfully.")
    return results


def format_results(stats: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, str]]:
    """
    Formats the temperature statistics to 2 decimal places and sorts them by station name.
    """
    sorted_stats = dict(sorted(stats.items(), key=lambda item: item[0]))
    formatted = {
        station: {
            "min": f"{data['min']:.2f}",
            "mean": f"{data['mean']:.2f}",
            "max": f"{data['max']:.2f}",
        }
        for station, data in sorted_stats.items()
    }
    log_step("Format results", f"Success: {len(formatted)} stations processed")
    print(f"✅ Results formatted successfully: {len(formatted)} stations processed.")
    return formatted


def process_temperatures(path_to_csv: Path) -> Dict[str, Dict[str, str]]:
    """
    Full processing pipeline: reads, computes, formats temperature statistics.
    """
    print("Starting temperature processing from CSV file...")
    start_time = time.time()

    temperature_data = read_temperatures(path_to_csv)
    stats = calculate_statistics(temperature_data)
    formatted = format_results(stats)

    elapsed = time.time() - start_time
    print(f"⏱️  Total processing completed in {elapsed:.2f} seconds.")
    log_step("⏱️  Total processing", f"Completed in {elapsed:.2f} seconds")

    return formatted


# Main execution
if __name__ == "__main__":
    if not PATH_CSV.exists():
        print(f"❌ File {PATH_CSV} not found.")
        log_step("File check", "Failed: File not found")
    else:
        try:
            results = process_temperatures(PATH_CSV)
            # Show sample of results
            for station, stats in list(results.items())[:5]:
                print(f"{station}: {stats}")
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            log_step("Process temperatures", f"Failed: {e}")
