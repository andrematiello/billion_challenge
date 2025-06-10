from csv import reader, writer
from collections import defaultdict
from pathlib import Path
from typing import Dict
import time
import datetime
import pyarrow as pa
import pyarrow.parquet as pq

# 📁 Caminhos principais
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_CSV = BASE_DIR / "data" / "weather_stations.csv"  # Caminho do CSV de entrada
LOG_PATH = BASE_DIR / "logs" / "log_pyarrow.csv"  # Caminho do log
OUTPUT_CSV_PATH = (
    BASE_DIR / "data" / "measurements.pyarrow.csv"
)  # Caminho do CSV de saída
OUTPUT_PARQUET_PATH = OUTPUT_CSV_PATH.with_suffix(
    ".parquet"
)  # Caminho do Parquet de saída

# 🛠️ Garante que os diretórios existem
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

# 📝 Log incremental


def log_step(step: str, status: str) -> None:
    try:
        with LOG_PATH.open("a", newline="") as log_file:
            log_writer = writer(log_file)
            timestamp = datetime.datetime.now().isoformat()
            if status.lower().startswith("success") or status.lower().startswith(
                "completed"
            ):
                status = "✅ " + status
            log_writer.writerow([timestamp, step, status])
    except Exception as e:
        print(f"[LOG ERROR] Failed to write log: {e}")


# 📥 Lê CSV e realiza agregação incremental


def read_and_aggregate(path_to_csv: Path) -> Dict[str, Dict[str, float]]:
    stats = defaultdict(
        lambda: {"min": float("inf"), "max": float("-inf"), "sum": 0.0, "count": 0}
    )
    row_count = 0
    try:
        with path_to_csv.open("r", encoding="utf-8") as file:
            csv_reader = reader(file, delimiter=";")
            for row in csv_reader:
                row_count += 1
                if row_count % 50_000_000 == 0:
                    print(f"[DEBUG] Processed {row_count:,} lines...")
                if len(row) != 2:
                    continue
                try:
                    station = row[0]
                    temp = float(row[1])
                    s = stats[station]
                    s["min"] = min(s["min"], temp)
                    s["max"] = max(s["max"], temp)
                    s["sum"] += temp
                    s["count"] += 1
                except ValueError:
                    continue
        log_step(
            "Read and aggregate",
            f"Success: {len(stats)} stations from {row_count} lines",
        )
        print(f"✅ Aggregated {row_count:,} rows from {len(stats)} stations.")
    except Exception as e:
        log_step("Read and aggregate", f"Failed: {e}")
        raise
    return stats


# 🎯 Formata os dados (duas casas decimais e ordenação alfabética)


def format_results(stats: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, str]]:
    formatted = {}
    for station, values in stats.items():
        mean = values["sum"] / values["count"] if values["count"] else 0
        formatted[station] = {
            "min": f"{values['min']:.2f}",
            "mean": f"{mean:.2f}",
            "max": f"{values['max']:.2f}",
        }
    formatted = dict(sorted(formatted.items()))
    log_step("Format results", f"Success: {len(formatted)} stations")
    print(f"✅ Results formatted: {len(formatted)} stations.")
    return formatted


# 💾 Salva em CSV


def save_results_to_csv(results: Dict[str, Dict[str, str]], path: Path) -> None:
    try:
        with path.open("w", encoding="utf-8") as f:
            f.write("station;min;mean;max\n")
            for station, data in results.items():
                f.write(f"{station};{data['min']};{data['mean']};{data['max']}\n")
        log_step("Save results (CSV)", "Success")
        print(f"✅ Results saved to {path}")
    except Exception as e:
        log_step("Save results (CSV)", f"Failed: {e}")
        print(f"❌ Failed to save CSV: {e}")


# 📦 Salva em Parquet com pyarrow


def save_results_to_parquet(results: Dict[str, Dict[str, str]], path: Path) -> None:
    try:
        table = pa.table(
            {
                "station": list(results.keys()),
                "min": [v["min"] for v in results.values()],
                "mean": [v["mean"] for v in results.values()],
                "max": [v["max"] for v in results.values()],
            }
        )
        pq.write_table(table, path)
        log_step("Save results (Parquet)", "Success")
        print(f"✅ Results saved to {path}")
    except Exception as e:
        log_step("Save results (Parquet)", f"Failed: {e}")
        print(f"❌ Failed to save Parquet: {e}")


# 🔁 Pipeline principal


def process_temperatures():
    print("🚀 Starting temperature processing from CSV file...")
    start = time.time()
    stats = read_and_aggregate(PATH_CSV)
    formatted = format_results(stats)
    save_results_to_csv(formatted, OUTPUT_CSV_PATH)
    save_results_to_parquet(formatted, OUTPUT_PARQUET_PATH)
    elapsed = time.time() - start
    print(f"⏱️  Total processing completed in {elapsed:.2f} seconds.")
    log_step("⏱️  Total processing", f"Completed in {elapsed:.2f} seconds")


# ▶️ Execução
if __name__ == "__main__":
    print(f"[DEBUG] BASE_DIR: {BASE_DIR}")
    print(f"[DEBUG] PATH_CSV: {PATH_CSV}")
    print(f"[DEBUG] LOG_PATH: {LOG_PATH}")
    print(f"[DEBUG] OUTPUT_CSV_PATH: {OUTPUT_CSV_PATH}")
    print(f"[DEBUG] OUTPUT_PARQUET_PATH: {OUTPUT_PARQUET_PATH}")

    if not PATH_CSV.exists():
        print(f"❌ File {PATH_CSV} not found.")
        log_step("File check", "Failed: File not found")
    else:
        try:
            process_temperatures()
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            log_step("Process temperatures", f"Failed: {e}")
