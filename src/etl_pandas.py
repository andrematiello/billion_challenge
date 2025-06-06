# import pandas as pd
# from pathlib import Path
# import time
# import datetime
# from csv import writer

# # Paths and constants
# BASE_DIR = Path(__file__).resolve().parent.parent
# INPUT_PATH = BASE_DIR / "data" / "weather_stations.csv"
# OUTPUT_PATH = BASE_DIR / "data" / "measurements_pandas.csv"
# LOG_PATH = BASE_DIR / "logs" / "log_pandas.csv"

# # Ensure directories exist
# LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
# OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# def log_step(step: str, status: str) -> None:
#     with LOG_PATH.open("a", newline="") as log_file:
#         log_writer = writer(log_file)
#         timestamp = datetime.datetime.now().isoformat()
#         if status.lower().startswith("success") or status.lower().startswith(
#             "completed"
#         ):
#             status = "✅ " + status
#         log_writer.writerow([timestamp, step, status])


# def process_with_pandas():
#     print("Starting ETL with pandas...")
#     start_time = time.time()

#     try:
#         df = pd.read_csv(
#             INPUT_PATH,
#             sep=";",
#             names=["station", "temperature"],
#             dtype={"station": str, "temperature": float},
#             skiprows=1,
#         )
#         log_step("Read CSV", f"Success: {len(df)} rows loaded")
#         print(f"✅ CSV read successfully: {len(df)} rows loaded.")
#     except Exception as e:
#         log_step("Read CSV", f"Failed: {e}")
#         print(f"❌ Failed to read CSV: {e}")
#         return

#     try:
#         df_kpi = (
#             df.groupby("station")["temperature"]
#             .agg(["min", "mean", "max"])
#             .reset_index()
#         )
#         log_step("Aggregate stats", f"Success: {len(df_kpi)} stations processed")
#         print(f"✅ Statistics calculated successfully: {len(df_kpi)} stations.")
#     except Exception as e:
#         log_step("Aggregate stats", f"Failed: {e}")
#         print(f"❌ Failed to calculate statistics: {e}")
#         return

#     try:
#         df_sorted = df_kpi.sort_values("station")

#         # Formatando com duas casas decimais (como string)
#         df_sorted["min"] = df_sorted["min"].map("{:.2f}".format)
#         df_sorted["mean"] = df_sorted["mean"].map("{:.2f}".format)
#         df_sorted["max"] = df_sorted["max"].map("{:.2f}".format)

#         df_sorted.to_csv(OUTPUT_PATH, index=False, sep=";")
#         log_step("Save output", "Success")
#         print(f"✅ Results saved to: {OUTPUT_PATH}")
#     except Exception as e:
#         log_step("Save output", f"Failed: {e}")
#         print(f"❌ Failed to save results: {e}")
#         return

#     elapsed = time.time() - start_time
#     print(f"⏱️  Total processing time: {elapsed:.2f} seconds.")
#     log_step("Total processing", f"Completed in {elapsed:.2f} seconds")


# if __name__ == "__main__":
#     if not INPUT_PATH.exists():
#         print(f"❌ File {INPUT_PATH} not found.")
#         log_step("File check", "Failed: File not found")
#     else:
#         process_with_pandas()

# gravação em parquet, acima, comente em csv
import pandas as pd
from pathlib import Path
import time
import datetime
from csv import writer

# Paths and constants
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "weather_stations.csv"
OUTPUT_PATH = BASE_DIR / "data" / "measurements_pandas.csv"
OUTPUT_PARQUET = BASE_DIR / "data" / "measurements_pandas.parquet"
LOG_PATH = BASE_DIR / "logs" / "log_pandas.csv"

# Ensure directories exist
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_step(step: str, status: str) -> None:
    with LOG_PATH.open("a", newline="") as log_file:
        log_writer = writer(log_file)
        timestamp = datetime.datetime.now().isoformat()
        if status.lower().startswith("success") or status.lower().startswith(
            "completed"
        ):
            status = "✅ " + status
        log_writer.writerow([timestamp, step, status])


def process_with_pandas():
    print("Starting ETL with pandas...")
    start_time = time.time()

    try:
        df = pd.read_csv(
            INPUT_PATH,
            sep=";",
            names=["station", "temperature"],
            dtype={"station": str, "temperature": float},
            skiprows=1,
        )
        log_step("Read CSV", f"Success: {len(df)} rows loaded")
        print(f"✅ CSV read successfully: {len(df)} rows loaded.")
    except Exception as e:
        log_step("Read CSV", f"Failed: {e}")
        print(f"❌ Failed to read CSV: {e}")
        return

    try:
        df_kpi = (
            df.groupby("station")["temperature"]
            .agg(["min", "mean", "max"])
            .reset_index()
        )
        log_step("Aggregate stats", f"Success: {len(df_kpi)} stations processed")
        print(f"✅ Statistics calculated successfully: {len(df_kpi)} stations.")
    except Exception as e:
        log_step("Aggregate stats", f"Failed: {e}")
        print(f"❌ Failed to calculate statistics: {e}")
        return

    try:
        df_sorted = df_kpi.sort_values("station")

        # Formatando com duas casas decimais como string
        df_sorted["min"] = df_sorted["min"].map("{:.2f}".format)
        df_sorted["mean"] = df_sorted["mean"].map("{:.2f}".format)
        df_sorted["max"] = df_sorted["max"].map("{:.2f}".format)

        df_sorted.to_csv(OUTPUT_PATH, index=False, sep=";")
        log_step("Save CSV", "Success")
        print(f"✅ Results saved to: {OUTPUT_PATH}")
    except Exception as e:
        log_step("Save CSV", f"Failed: {e}")
        print(f"❌ Failed to save CSV: {e}")
        return

    # Linha separadora no log
    log_step("-----", "-----")

    try:
        df_sorted.to_parquet(OUTPUT_PARQUET, index=False)
        log_step("Save Parquet", "Success")
        print(f"✅ Results saved to: {OUTPUT_PARQUET}")
    except Exception as e:
        log_step("Save Parquet", f"Failed: {e}")
        print(f"❌ Failed to save Parquet: {e}")
        return

    elapsed = time.time() - start_time
    print(f"⏱️  Total processing time: {elapsed:.2f} seconds.")
    log_step("Total processing", f"Completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    if not INPUT_PATH.exists():
        print(f"❌ File {INPUT_PATH} not found.")
        log_step("File check", "Failed: File not found")
    else:
        process_with_pandas()
