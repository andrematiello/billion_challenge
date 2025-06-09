# 🌡️ ONE BILLION CHALLENGE (OBRC) – Python Edition

## ABOUT THE PROJECT

> Uma jornada prática e realista de engenharia de dados para processar **1 bilhão de registros**, extraindo **estatísticas agregadas de temperatura** com performance, escalabilidade e elegância em Python.

---

## 🧠 Objetivo do Projeto

O projeto **One Billion Row Challenge (OBRC)** foi desenvolvido como um exercício avançado de **engenharia de dados aplicada**, com o objetivo de demonstrar como processar com eficiência um **arquivo massivo de 1 bilhão de linhas (~14GB)** usando **Python**. O foco está em realizar operações computacionalmente intensas — como **agregações** (mínimo, média e máximo) e **ordenação** — com uso criterioso de recursos computacionais.

Este projeto é particularmente útil como estudo de caso para engenheiros de dados, cientistas de dados e desenvolvedores que desejam aprofundar seus conhecimentos em **processamento de arquivos massivos**, **estratégias de chunking**, **desempenho de bibliotecas Python** e **uso de engines analíticas modernas** como o **DuckDB**.

---

## 🧬 Inspiração

O desafio foi inspirado no projeto original [1BRC](https://github.com/gunnarmorling/1brc), proposto por **Gunnar Morling** em Java, com o seguinte espírito:

> “Explore até onde as linguagens modernas podem ir ao processar um bilhão de linhas. Use todos os (v)núcleos, SIMD, otimizações de GC... e crie a implementação mais rápida para resolver esse problema!”

Posteriormente, a iniciativa foi adaptada para Python por **Luciano Vasconcelos**, no repositório [One-Billion-Row-Challenge-Python](https://github.com/lvgalvao/One-Billion-Row-Challenge-Python), como um workshop, dentro do contexto educacional da **Jornada de Dados**, em 2024.

---

## 🗂️ Estrutura dos Dados

O arquivo de entrada contém **medições de temperatura** de diferentes estações meteorológicas, com o seguinte formato por linha:

```text
<nome_da_estação>;<temperatura>
```

nome_da_estação: string
temperatura: float com precisão de duas casas decimais
Exemplo:
```text
Stockholm;-5.32
São Paulo;25.85
Cape Town;19.01
```


---

## 🔍 Desafio Proposto

Desenvolver soluções em Python para:

Ler o arquivo de entrada com 1 bilhão de linhas

Calcular, para cada estação:

- Temperatura mínima

- Temperatura máxima

- Temperatura média (com 1 casa decimal)

Ordenar os resultados por nome da estação

Exportar os resultados para os formatos .csv e .parquet

Comparar diferentes abordagens de performance, memória e escalabilidade

---

## 🧪 Abordagens Implementadas
1. 🔹 Leitura Linha a Linha (Streaming Puro - Python Nativo)
Uso de leitura sequencial com open() + readline()

Agregações realizadas em tempo real com dicionários

Estratégia eficiente em consumo de memória (low RAM footprint)

Ideal para ambientes com recursos limitados

2. 🔸 Chunking Manual (Python Nativo com Divisão em Blocos)
Técnica de leitura em blocos (ex: 1 milhão de linhas por vez)

Reduz picos de memória e melhora o controle do processamento

Útil para ajustes finos de performance e paralelização

3. 🐼 Pandas (DataFrame Completo)
Abordagem de leitura em lote único com pd.read_csv()

Permite uso de funções vetorizadas e agregações rápidas

Limitações para máquinas com <16GB RAM

4. 🧊 Pandas com Chunking (pd.read_csv(..., chunksize=N))
Divide o dataset em mini-DataFrames processados iterativamente

Une a performance do Pandas com escalabilidade de pipelines

Útil para ambientes em nuvem com controle de memória

5. 🦆 DuckDB (Processamento Colunar com SQL Embutido)
Engine analítica colunar embutida (sem servidor)

Altamente otimizada para workloads de leitura pesada

Permite uso de SQL para agregações diretas no arquivo .csv

Suporte nativo a .parquet, integração direta com Pandas, Apache Arrow e Python

## 📊 Exemplos de Saída
Formato de saída (ordenado alfabeticamente por nome da estação):

```python
| Estação    | Min    | Média | Max   |
| ---------- | ------ | ----- | ----- |
| Aabenraa   | -99.80 | 3.4   | 99.80 |
| Bariloche  | -57.40 | 8.2   | 87.30 |
| Copenhagen | -45.50 | 11.9  | 94.10 |
```

---

## 💾 Formatos de Saída Gerados
Todos os resultados finais são exportados nos seguintes formatos:

results_<metodo>.csv

results_<metodo>.parquet

Isso permite análises posteriores em ferramentas como Power BI, Metabase, Apache Superset ou puro Python.

---

## 📈 Benchmarking e Análise de Performance
Método	Tempo Estimado	Uso de Memória	Comentários
Python Nativo (streaming)	Alto	Muito baixo	Alta compatibilidade com ambientes limitados
Chunking Manual	Médio	Controlado	Equilíbrio entre controle e simplicidade
Pandas Completo	Baixo*	Alto	Muito rápido, mas exige boa RAM
Pandas com Chunking	Médio-baixo	Controlado	Ótima relação performance/memória
DuckDB SQL	Baixo	Muito baixo	Ideal para pipelines analíticos colunarizados

---

## 🧱 Tecnologias Utilizadas

### Project support
#### pre-commit hooks
trailing-whitespace
end-of-file-fixer
check-yaml
check-added-large-files
check-json
check-merge-conflict
check-case-conflict
#### pip-audit
#### black
#### ruff


### Project development

Python 3.11+

Pandas

DuckDB

Polars (explorado em experimentos complementares)

Poetry para gerenciamento de dependências

Pyenv para isolamento de ambientes

VSCode + WSL + Docker para desenvolvimento local

---

## MAIN TECHNICAL FEATURES

✅ Modular function design (read, calculate, format, log)
✅ Log file with timestamps and emojis for readability
✅ Automatic folder creation for logs
✅ Fast performance with native Python (no Pandas or NumPy required)
✅ Friendly CLI usage, expandable to larger systems

---

Project carried out with the support of Artificial Intelligence (ChatGPT);

For future improvements: extraction of real data with cleaning and transformation, followed by loading into a Data Warehouse, possibly in a cloud provider, also, an ETL orchestrated with Apache Airflow and best CI/CD practices.


## QUESTIONS, SUGGESTIONS OR FEEDBACK

**🚀 André Matiello C. Caramanti - [matiello.andre@hotmail.com](mailto:matiello.andre@hotmail.com)**

---

## LICENSE

[MIT License](https://andrematiello.notion.site/mit-license)
