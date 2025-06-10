# import streamlit as st
# import pandas as pd
# from pathlib import Path
# import plotly.express as px

# # 📂 Caminho do arquivo CSV
# csv_path = Path(__file__).resolve().parent.parent / "data" / "station_metrics_mart.csv"

# # 🧱 Título da página
# st.title("📊 Tabela de Medidas - DuckDB")

# # ✅ Verificação de existência do arquivo
# if not csv_path.exists():
#     st.error(f"❌ Arquivo não encontrado: {csv_path}")
# else:
#     # 🚑 Leitura do CSV com tratamento de erro
#     try:
#         df = pd.read_csv(csv_path, sep=";", nrows=1000)  # nrows temporário para teste
#         st.success("✅ CSV carregado com sucesso!")
#     except Exception as e:
#         st.error(f"❌ Erro ao ler o CSV: {e}")
#         st.stop()

#     # 📋 Tabela interativa com os dados
#     st.subheader("📋 Tabela com Estatísticas por Estação")
#     st.dataframe(df, use_container_width=True)

#     # 📈 Gráfico — Temperatura Média
#     st.subheader("📈 Temperatura Média por Estação")
#     fig_mean = px.bar(
#         df,
#         x="Station",
#         y="Average Temperature (°C)",
#         title="Temperatura Média por Estação",
#         labels={"Average Temperature (°C)": "Temperatura Média (°C)"},
#     )
#     st.plotly_chart(fig_mean, use_container_width=True)

#     # 🌡️ Gráfico — Temperatura Mínima
#     st.subheader("🌡️ Temperatura Mínima por Estação")
#     fig_min = px.bar(
#         df,
#         x="Station",
#         y="Min Temperature (°C)",
#         title="Temperatura Mínima por Estação",
#         labels={"Min Temperature (°C)": "Temp. Mínima (°C)"},
#         color="Min Temperature (°C)",
#         color_continuous_scale="blues",
#     )
#     st.plotly_chart(fig_min, use_container_width=True)

#     # 🔥 Gráfico — Temperatura Máxima
#     st.subheader("🔥 Temperatura Máxima por Estação")
#     fig_max = px.bar(
#         df,
#         x="Station",
#         y="Max Temperature (°C)",
#         title="Temperatura Máxima por Estação",
#         labels={"Max Temperature (°C)": "Temp. Máxima (°C)"},
#         color="Max Temperature (°C)",
#         color_continuous_scale="reds",
#     )
#     st.plotly_chart(fig_max, use_container_width=True)

# dashboard/app_duckdb_csv_table.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Caminho do arquivo CSV
csv_path = Path(__file__).resolve().parent.parent / "data" / "station_metrics_mart.csv"

# Título principal
st.set_page_config(page_title="Dashboard de Estações", layout="wide")
st.title("📊 Tabela de Medidas - DuckDB")


# Lê o CSV com cache para otimizar desempenho
@st.cache_data
def load_data(path):
    return pd.read_csv(path, sep=";")


# Verifica se arquivo existe e carrega dados
if not csv_path.exists():
    st.error(f"❌ Arquivo não encontrado: {csv_path}")
    st.stop()

try:
    df = load_data(csv_path)
except Exception as e:
    st.error(f"❌ Erro ao ler o CSV: {e}")
    st.stop()

# Filtro por estação
station_options = ["Todas"] + sorted(df["Station"].unique().tolist())
selected_station = st.selectbox("🔎 Selecione uma estação:", station_options)

if selected_station != "Todas":
    df_filtered = df[df["Station"] == selected_station]
else:
    df_filtered = df

# Métricas resumo (linha com 3 colunas)
col1, col2, col3 = st.columns(3)
col1.metric("🌡️ Média Geral", f"{df_filtered['Average Temperature (°C)'].mean():.2f} °C")
col2.metric("🔥 Máxima Geral", f"{df_filtered['Max Temperature (°C)'].max():.2f} °C")
col3.metric("❄️ Mínima Geral", f"{df_filtered['Min Temperature (°C)'].min():.2f} °C")

# Exibe tabela interativa
st.subheader("📋 Tabela com Estatísticas por Estação")
st.dataframe(df_filtered, use_container_width=True)

# Gráfico 1 — Temperatura média
st.subheader("📈 Temperatura Média por Estação")
fig_mean = px.bar(
    df_filtered,
    x="Station",
    y="Average Temperature (°C)",
    title="Temperatura Média por Estação",
    labels={"Average Temperature (°C)": "Temperatura Média (°C)"},
)
st.plotly_chart(fig_mean, use_container_width=True)

# Gráfico 2 — Temperatura mínima
st.subheader("🌡️ Temperatura Mínima por Estação")
fig_min = px.bar(
    df_filtered,
    x="Station",
    y="Min Temperature (°C)",
    title="Temperatura Mínima por Estação",
    labels={"Min Temperature (°C)": "Temp. Mínima (°C)"},
    color="Min Temperature (°C)",
    color_continuous_scale="blues",
)
st.plotly_chart(fig_min, use_container_width=True)

# Gráfico 3 — Temperatura máxima
st.subheader("🔥 Temperatura Máxima por Estação")
fig_max = px.bar(
    df_filtered,
    x="Station",
    y="Max Temperature (°C)",
    title="Temperatura Máxima por Estação",
    labels={"Max Temperature (°C)": "Temp. Máxima (°C)"},
    color="Max Temperature (°C)",
    color_continuous_scale="reds",
)
st.plotly_chart(fig_max, use_container_width=True)

# Gráfico 4 — Dispersão temperatura mínima vs máxima
st.subheader("📍 Dispersão: Temperaturas Mínima vs Máxima")
fig_scatter = px.scatter(
    df_filtered,
    x="Min Temperature (°C)",
    y="Max Temperature (°C)",
    size=df_filtered["Average Temperature (°C)"].abs(),  # <- aqui está a correção
    hover_name="Station",
    title="Relação entre Temp. Mínima e Máxima",
    labels={
        "Min Temperature (°C)": "Temp. Mínima (°C)",
        "Max Temperature (°C)": "Temp. Máxima (°C)",
    },
)
st.plotly_chart(fig_scatter, use_container_width=True)
# Rodapé com informações adicionais
st.markdown("---")
st.markdown(
    """
    <style>
        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
        Dashboard de Estações - Dados de Temperatura
    </div>
    """,
    unsafe_allow_html=True,
)
# Fim do script
