import pandas as pd
from pathlib import Path
import time
import datetime
from csv import writer
from tqdm import tqdm

# === CONFIGURAÇÕES GERAIS ===

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "weather_stations.csv"
OUTPUT_CSV = BASE_DIR / "data" / "measurements_pandas_chunk.csv"
OUTPUT_PARQUET = BASE_DIR / "data" / "measurements_pandas_chunk.parquet"
LOG_PATH = BASE_DIR / "logs" / "log_pandas_chunk.csv"

# Garante que os diretórios de dados e logs existam
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)


def log_step(step: str, status: str) -> None:
    """Registra cada etapa do pipeline no arquivo de log com timestamp."""
    with LOG_PATH.open("a", newline="") as log_file:
        log_writer = writer(log_file)
        timestamp = datetime.datetime.now().isoformat()
        if status.lower().startswith("success") or status.lower().startswith(
            "completed"
        ):
            status = "✅ " + status
        log_writer.writerow([timestamp, step, status])


def process_with_pandas_chunked(chunksize=100_000_000):
    """
    Pipeline de processamento com Pandas usando leitura em chunks + barra de progresso.
    Inclui saída em CSV e Parquet, com logs e barra de progresso.
    """
    print("🚀 Starting ETL with pandas (chunked + tqdm)...")
    start_time = time.time()

    try:
        total_lines = sum(1 for _ in open(INPUT_PATH, encoding="utf-8")) - 1
        total_chunks = (total_lines // chunksize) + 1
        stats = {}

        for chunk in tqdm(
            pd.read_csv(
                INPUT_PATH,
                sep=";",
                names=["station", "temperature"],
                dtype={"station": str, "temperature": float},
                skiprows=1,
                chunksize=chunksize,
            ),
            total=total_chunks,
            desc="🔄 Processando chunks",
            unit="chunk",
        ):
            for station, group in chunk.groupby("station"):
                t_min = group["temperature"].min()
                t_max = group["temperature"].max()
                t_mean = group["temperature"].mean()

                if station not in stats:
                    stats[station] = {"min": t_min, "mean": [t_mean], "max": t_max}
                else:
                    stats[station]["min"] = min(stats[station]["min"], t_min)
                    stats[station]["max"] = max(stats[station]["max"], t_max)
                    stats[station]["mean"].append(t_mean)

        df_kpi = pd.DataFrame(
            [
                {
                    "station": st,
                    "min": f"{s['min']:.2f}",
                    "mean": f"{pd.Series(s['mean']).mean():.2f}",
                    "max": f"{s['max']:.2f}",
                }
                for st, s in stats.items()
            ]
        )

        df_kpi = df_kpi.sort_values("station")

        # === GRAVAÇÃO EM CSV ===
        df_kpi.to_csv(OUTPUT_CSV, index=False, sep=";")
        log_step("Save CSV", "Success")
        print(f"✅ Results saved to: {OUTPUT_CSV}")

        # === LINHA SEPARADORA NO LOG ===
        log_step("-----", "-----")

        # === GRAVAÇÃO EM PARQUET ===
        df_kpi.to_parquet(OUTPUT_PARQUET, index=False)
        log_step("Save Parquet", "Success")
        print(f"✅ Results saved to: {OUTPUT_PARQUET}")

    except Exception as e:
        log_step("Chunked processing", f"Failed: {e}")
        print(f"❌ Chunked processing failed: {e}")
        return

    elapsed = time.time() - start_time
    print(f"⏱️  Total processing time: {elapsed:.2f} seconds.")
    log_step("Total processing", f"Completed in {elapsed:.2f} seconds")


# === EXECUÇÃO ===

if __name__ == "__main__":
    if not INPUT_PATH.exists():
        print(f"❌ File {INPUT_PATH} not found.")
        log_step("File check", "Failed: File not found")
    else:
        process_with_pandas_chunked()
