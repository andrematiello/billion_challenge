# src/create_station_metrics_mart.py

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT = BASE_DIR / "data" / "measurements_duckDB.csv"
OUTPUT = BASE_DIR / "data" / "station_metrics_mart.csv"

# Lê CSV
df = pd.read_csv(INPUT, sep=";")

# Converte colunas numéricas com segurança
df["min"] = pd.to_numeric(df["min"], errors="coerce")
df["mean"] = pd.to_numeric(df["mean"], errors="coerce")
df["max"] = pd.to_numeric(df["max"], errors="coerce")

# Agrupa por estação e calcula estatísticas
df_out = (
    df.groupby("station")
    .agg(
        {
            "min": "min",
            "mean": "mean",
            "max": "max",
        }
    )
    .reset_index()
)

# Renomeia colunas para visualização
df_out.columns = [
    "Station",
    "Min Temperature (°C)",
    "Average Temperature (°C)",
    "Max Temperature (°C)",
]

# Salva como CSV
df_out.to_csv(OUTPUT, sep=";", index=False)
print(f"✅ Arquivo salvo em: {OUTPUT}")
