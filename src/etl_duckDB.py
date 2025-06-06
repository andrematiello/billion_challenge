import duckdb
import time
import datetime
from pathlib import Path
from csv import writer

# === Caminhos do projeto ===
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "weather_stations.csv"
OUTPUT_PATH = BASE_DIR / "data" / "measurements_duckDB.csv"
LOG_PATH = BASE_DIR / "logs" / "log_duckDB.csv"

# === Garantir que diretórios existam ===
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_step(step: str, status: str) -> None:
    """
    Registra uma etapa no log, com timestamp e status.
    """
    with LOG_PATH.open("a", newline="") as log_file:
        log_writer = writer(log_file)
        timestamp = datetime.datetime.now().isoformat()
        if status.lower().startswith("success") or status.lower().startswith(
            "completed"
        ):
            status = "✅ " + status
        log_writer.writerow([timestamp, step, status])


def process_with_duckdb():
    """
    Pipeline com DuckDB:
    - Lê CSV sem cabeçalho
    - Define colunas manualmente
    - Executa agregações SQL
    - Salva CSV final ordenado
    - Gera log detalhado
    """
    print("🚀 Iniciando processamento com DuckDB...")
    start = time.time()

    try:
        con = duckdb.connect(database=":memory:")
        log_step("Conexão DuckDB", "Success")

        # Cria uma tabela temporária com os dados agregados
        con.execute(
            f"""
            CREATE TABLE results AS
            SELECT
                station,
                ROUND(MIN(temperature), 2) AS min,
                ROUND(AVG(temperature), 2) AS mean,
                ROUND(MAX(temperature), 2) AS max
            FROM read_csv_auto(
                '{INPUT_PATH.as_posix()}',
                delim=';',
                header=False,
                columns={{'station': 'VARCHAR', 'temperature': 'DOUBLE'}}
            )
            GROUP BY station
            ORDER BY station;
        """
        )
        log_step("Agregação executada", "Success")

        # Conta quantas estações distintas foram processadas
        result = con.execute("SELECT COUNT(*) FROM results").fetchone()[0]
        log_step("Contagem de estações", f"Success: {result} stations processed")

        # Exporta o resultado para CSV
        con.execute(
            f"""
            COPY results TO '{OUTPUT_PATH.as_posix()}'
            (FORMAT CSV, HEADER TRUE, DELIMITER ';');
        """
        )
        log_step("Exportação para CSV", "Success")

        print(f"✅ Resultados salvos em: {OUTPUT_PATH}")
        print(f"📊 Estações processadas: {result}")

    except Exception as e:
        log_step("ETL DuckDB", f"Failed: {e}")
        print(f"❌ Falha no processamento: {e}")
        return

    elapsed = time.time() - start
    print(f"⏱️  Tempo total: {elapsed:.2f} segundos.")
    log_step("Processamento finalizado", f"Completed in {elapsed:.2f} seconds")


# === Execução principal ===
if __name__ == "__main__":
    if not INPUT_PATH.exists():
        print(f"❌ Arquivo {INPUT_PATH} não encontrado.")
        log_step("Checagem do arquivo", "Failed: File not found")
    else:
        process_with_duckdb()
