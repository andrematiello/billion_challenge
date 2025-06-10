from csv import writer
from pathlib import Path
import time
import datetime
import polars as pl

# 📁 Caminhos principais
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_CSV = BASE_DIR / "data" / "weather_stations.csv"
LOG_PATH = BASE_DIR / "logs" / "log_python.csv"
OUTPUT_CSV_PATH = BASE_DIR / "data" / "measurements_python.csv"
OUTPUT_PARQUET_PATH = OUTPUT_CSV_PATH.with_suffix(".parquet")

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


# 📥 Lê e processa com Polars Lazy (streaming seguro)
def read_and_aggregate_with_polars_lazy(path_to_csv: Path) -> pl.DataFrame:
    try:
        print("📥 Lendo arquivo CSV com Polars (modo lazy)...")
        df_lazy = (
            pl.scan_csv(
                path_to_csv,
                separator=";",
                has_header=False,
                new_columns=["station", "temperature"],
            )
            .group_by("station")
            .agg(
                [
                    pl.col("temperature").min().alias("min"),
                    pl.col("temperature").mean().alias("mean"),
                    pl.col("temperature").max().alias("max"),
                ]
            )
            .sort("station")
            .with_columns(
                [
                    pl.col("min").round(2),
                    pl.col("mean").round(2),
                    pl.col("max").round(2),
                ]
            )
        )
        df = df_lazy.collect()
        log_step("Read and aggregate (Polars lazy)", f"Success: {df.height} stations")
        print(f"✅ Aggregation complete: {df.height} stations")
        return df
    except Exception as e:
        log_step("Read and aggregate (Polars lazy)", f"Failed: {e}")
        raise


# 💾 Salva resultados
def save_results(df: pl.DataFrame, csv_path: Path, parquet_path: Path) -> None:
    try:
        df.write_csv(csv_path, separator=";")
        log_step("Save results (CSV)", "Success")
        print(f"✅ Results saved to {csv_path}")
    except Exception as e:
        log_step("Save results (CSV)", f"Failed: {e}")
        print(f"❌ Failed to save CSV: {e}")

    try:
        df.write_parquet(parquet_path)
        log_step("Save results (Parquet)", "Success")
        print(f"✅ Results saved to {parquet_path}")
    except Exception as e:
        log_step("Save results (Parquet)", f"Failed: {e}")
        print(f"❌ Failed to save Parquet: {e}")


# 🔁 Pipeline principal
def process_with_polars():
    print("🚀 Starting temperature processing with Polars (lazy)...")
    start = time.time()
    df = read_and_aggregate_with_polars_lazy(PATH_CSV)
    save_results(df, OUTPUT_CSV_PATH, OUTPUT_PARQUET_PATH)
    elapsed = time.time() - start
    print(f"⏱️  Total processing completed in {elapsed:.2f} seconds.")
    log_step("⏱️  Total processing (Polars lazy)", f"Completed in {elapsed:.2f} seconds")


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
            process_with_polars()
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            log_step("Process temperatures (Polars lazy)", f"Failed: {e}")
