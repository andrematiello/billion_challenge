import streamlit as st
import pandas as pd
import time
import os
import concurrent.futures

# Caminho base dos dados
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "data"

# Arquivos e títulos
artefatos = [
    ("measurements_duckDB.csv", "🔹 DuckDB CSV"),
    ("measurements_duckDB.parquet", "🔸 DuckDB Parquet"),
    ("measurements_pandas.csv", "🔹 Pandas CSV"),
    ("measurements_pandas.parquet", "🔸 Pandas Parquet"),
    ("measurements_python.csv", "🔹 Python CSV"),
    ("measurements_python.parquet", "🔸 Python Parquet"),
]


def carregar_arquivo(nome_arquivo, titulo):
    caminho = os.path.join(BASE_PATH, nome_arquivo)
    try:
        inicio = time.time()
        if nome_arquivo.endswith(".csv"):
            df = pd.read_csv(caminho, sep=";")
        elif nome_arquivo.endswith(".parquet"):
            df = pd.read_parquet(caminho)
        tempo = time.time() - inicio
        return (titulo, df, tempo, None)
    except Exception as e:
        return (titulo, None, None, str(e))


def exibir_tabela(titulo, df, tempo, erro):
    with st.container():
        st.subheader(titulo)
        if erro:
            st.error(f"Erro ao carregar: {erro}")
        elif df is not None:
            st.caption(f"⏱️ Tempo de carregamento: {tempo:.4f} segundos")
            st.dataframe(df)
        else:
            st.warning("Arquivo não encontrado ou vazio.")


# Título principal
st.title("📊 Comparativo de Artefatos - ETL Weather Stations")

# Carregamento paralelo dos arquivos
with concurrent.futures.ThreadPoolExecutor() as executor:
    resultados = list(executor.map(lambda args: carregar_arquivo(*args), artefatos))

# Exibição das tabelas
for titulo, df, tempo, erro in resultados:
    exibir_tabela(titulo, df, tempo, erro)
