# from csv import reader, writer
# from collections import defaultdict
# from pathlib import Path
# from typing import Dict
# import time
# import datetime

# # Constants
# BASE_DIR = Path(__file__).resolve().parent.parent  # volta para a raiz do projeto
# PATH_CSV = BASE_DIR / "data" / "weather_stations.csv"
# LOG_PATH = BASE_DIR / "logs" / "log_python.csv"
# OUTPUT_PATH = BASE_DIR / "data" / "measurements_python.csv"  # ← alterado aqui

# # Ensure required directories exist
# LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
# OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# def log_step(step: str, status: str) -> None:
#     """
#     Logs a processing step to a CSV log file, adding a green check emoji for success.
#     """
#     with LOG_PATH.open("a", newline="") as log_file:
#         log_writer = writer(log_file)
#         timestamp = datetime.datetime.now().isoformat()
#         if status.lower().startswith("success") or status.lower().startswith(
#             "completed"
#         ):
#             status = "✅ " + status
#         log_writer.writerow([timestamp, step, status])


# def read_temperatures(path_to_csv: Path) -> Dict[str, list[float]]:
#     """
#     Reads temperature data from a CSV file and groups it by weather station.
#     """
#     temperature_by_station = defaultdict(list)
#     try:
#         with path_to_csv.open("r", encoding="utf-8") as file:
#             csv_reader = reader(file, delimiter=";")
#             for row in csv_reader:
#                 if len(row) != 2:
#                     continue  # Skip malformed rows
#                 try:
#                     station_name = str(row[0])
#                     temperature = float(row[1])
#                     temperature_by_station[station_name].append(temperature)
#                 except ValueError:
#                     continue  # Skip rows with invalid float conversion
#         log_step("Read temperatures", "Success")
#         print("✅ Temperatures read successfully.")
#     except Exception as e:
#         log_step("Read temperatures", f"Failed: {e}")
#         raise
#     return temperature_by_station


# def calculate_statistics(
#     temperature_data: Dict[str, list[float]],
# ) -> Dict[str, Dict[str, float]]:
#     """
#     Calculates min, mean, and max temperatures for each station.
#     """
#     results = {}
#     for station, temperatures in temperature_data.items():
#         results[station] = {
#             "min": min(temperatures),
#             "mean": sum(temperatures) / len(temperatures),
#             "max": max(temperatures),
#         }
#     log_step("Calculate statistics", "Success")
#     print("✅ Statistics calculated successfully.")
#     return results


# def format_results(stats: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, str]]:
#     """
#     Formats the temperature statistics to 2 decimal places and sorts them by station name.
#     """
#     sorted_stats = dict(sorted(stats.items(), key=lambda item: item[0]))
#     formatted = {
#         station: {
#             "min": f"{data['min']:.2f}",
#             "mean": f"{data['mean']:.2f}",
#             "max": f"{data['max']:.2f}",
#         }
#         for station, data in sorted_stats.items()
#     }
#     log_step("Format results", f"Success: {len(formatted)} stations processed")
#     print(f"✅ Results formatted successfully: {len(formatted)} stations processed.")
#     return formatted


# def save_results_to_file(results: Dict[str, Dict[str, str]], output_path: Path) -> None:
#     """
#     Saves the formatted results to a CSV file with semicolon delimiter.
#     """
#     try:
#         with output_path.open("w", encoding="utf-8") as f:
#             f.write("station;min;mean;max\n")
#             for station, data in results.items():
#                 line = f"{station};{data['min']};{data['mean']};{data['max']}\n"
#                 f.write(line)
#         log_step("Save results", "Success")
#         print(f"✅ Results saved to {output_path}")
#     except Exception as e:
#         log_step("Save results", f"Failed: {e}")
#         print(f"❌ Failed to save results: {e}")


# def process_temperatures(path_to_csv: Path) -> Dict[str, Dict[str, str]]:
#     """
#     Full processing pipeline: reads, computes, formats temperature statistics.
#     """
#     print("Starting temperature processing from CSV file...")
#     start_time = time.time()

#     temperature_data = read_temperatures(path_to_csv)
#     stats = calculate_statistics(temperature_data)
#     formatted = format_results(stats)
#     save_results_to_file(formatted, OUTPUT_PATH)

#     elapsed = time.time() - start_time
#     print(f"⏱️  Total processing completed in {elapsed:.2f} seconds.")
#     log_step("⏱️  Total processing", f"Completed in {elapsed:.2f} seconds")

#     return formatted


# # Main execution
# if __name__ == "__main__":
#     if not PATH_CSV.exists():
#         print(f"❌ File {PATH_CSV} not found.")
#         log_step("File check", "Failed: File not found")
#     else:
#         try:
#             results = process_temperatures(PATH_CSV)
#             # Show sample of results
#             for station, stats in list(results.items())[:5]:
#                 print(f"{station}: {stats}")
#         except Exception as e:
#             print(f"❌ Processing failed: {e}")
#             log_step("Process temperatures", f"Failed: {e}")


# inserindo saída parquet, acima somente csv
from csv import reader, writer
from collections import defaultdict
from pathlib import Path
from typing import Dict
import time
import datetime

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_CSV = BASE_DIR / "data" / "weather_stations.csv"
LOG_PATH = BASE_DIR / "logs" / "log_python.csv"
OUTPUT_PATH = BASE_DIR / "data" / "measurements_python.csv"

# Ensure required directories exist
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


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


def save_results_to_file(results: Dict[str, Dict[str, str]], output_path: Path) -> None:
    """
    Saves the formatted results to a CSV file with semicolon delimiter
    and also creates a Parquet version in the same directory.
    """
    try:
        with output_path.open("w", encoding="utf-8") as f:
            f.write("station;min;mean;max\n")
            for station, data in results.items():
                line = f"{station};{data['min']};{data['mean']};{data['max']}\n"
                f.write(line)
        log_step("Save results", "Success")
        print(f"✅ Results saved to {output_path}")
    except Exception as e:
        log_step("Save results", f"Failed: {e}")
        print(f"❌ Failed to save results: {e}")
        return

    # Linha separadora no log
    log_step("───────────────", "───────────────")

    # Salvar também como Parquet
    try:
        import pandas as pd

        df = pd.DataFrame.from_dict(results, orient="index")
        df.index.name = "station"
        df.reset_index(inplace=True)

        parquet_path = output_path.with_name("measurements_python.parquet")
        df.to_parquet(parquet_path, index=False)

        log_step("Save results (Parquet)", "Success")
        print(f"✅ Results also saved to {parquet_path}")
    except Exception as e:
        log_step("Save results (Parquet)", f"Failed: {e}")
        print(f"❌ Failed to save results to Parquet: {e}")


def process_temperatures(path_to_csv: Path) -> Dict[str, Dict[str, str]]:
    """
    Full processing pipeline: reads, computes, formats temperature statistics.
    """
    print("Starting temperature processing from CSV file...")
    start_time = time.time()

    temperature_data = read_temperatures(path_to_csv)
    stats = calculate_statistics(temperature_data)
    formatted = format_results(stats)
    save_results_to_file(formatted, OUTPUT_PATH)

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
