# ONE BILLION CHALLENGE – PYTHON EDITION

## ABOUT THE PROJECT

Uma jornada prática e realista de engenharia de dados para processar 1 bilhão de registros, extraindo estatísticas agregadas de temperatura com performance, escalabilidade em Python, utilizando o projeto **One Billion Row Challenge**, desenvolvido como um exercício avançado de engenharia de dados aplicada, com o objetivo de demonstrar como processar com eficiência um arquivo massivo de 1 bilhão de linhas (~14GB) usando Python, cujo foco está em realizar operações computacionalmente intensas como agregações (mínimo, média e máximo) e ordenação com uso criterioso de recursos computacionais, de forma escalável.

Este projeto é particularmente útil como estudo de caso para engenheiros de dados, cientistas de dados e desenvolvedores que desejam aprofundar seus conhecimentos em processamento de arquivos massivos, estratégias de chunking, desempenho de bibliotecas Python e uso de engines analíticas modernas como o DuckDB e embora o One Billion Row Challenge não seja um projeto técnico, ele simula situações reais de negócio enfrentadas por empresas que lidam com grandes volumes de dados transacionais, sensoriais ou operacionais.

## INSPIRATION

O desafio foi inspirado no projeto original [1BRC](https://github.com/gunnarmorling/1brc), proposto por Gunnar Morling em Java, com o espírito:

> “Explore até onde as linguagens modernas podem ir ao processar um bilhão de linhas, use todos os (v)núcleos, SIMD, otimizações de GC... e crie a implementação mais rápida para resolver esse problema!”

Posteriormente, a iniciativa foi adaptada para Python por Luciano Vasconcelos, no repositório [One-Billion-Row-Challenge-Python](https://github.com/lvgalvao/One-Billion-Row-Challenge-Python), como um workshop, dentro do contexto educacional da Jornada de Dados, em 2024.


---

## BUSINESS PROBLEM

A seguir, destacam-se os principais problemas que esse case ajuda a resolver:

➡️ 1. Processamento de Grandes Volumes de Dados em Arquivos Brutos, quando empresas frequentemente recebem dados em formatos como .csv, .json ou .parquet contendo milhões ou bilhões de linhas, especialmente em setores como varejo, energia, climatologia, IoT e telecom, demonstrando como ler, limpar e agregar dados diretamente de arquivos massivos, sem a necessidade imediata de carregar tudo na memória ou depender de clusters caros.

➡️ 2. Cálculo Eficiente de Estatísticas Agregadas, por meio da análise de dados operacionais exige cálculos como média, máximo e mínimo, que parecem simples, mas se tornam desafiadores com grande volume e múltiplas chaves, o case mostra como aplicar estratégias otimizadas de agregação, inclusive via DuckDB ou Pandas com chunking, simulando o cálculo de indicadores operacionais em escala.

➡️ 3. Desempenho e Otimização de Recursos Computacionais, quando projetos de dados nem sempre rodam em ambientes robustos, muitos times enfrentam limitações de RAM, CPU e I/O, especialmente em pipelines locais, servidores intermediários ou jobs agendados, explorando estratégias de baixo consumo de memória, chunking e uso de engines colunares (como DuckDB) que permitem otimizar desempenho mesmo em máquinas comuns.

➡️ 4. Validação de Arquiteturas Analíticas para Batch Processing, no processo de validação, por exemplo, se uma arquitetura (ex: processamento local + exportação .parquet) atende aos SLAs de tempo e custo antes de mover dados para a nuvem, fornecendo um sandbox completo e replicável, permitindo testar pipelines de processamento, benchmarkar formatos de arquivo e comparar abordagens de leitura e agregação.

➡️ 5. Treinamento e Capacitação Técnica de Times de Dados, para formar times com maturidade em engenharia de dados exige cases práticos e desafiadores, que vão além de notebooks pequenos ou datasets de toy, demonstrando ser um estudo de caso avançado que pode ser usado para treinar engenheiros, analistas e cientistas de dados, com foco em performance, arquitetura de dados e boas práticas de codificação.

➡️ 6. Exportação de Dados para Consumo em BI e Visualizações, etapa comum a necessidade de transformar arquivos brutos em formatos eficientes para dashboards (como .csv limpo ou .parquet otimizado), gerando outputs padronizados e ordenados para ingestão por ferramentas como Power BI, Metabase, Superset ou soluções em nuvem, com foco em consumo rápido e leve.

---

## PROPOSED CHALLENGE

Desenvolver soluções em Python para:

🔹Ler o arquivo de entrada com 1 bilhão de linhas

🔹Calcular, para cada estação:
- Temperatura mínima
- Temperatura máxima
- Temperatura média (com 2 casas decimais)

🔹Ordenar os resultados por nome da estação

🔹Exportar os resultados para os formatos .csv e .parquet

🔹Comparar diferentes abordagens de performance, memória e escalabilidade

### DATA STRUCTURE

O arquivo de entrada contém medições de temperatura de diferentes estações meteorológicas, com o seguinte formato por linha:

### GENERAL OPERATION

1. Validação dos Argumentos, pois o script recebe como argumento a quantidade de linhas a serem geradas.

2. Coleta de Nomes de Estações, lê um arquivo chamado `model.csv` com nomes de estações meteorológicas.

3. Remove duplicatas e ignora linhas comentadas com `#`, ainda devolve uma estimativa de tamanho do arquivo

4. Calcula o tamanho estimado do arquivo final com base na média de caracteres dos nomes das estações e nas temperaturas geradas, com a geração de dados sintéticos

5. Cria medições com temperaturas aleatórias entre -99.9°C e 99.9°C e gera o arquivo `data/weather_stations.csv`.

6. Utiliza processamento em batches de 10.000 registros para melhor desempenho de escrita e apresenta uma barra de progresso ao longo da execução.

7. Medições de Performance sendo que ao final, mostra o tempo total de execução e o tamanho real do arquivo gerado.

### OUTPUT FILE

Arquivo gerado `data/weather_stations.csv` em 6 min e 5 seg, com 14.8 GiB, somando 1 bilhão de linhas.

```text
<nome_da_estação>;<temperatura>
```
- nome_da_estação: string
- temperatura: float com precisão de duas casas decimais

Exemplo:

```text
Stockholm;-5.32
São Paulo;25.85
Cape Town;19.01
```

### INTERESTING TECHNICAL POINTS

- Evita uso de `round()` para performance, usando `f"{x:.1f}"` para limitar casas decimais
- Usa `random.choices()` para gerar estações com distribuição uniforme entre nomes válidos
- Escreve dados em lote para evitar overhead de I/O, linha a linha
- Estima o uso de disco antes da geração, com função personalizada para conversão de bytes
- Fornece mensagens amigáveis de erro e ajuda ao usuário


### IMPLEMENTED APPROACHES

🔹 Leitura Linha a Linha (Streaming Puro - Python Nativo)
- Uso de leitura sequencial com open() + readline()
- Agregações realizadas em tempo real com dicionários
- Estratégia eficiente em consumo de memória (low RAM footprint)
- Ideal para ambientes com recursos limitados

🔹 Chunking Manual (Python Nativo com Divisão em Blocos)
- Técnica de leitura em blocos (ex: 1 milhão de linhas por vez)
- Reduz picos de memória e melhora o controle do processamento
- Útil para ajustes finos de performance e paralelização

🔹 Pandas (DataFrame Completo)
- Abordagem de leitura em lote único com pd.read_csv()
- Permite uso de funções vetorizadas e agregações rápidas
- Limitações para máquinas com <16GB RAM

🔹 Pandas com Chunking (pd.read_csv(..., chunksize=N))
- Divide o dataset em mini-DataFrames processados iterativamente
- Une a performance do Pandas com escalabilidade de pipelines
- Útil para ambientes em nuvem com controle de memória

🔹 DuckDB (Processamento Colunar com SQL Embutido)
- Engine analítica colunar embutida (sem servidor)
- Altamente otimizada para workloads de leitura pesada
- Permite uso de SQL para agregações diretas no arquivo .csv
- Suporte nativo a .parquet, integração direta com Pandas, Apache Arrow e Python

---

## HOW TO RUN

### REQUIREMENTS

1. Git e Github: Utilizado para versionamento do código e para repositório remoto do projeto.
Você deve ter o Git instalado em sua máquina e também deve ter uma conta no GitHub.
[Instruções de instalação do Git aqui](https://git-scm.com/doc).
[Instruções de instalação do Github aqui](https://docs.github.com/pt).

2. Pyenv: É usado para gerenciar versões do Python em ambientes virtuais, fundamental para isolar a aplicação e evitar problemas de conflitos entre versões de bibliotecas e do próprio Python.
[Instruções de instalação do Pyenv aqui](https://github.com/pyenv/pyenv#installation).
Neste projeto, vamos utilizar o Python 3.11.4

3. Poetry: Este projeto utiliza Poetry para gerenciamento de dependências.
[Instruções de instalação do Poetry aqui](https://python-poetry.org/docs/#installation).

### INSTALAÇÃO E CONFIGURAÇÃO

A - Execute o comando, passando os argumentos da quantidade de linhas que quer gerar:

```python
python create_measurements.py 1_000_000_000
```
---

B - Entre no diretório `/data/`e execute o comando, de acordo com a ferramenta e amodelagem de dados desejada:

i) Python
```python
python etl_python.py
```

ii) Python com chuncking
```python
python etl_python_chuncking.py
```

iii) Pandas
```python
python etl_pandas.py
```

iv) Pandas com chuncking
```python
python etl_pandas_chuncking.py
```
---

C - Instale a biblioteca duckDB, utilizando o Poetry, com o comando:
```python
poetry add duckdb
```

v) duckDB
```python
python etl_duckDB.py
```

## OUTPUT EXAMPLES

Todos os resultados finais são exportados nos formatos .csv e .parquet

Isso permite análises posteriores em ferramentas como Power BI, Metabase, Apache Superset ou puro Python.Formato de saída (ordenado alfabeticamente por nome da estação):

```python
| Estação    | Min    | Média | Max   |
| ---------- | ------ | ----- | ----- |
| Aabenraa   | -99.80 | 3.4   | 99.80 |
| Bariloche  | -57.40 | 8.2   | 87.30 |
| Copenhagen | -45.50 | 11.9  | 94.10 |
```

---

## TECHNOLOGIES USED

### PROJECT SUPPORT

🔹 Poetry para gerenciamento de dependências

🔹 Pyenv para isolamento de ambientes

🔹 Pre-commit hooks:
- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-added-large-files
- check-json
- check-merge-conflict
- check-case-conflict

🔹 Pip-audit

🔹 Black

🔹 Ruff


### PROJECT DEVELOPMENT

🔹Python 3.11+

🔹Pandas

🔹DuckDB

🔹Polars

---

## BENCHMARKING AND PERFORMANCE

Método	Tempo Estimado	Uso de Memória	Comentários
Python Nativo (streaming)	Alto	Muito baixo	Alta compatibilidade com ambientes limitados
Chunking Manual	Médio	Controlado	Equilíbrio entre controle e simplicidade
Pandas Completo	Baixo*	Alto	Muito rápido, mas exige boa RAM
Pandas com Chunking	Médio-baixo	Controlado	Ótima relação performance/memória
DuckDB SQL	Baixo	Muito baixo	Ideal para pipelines analíticos colunarizados

---

## MAIN TECHNICAL FEATURES

✅ Modular function design (read, calculate, format, log)

✅ Log file with timestamps and emojis for readability

✅ Automatic folder creation for logs

✅ Fast performance with native Python (no Pandas or NumPy required)

✅ Friendly CLI usage, expandable to larger systems

---

Project carried out with the support of Artificial Intelligence (ChatGPT)

For future improvements: extraction of real data with cleaning and transformation, followed by loading into a Data Warehouse, possibly in a cloud provider, also, an ETL orchestrated with Apache Airflow and best CI/CD practices


## QUESTIONS, SUGGESTIONS OR FEEDBACK

**🚀 André Matiello C. Caramanti - [matiello.andre@hotmail.com](mailto:matiello.andre@hotmail.com)**

---

## LICENSE

[MIT License](https://andrematiello.notion.site/mit-license)
