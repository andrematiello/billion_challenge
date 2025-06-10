import streamlit as st
import pandas as pd
from pathlib import Path

# Caminho do arquivo CSV
csv_path = Path(__file__).resolve().parent.parent / "data" / "measurements_duckDB.csv"

# Título
st.title("📊 Tabela de Medidas - DuckDB")

# Verifica se o arquivo existe
if not csv_path.exists():
    st.error(f"Arquivo não encontrado: {csv_path}")
else:
    # Lê o CSV
    df = pd.read_csv(csv_path, sep=";")

    # Exibe como tabela interativa
    st.dataframe(df, use_container_width=True)
