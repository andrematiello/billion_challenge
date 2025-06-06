# # import pandas as pd
# # from pathlib import Path
# # import time
# # import datetime
# # from csv import writer
# # from tqdm import tqdm

# # # Paths and constants
# # BASE_DIR = Path(__file__).resolve().parent.parent
# # INPUT_PATH = BASE_DIR / "data" / "weather_stations.csv"
# # OUTPUT_PATH = BASE_DIR / "data" / "measurements_pandas_chunk.csv"
# # LOG_PATH = BASE_DIR / "logs" / "log_pandas_chunk.csv"

# # # Ensure directories exist
# # LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
# # OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# # def log_step(step: str, status: str) -> None:
# #     with LOG_PATH.open("a", newline="") as log_file:
# #         log_writer = writer(log_file)
# #         timestamp = datetime.datetime.now().isoformat()
# #         if status.lower().startswith("success") or status.lower().startswith("completed"):
# #             status = "✅ " + status
# #         log_writer.writerow([timestamp, step, status])


# # def process_with_pandas_chunked(chunksize=1_000_000):
# #     print("Starting ETL with pandas (chunked + tqdm)...")
# #     start_time = time.time()

# #     try:
# #         # Estimar número total de linhas (exceto cabeçalho)
# #         total_lines = sum(1 for _ in open(INPUT_PATH, encoding="utf-8")) - 1
# #         total_chunks = (total_lines // chunksize) + 1

# #         stats = {}

# #         for chunk in tqdm(
# #             pd.read_csv(
# #                 INPUT_PATH,
# #                 sep=";",
# #                 names=["station", "temperature"],
# #                 dtype={"station": str, "temperature": float},
# #                 skiprows=1,
# #                 chunksize=chunksize,
# #             ),
# #             total=total_chunks,
# #             desc="🔄 Processando chunks",
# #             unit="chunk",
# #         ):
# #             for station, group in chunk.groupby("station"):
# #                 t_min = group["temperature"].min()
# #                 t_max = group["temperature"].max()
# #                 t_mean = group["temperature"].mean()

# #                 if station not in stats:
# #                     stats[station] = {"min": t_min, "mean": [t_mean], "max": t_max}
# #                 else:
# #                     stats[station]["min"] = min(stats[station]["min"], t_min)
# #                     stats[station]["max"] = max(stats[station]["max"], t_max)
# #                     stats[station]["mean"].append(t_mean)

# #         df_kpi = pd.DataFrame([
# #             {
# #                 "station": st,
# #                 "min": f"{s['min']:.2f}",
# #                 "mean": f"{pd.Series(s['mean']).mean():.2f}",
# #                 "max": f"{s['max']:.2f}",
# #             }
# #             for st, s in stats.items()
# #         ])

# #         df_kpi = df_kpi.sort_values("station")
# #         df_kpi.to_csv(OUTPUT_PATH, index=False, sep=";")

# #         log_step("Chunked processing", f"Success: {len(df_kpi)} stations processed")
# #         print(f"✅ Results saved to: {OUTPUT_PATH}")

# #     except Exception as e:
# #         log_step("Chunked processing", f"Failed: {e}")
# #         print(f"❌ Chunked processing failed: {e}")
# #         return

# #     elapsed = time.time() - start_time
# #     print(f"⏱️  Total processing time: {elapsed:.2f} seconds.")
# #     log_step("Total processing", f"Completed in {elapsed:.2f} seconds")


# # if __name__ == "__main__":
# #     if not INPUT_PATH.exists():
# #         print(f"❌ File {INPUT_PATH} not found.")
# #         log_step("File check", "Failed: File not found")
# #     else:
# #         process_with_pandas_chunked()


# import pandas as pd
# from pathlib import Path
# import time
# import datetime
# from csv import writer
# from tqdm import tqdm

# # === CONFIGURAÇÕES GERAIS ===

# BASE_DIR = Path(__file__).resolve().parent.parent
# INPUT_PATH = BASE_DIR / "data" / "weather_stations.csv"
# OUTPUT_PATH = BASE_DIR / "data" / "measurements_pandas_chunk.csv"
# LOG_PATH = BASE_DIR / "logs" / "log_pandas_chunk.csv"

