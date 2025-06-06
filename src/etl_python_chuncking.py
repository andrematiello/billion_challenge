# colocando tqdm e chuncking para melhorar a performance e o uso de memória

from csv import reader, writer
from collections import defaultdict
from pathlib import Path
from typing import Dict
import time
import datetime
from tqdm import tqdm

# ==== CONFIGURAÇÕES E CONSTANTES ====

BASE_DIR = Path(__file__).resolve().parent.parent  # Caminho base do projeto
PATH_CSV = BASE_DIR / "data" / "weather_stations.csv"  # Caminho do CSV de entrada
LOG_PATH = BASE_DIR / "logs" / "log_python_chunk.csv"  # Caminho do arquivo de log
OUTPUT_PATH = BASE_DIR / "data" / "measurements_python_chunk.csv"  # Caminho de saída
CHUNK_SIZE = 10_000_000  # Número de linhas lidas por chunk (ajustável)

# Garante que os diretórios 'data' e 'logs' existem
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# ==== FUNÇÃO DE LOG ====


def log_step(step: str, status: str) -> None:
    """Registra cada etapa no arquivo de log com timestamp."""
    with LOG_PATH.open("a", newline="") as log_file:
        log_writer = writer(log_file)
        timestamp = datetime.datetime.now().isoformat()
        if status.lower().startswith("success") or status.lower().startswith(
            "completed"
        ):
            status = "✅ " + status
        log_writer.writerow([timestamp, step, status])


# ==== PROCESSAMENTO DE CADA CHUNK ====


def process_chunk(chunk_rows, stats):
    """
    Processa um chunk de linhas, atualizando os agregados por estação.
    Em vez de guardar as temperaturas, armazena apenas os valores agregados.
    """
    for row in chunk_rows:
        if len(row) != 2:
            continue  # Pula linhas malformadas
        try:
            station = row[0]
            temp = float(row[1])
            # Atualiza agregados: contagem, soma, mínimo, máximo
            stats[station]["count"] += 1
            stats[station]["sum"] += temp
            stats[station]["min"] = min(stats[station]["min"], temp)
            stats[station]["max"] = max(stats[station]["max"], temp)
        except ValueError:
            continue  # Pula linhas com valores inválidos


# ==== LEITURA EM CHUNKS COM AGREGAÇÃO ====


def read_temperatures_in_chunks(
    path_to_csv: Path, chunk_size: int
) -> Dict[str, Dict[str, float]]:
    """
    Lê o arquivo CSV em chunks e agrega os dados por estação de forma incremental.
    """
    # Inicializa dicionário com agregados por estação
    stats = defaultdict(
        lambda: {"count": 0, "sum": 0.0, "min": float("inf"), "max": float("-inf")}
    )

    # Estima o total de linhas para a barra de progresso
    total_lines = sum(1 for _ in open(path_to_csv, encoding="utf-8"))

    try:
        with path_to_csv.open("r", encoding="utf-8") as file:
            csv_reader = reader(file, delimiter=";")
            chunk = []

            # Itera sobre as linhas do CSV com barra de progresso
            for row in tqdm(
                csv_reader, total=total_lines, desc="📥 Lendo em chunks", unit="linha"
            ):
                chunk.append(row)
                if len(chunk) >= chunk_size:
                    process_chunk(chunk, stats)  # Processa o chunk atual
                    chunk = []  # Limpa o chunk da memória

            # Processa as últimas linhas restantes (se houver)
            if chunk:
                process_chunk(chunk, stats)

        log_step("Read temperatures (chunked)", "Success")
        print("✅ Temperatures read and aggregated successfully.")
    except Exception as e:
        log_step("Read temperatures", f"Failed: {e}")
        raise

    return stats


# ==== FORMATAÇÃO FINAL ====


def format_results(stats: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, str]]:
    """
    Converte os resultados agregados em strings formatadas com 2 casas decimais.
    """
    sorted_stats = dict(sorted(stats.items()))  # Ordena por nome da estação
    formatted = {}

    for station, data in tqdm(
        sorted_stats.items(), desc="🧮 Formatando resultados", unit="estação"
    ):
        formatted[station] = {
            "min": f"{data['min']:.2f}",
            "mean": f"{data['sum'] / data['count']:.2f}",
            "max": f"{data['max']:.2f}",
        }

    log_step("Format results", f"Success: {len(formatted)} stations processed")
    print(f"✅ Results formatted successfully: {len(formatted)} stations processed.")
    return formatted


# ==== GRAVAÇÃO EM DISCO ====


def save_results_to_file(results: Dict[str, Dict[str, str]], output_path: Path) -> None:
    """
    Salva os resultados formatados em um arquivo CSV com delimitador ponto-e-vírgula.
    """
    try:
        with output_path.open("w", encoding="utf-8") as f:
            f.write("station;min;mean;max\n")
            for station, data in results.items():
                f.write(f"{station};{data['min']};{data['mean']};{data['max']}\n")
        log_step("Save results", "Success")
        print(f"✅ Results saved to {output_path}")
    except Exception as e:
        log_step("Save results", f"Failed: {e}")
        print(f"❌ Failed to save results: {e}")


# ==== PIPELINE PRINCIPAL ====


def process_temperatures(path_to_csv: Path):
    """
    Pipeline principal que organiza todo o fluxo de leitura, agregação, formatação e gravação.
    """
    print("🚀 Iniciando processamento com chunking otimizado...")
    start = time.time()

    # 1. Lê e agrega em tempo real
    stats = read_temperatures_in_chunks(path_to_csv, CHUNK_SIZE)

    # 2. Formata os resultados para saída
    formatted = format_results(stats)

    # 3. Salva o resultado final
    save_results_to_file(formatted, OUTPUT_PATH)

    # 4. Log final de desempenho
    elapsed = time.time() - start
    print(f"⏱️  Total processing completed in {elapsed:.2f} seconds.")
    log_step("Total processing", f"Completed in {elapsed:.2f} seconds")


# ==== EXECUÇÃO ====

if __name__ == "__main__":
    if not PATH_CSV.exists():
        print(f"❌ File {PATH_CSV} not found.")
        log_step("File check", "Failed: File not found")
    else:
        try:
            process_temperatures(PATH_CSV)
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            log_step("Process temperatures", f"Failed: {e}")
