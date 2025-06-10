from csv import reader, writer
from collections import defaultdict
from pathlib import Path
import time
import datetime
import pandas as pd

# 📁 Caminhos principais
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_CSV = BASE_DIR / "data" / "weather_stations.csv"
INTERMEDIATE_PATH = BASE_DIR / "data" / "intermediate_stats.csv"
OUTPUT_CSV_PATH = BASE_DIR / "data" / "measurements_python.csv"
OUTPUT_PARQUET_PATH = OUTPUT_CSV_PATH.with_suffix(".parquet")
LOG_PATH = BASE_DIR / "logs" / "log_python.csv"

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


# 🔁 Passo 1: Agregação incremental (sem listas)
def first_pass_aggregate(path_to_csv: Path, intermediate_path: Path):
    station_stats = defaultdict(
        lambda: {"sum": 0.0, "count": 0, "min": float("inf"), "max": float("-inf")}
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
                    station = str(row[0])
                    temp = float(row[1])
                    stats = station_stats[station]
                    stats["sum"] += temp
                    stats["count"] += 1
                    stats["min"] = min(stats["min"], temp)
                    stats["max"] = max(stats["max"], temp)
                except ValueError:
                    continue

        with intermediate_path.open("w", encoding="utf-8") as f:
            f.write("station;sum;count;min;max\n")
            for station, stats in station_stats.items():
                line = f"{station};{stats['sum']};{stats['count']};{stats['min']};{stats['max']}\n"
                f.write(line)

        log_step(
            "First pass aggregation",
            f"Success: {len(station_stats)} stations from {row_count} lines",
        )
        print(f"✅ First pass complete: {row_count:,} lines processed.")
    except Exception as e:
        log_step("First pass aggregation", f"Failed: {e}")
        raise


# 🧮 Passo 2: Cálculo final e exportação
def second_pass_compute(
    intermediate_path: Path, output_csv: Path, output_parquet: Path
):
    try:
        df = pd.read_csv(intermediate_path, sep=";")
        df["mean"] = df["sum"] / df["count"]
        df = df[["station", "min", "mean", "max"]]
        df = df.sort_values("station")
        df.to_csv(output_csv, sep=";", index=False)
        df.to_parquet(output_parquet, index=False)
        log_step("Second pass compute", "Success")
        print("✅ Final results saved to CSV and Parquet.")
    except Exception as e:
        log_step("Second pass compute", f"Failed: {e}")
        print(f"❌ Failed to compute final stats: {e}")


# 🔁 Execução completa
def process_temperatures():
    print("🚀 Starting 2-pass processing for massive CSV...")
    start_time = time.time()

    first_pass_aggregate(PATH_CSV, INTERMEDIATE_PATH)
    second_pass_compute(INTERMEDIATE_PATH, OUTPUT_CSV_PATH, OUTPUT_PARQUET_PATH)

    elapsed = time.time() - start_time
    print(f"⏱️  Total processing completed in {elapsed:.2f} seconds.")
    log_step("⏱️  Total processing", f"Completed in {elapsed:.2f} seconds")


# ▶️ Execução principal
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