# # Garante que os diretórios de dados e logs existam
# LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
# OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# def log_step(step: str, status: str) -> None:
#     """Registra cada etapa do pipeline no arquivo de log com timestamp."""
#     with LOG_PATH.open("a", newline="") as log_file:
#         log_writer = writer(log_file)
#         timestamp = datetime.datetime.now().isoformat()
#         if status.lower().startswith("success") or status.lower().startswith(
#             "completed"
#         ):
#             status = "✅ " + status
#         log_writer.writerow([timestamp, step, status])


# def process_with_pandas_chunked(chunksize=10_000_000):
#     """
#     Pipeline de processamento com Pandas usando leitura em chunks + barra de progresso.
#     Vantagens:
#     - Escalável: funciona mesmo com arquivos gigantes
#     - Econômico em memória: processa parte por parte
#     - Agregado em tempo real: não armazena todos os dados brutos
#     - Visual: usa tqdm para progresso
#     - Log automático: salva status de cada etapa
#     """
#     print("🚀 Starting ETL with pandas (chunked + tqdm)...")
#     start_time = time.time()

#     try:
#         # Estima o número total de linhas para barra de progresso
#         total_lines = sum(1 for _ in open(INPUT_PATH, encoding="utf-8")) - 1
#         total_chunks = (total_lines // chunksize) + 1

#         # Armazena estatísticas por estação com agregação incremental
#         stats = {}

#         # === LEITURA POR CHUNKS ===
#         for chunk in tqdm(
#             pd.read_csv(
#                 INPUT_PATH,
#                 sep=";",
#                 names=["station", "temperature"],
#                 dtype={"station": str, "temperature": float},
#                 skiprows=1,
#                 chunksize=chunksize,
#             ),
#             total=total_chunks,
#             desc="🔄 Processando chunks",
#             unit="chunk",
#         ):
#             # Agrupamento por estação e cálculo das estatísticas
#             for station, group in chunk.groupby("station"):
#                 t_min = group["temperature"].min()
#                 t_max = group["temperature"].max()
#                 t_mean = group["temperature"].mean()

#                 # Armazenamento eficiente de min, max e soma parcial de médias
#                 if station not in stats:
#                     stats[station] = {"min": t_min, "mean": [t_mean], "max": t_max}
#                 else:
#                     stats[station]["min"] = min(stats[station]["min"], t_min)
#                     stats[station]["max"] = max(stats[station]["max"], t_max)
#                     stats[station]["mean"].append(t_mean)

#         # === FORMATAÇÃO FINAL ===
#         # Cria DataFrame com as médias finais e formata com 2 casas decimais
#         df_kpi = pd.DataFrame(
#             [
#                 {
#                     "station": st,
#                     "min": f"{s['min']:.2f}",
#                     "mean": f"{pd.Series(s['mean']).mean():.2f}",
#                     "max": f"{s['max']:.2f}",
#                 }
#                 for st, s in stats.items()
#             ]
#         )

#         # Ordena por nome da estação
#         df_kpi = df_kpi.sort_values("station")

#         # === GRAVAÇÃO EM DISCO ===
#         df_kpi.to_csv(OUTPUT_PATH, index=False, sep=";")

#         log_step("Chunked processing", f"Success: {len(df_kpi)} stations processed")
#         print(f"✅ Results saved to: {OUTPUT_PATH}")

#     except Exception as e:
#         log_step("Chunked processing", f"Failed: {e}")
#         print(f"❌ Chunked processing failed: {e}")
#         return

#     # === TEMPO TOTAL ===
#     elapsed = time.time() - start_time
#     print(f"⏱️  Total processing time: {elapsed:.2f} seconds.")
#     log_step("Total processing", f"Completed in {elapsed:.2f} seconds")


# # === EXECUÇÃO ===

# if __name__ == "__main__":
#     if not INPUT_PATH.exists():
#         print(f"❌ File {INPUT_PATH} not found.")
#         log_step("File check", "Failed: File not found")
#     else:
#         process_with_pandas_chunked()

# gravação em parquet, acima, comente em csv
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


def process_with_pandas_chunked(chunksize=10_000_000):
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
