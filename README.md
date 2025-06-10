# ONE BILLION CHALLENGE – PYTHON EDITION

## ABOUT THE PROJECT

Uma jornada prática e realista de engenharia de dados para processar 1 bilhão de registros, extraindo estatísticas agregadas de temperatura com performance, escalabilidade em Python, utilizando o projeto One Billion Row Challenge, desenvolvido como um exercício avançado de engenharia de dados aplicada, com o objetivo de demonstrar como processar com eficiência um arquivo massivo de 1 bilhão de linhas (~14GB) usando Python, cujo foco está em realizar operações computacionalmente intensas como agregações (mínimo, média e máximo) e ordenação com uso criterioso de recursos computacionais, de forma escalável.

Este projeto é particularmente útil como estudo de caso para engenheiros de dados, cientistas de dados e desenvolvedores que desejam aprofundar seus conhecimentos em processamento de arquivos massivos, estratégias de chunking, desempenho de bibliotecas Python e uso de engines analíticas modernas como o DuckDB e embora o One Billion Row Challenge não seja um projeto técnico, ele simula situações reais de negócio enfrentadas por empresas que lidam com grandes volumes de dados transacionais, sensoriais ou operacionais.

## INSPIRATION

O desafio foi inspirado no projeto original [1BRC](https://github.com/gunnarmorling/1brc), proposto por Gunnar Morling, em Java, posteriormente, a iniciativa foi adaptada para Python por Luciano Vasconcelos, no repositório [One-Billion-Row-Challenge-Python](https://github.com/lvgalvao/One-Billion-Row-Challenge-Python), como um workshop, dentro do contexto educacional da Jornada de Dados, em 2024.

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

---

### GENERAL OPERATION

1. Validação dos Argumentos, pois o script recebe como argumento a quantidade de linhas a serem geradas.

2. Coleta de Nomes de Estações, lê um arquivo chamado `model.csv` com nomes de estações meteorológicas.

3. Remove duplicatas e ignora linhas comentadas com `#`, ainda devolve uma estimativa de tamanho do arquivo

4. Calcula o tamanho estimado do arquivo final com base na média de caracteres dos nomes das estações e nas temperaturas geradas, com a geração de dados sintéticos

5. Cria medições com temperaturas aleatórias entre -99.9°C e 99.9°C e gera o arquivo `data/weather_stations.csv`.

6. Utiliza processamento em batches de 10.000 registros para melhor desempenho de escrita e apresenta uma barra de progresso ao longo da execução.

7. Medições de Performance sendo que ao final, mostra o tempo total de execução e o tamanho real do arquivo gerado.

---

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
---

### INTERESTING TECHNICAL POINTS

- Evita uso de `round()` para performance, usando `f"{x:.1f}"` para limitar casas decimais
- Usa `random.choices()` para gerar estações com distribuição uniforme entre nomes válidos
- Escreve dados em lote para evitar overhead de I/O, linha a linha
- Estima o uso de disco antes da geração, com função personalizada para conversão de bytes
- Fornece mensagens amigáveis de erro e ajuda ao usuário

---

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

---

### INSTALAÇÃO E CONFIGURAÇÃO

A - Execute o comando, passando os argumentos da quantidade de linhas que quer gerar:

```python
python create_measurements.py 1_000_000_000
```
---

B - Confirmar a quantidade de linhas e o formato do arquivo gerado:
```python
wc -l ../data/weather_stations.csv
head -n 5 ../data/weather_stations.csv
```

C - Entre no diretório `/data/`e execute o comando, de acordo com a ferramenta e amodelagem de dados desejada:

1) Python - processamento BRUTO com `defaultdict`, utilizando Python vanilla!
```python
python etl_python.py
```

2) Python com chuncking
```python
python etl_python_chuncking.py
```

3) Pandas
```python
python etl_pandas.py
```

4) Pandas com chuncking
```python
python etl_pandas_chuncking.py
```

5) Instale a biblioteca duckDB, utilizando o Poetry, com o comando:
```python
poetry add duckdb
```

6) duckDB
```python
python etl_duckDB.py
```

---

## OUTPUT EXAMPLES

Todos os resultados finais são exportados nos formatos .csv e .parquet

Isso permite análises posteriores em ferramentas como Power BI, Metabase, Apache Superset ou puro Python, inclusive, o arquivo de saída será ordenado alfabeticamente por nome da estação:

```python
| Estação | Min | Média | Max|
| ---------- | ------ | ----- | ----- |
| Aabenraa| -99.80 | 3.4| 99.80 |
| Bariloche  | -57.40 | 8.2| 87.30 |
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

---

### PROJECT DEVELOPMENT

🔹Python 3.11+

🔹Pandas

🔹Pyarrow

🔹Polars

🔹DuckDB

---

## BENCHMARKING AND PERFORMANCE

### PYTHON
🔴 Python vanilla, sem utilização de ulimit ou cgroups.
A ETL quebrou por 6 vezes, consumindo os 16 GiB (15.3) de memória RAM do servidor e mais 4 de Swp

🟨 Python Vanilla com melhorias de performance:
A ETL rodou satisfatoriamente, demorando 726.20 segundos (pouco mais de 12 minutos) e consumindo apenas 1.5 GiB de memória RAM, no momento de pico de utilização do sistema.

🟨 Python com a utilização de técnica de chunking
A ETL rodou sofrida, não aguentou com chuncking de 100 milhões de linhas, quebrando duas vezes, rodando com chuncking de 50 milhões de linhas em 20 etapas, demorando 1436.41 segundos (quase 24 minutos) e consumindo 12.2 GiB de memória RAM, no momento de pico de utilização do sistema.

---

### PYTHON + PYARROW
🟨 Python com a utilização da biblioteca pyarrow apenas para gravar o parquet.
A ETL rodou satisfatoriamente, demorando 711.31 segundos (quase 12 minutos) e consumindo apenas 1.2 GiB de memória RAM, no momento de pico de utilização do sistema.

---

### PYTHON + PANDAS
🔴 Python + Pandas na leitura e no processamento
A ETL quebrou por 3 vezes, consumindo os 16 GiB (15.3) de memória RAM do servidor e mais 4 de Swp

🟨 Python + Pandas na leitura e no processamento + utilização de técnica de chunking
A ETL rodou satisfatoriamente, rodou com chuncking de 100 milhões de linhas, demorando 348.58 segundos (quase 6 minutos) e consumindo 10 GiB de memória RAM, no momento de pico de utilização do sistema.

---

### PYTHON + POLARS
🔴 Python + Polars na leitura e no processamento
A ETL quebrou por 3 vezes, em 5 segundos, consumindo os 16 GiB (15.3) de memória RAM do servidor e mais 4 de Swp

🔴 Python + Polars na leitura e no processamento + utilização de técnica de paralelismo
A ETL quebrou por 3 vezes, em 5 segundos, consumindo os 16 GiB (15.3) de memória RAM do servidor e mais 4 de Swp

---

### duckDB
🟢 Utilização do banco de dados duckDB 🥇 🏆
A ETL rodou lisa, demorando 12.38 segundos e consumindo apenas 1.76 GiB de memória RAM, no momento de pico de utilização do sistema.


## CONCLUSION

O benchmark conduzido com 1 bilhão de registros sintéticos de estações meteorológicas revela insights importantes sobre tempo de execução, uso de memória, tamanho dos arquivos e escalabilidade entre diferentes estratégias de processamento: Python puro, Pandas, abordagens com chunking, Polars e DuckDB.

### 1. ⏱️ Tempo de Execução Total

- DuckDB manteve seu desempenho superior, concluindo a ETL em apenas 12.38 segundos, mesmo com 1 bilhão de linhas.
- Pandas com chunking foi a abordagem tradicional mais eficiente, concluindo em 348.58 segundos (~6 minutos).
- Python puro com melhorias levou 726.20 segundos (~12 minutos), com performance estável.
- Python com chunking precisou de múltiplas etapas (20 chunks de 50 milhões), totalizando 1436.41 segundos (~24 minutos).
- As abordagens com Polars e Pandas sem chunking falharam devido ao estouro de memória, não completando a execução.

![total_time](image.png)

DuckDB novamente se destaca por sua eficiência vetorizada e engine SQL em memória. Chunking com Pandas ou Python é mais lento, mas confiável quando há limitação de RAM.

---

### 2. 💾 Pico de Uso de Memória RAM

- Python + PyArrow (escrevendo apenas Parquet com PyArrow) foi o mais econômico, com pico de 1.2 GiB.
- DuckDB também se manteve enxuto, consumindo apenas 1.76 GiB.
- Python + melhorias estabilizou em 1.5 GiB.
- Pandas com chunking usou 10 GiB, demonstrando bom controle.
- Python com chunking chegou a 12.2 GiB.
- Pandas, Polars e outras abordagens sem chunking estouraram os 16 GiB de RAM + 4 GiB de swap, travando a execução.

![total_memory](image-1.png)

DuckDB e PyArrow mantêm uso controlado de memória. Abordagens com chunking consomem mais, mas são seguras. Estratégias sem chunking falham com volumes bilionários.

---

### 3. 📦 Tamanho dos Arquivos (MiB)

Todos os arquivos CSV têm tamanho semelhante (~252 KB). DuckDB gerou o menor .csv e também o .parquet mais compacto, evidenciando compressão eficiente e escrita otimizada.

![total_file_size](image-2.png)

---

### Considerações de Arquitetura e Escalabilidade

- DuckDB permanece como a opção mais rápida, leve e escalável para análise local, com excelente performance mesmo com 1 bilhão de registros.
- Pandas + chunking se mostra um bom compromisso para ambientes com restrição de memória, sem comprometer robustez.
- Python puro com chunking é funcional, mas requer ajustes e monitoramento rigoroso de recursos.
- Polars ainda não sustentou o volume testado — falhou em todas as tentativas mesmo com paralelismo ativado.

### Recomendações Finais

Para pipelines de grande volume com baixa complexidade de transformação e foco em performance:

- ✅ DuckDB continua imbatível: rápido, econômico e com boa compressão.
- 🟡 Pandas com chunking é seguro, compatível e fácil de manter.
- 🟡 Python com chunking é defensável, mas exige mais trabalho manual.
- 🔴 Abordagens sem chunking não são recomendadas acima de 1 bilhão de linhas.
- ➡️ DuckDB é a escolha mais enxuta, tanto em CSV quanto em Parquet.
- ➡️ Parquet é amplamente superior ao CSV em termos de eficiência de armazenamento e preparo para análise.

Nem todo projeto de dados exige alta performance ou infraestrutura distribuída, mas saber escolher a abordagem certa para o contexto certo é o que separa scripts rápidos de pipelines confiáveis e sustentáveis.

Seus testes mostraram que cada tecnologia se comporta de forma distinta frente a três fatores críticos: volume de dados, disponibilidade de memória RAM e necessidade de escalabilidade.

Abaixo, a análise de cada abordagem sob esse prisma:

#### DuckDB: rápido, leve e pronto para escalar localmente

O DuckDB demonstrou ser o motor mais equilibrado para análises locais e pipelines de pequeno e médio porte.

Por que funciona tão bem?

- Ele processa os dados direto do disco, sem precisar carregá-los inteiramente na memória.
- Seu modelo de execução é colunar e vetorizado, o que significa que cada operação trabalha por blocos otimizados, aproveitando o cache do processador.
- Funciona bem mesmo com apenas um núcleo (monothread), o que o torna ideal para ambientes simples, como notebooks ou servidores de uso geral.

✅ Ideal para protótipos rápidos e ETLs locais com performance real, ambientes com pouca RAM ou CPU

############################### ⛔ CUIDADO ###############################

O DuckDB é uma ferramenta poderosa, mas como toda tecnologia, tem um conjunto de casos para os quais é ideal e outros onde não é a melhor escolha, conforme segue:

## ⚠️⚠️⚠️ DuckDB é excelente para prototipagem, análise local, cargas moderadas e dados tabulares em formato Parquet, CSV, Arrow, mas por que DuckDB não é geralmente indicado para produção?

###  Limitações do DuckDB em produção, explicadas por contexto

#### 1. Arquitetura embutida, não cliente-servidor

- DuckDB roda embutido no processo da aplicação (embedded database), isso quer dizer que não há um servidor separado para lidar com concorrência, autenticação, escalabilidade, etc., em produção, espera-se que o banco aceite múltiplas conexões, distribua carga e possa ser escalado horizontalmente.

👉 Consequência: DuckDB é monousuário por design, se múltiplas aplicações ou usuários tentarem acessar o mesmo banco simultaneamente, você corre risco de corrupção ou race conditions.

---

#### 2. Não suporta múltiplas sessões concorrentes de escrita

- Em bancos como PostgreSQL, múltiplos processos podem ler e escrever simultaneamente, com controle de transações.
- O DuckDB só permite uma escrita por vez e ainda bloqueia arquivos `.duckdb` durante a operação.

👉 Consequência: Impraticável em ambientes multiusuário, com alta taxa de gravação ou uso concorrente, como APIs, microsserviços e sistemas OLTP.

---

### 3. Não é tolerante a falhas por padrão

- Bancos de produção geralmente contam com replicação, backups automáticos, failover, logs de transação para recovery e DuckDB não implementa esses recursos nativamente.

👉 Consequência: Se seu processo for interrompido abruptamente (por crash, falha de disco ou interrupção de energia), você pode perder o banco ou corromper o arquivo.

---

### 4. Não escala horizontalmente

- DuckDB não possui arquitetura distribuída, ele não foi feito para escalar em múltiplas máquinas nem processar grandes volumes em cluster (como Spark, Dask, BigQuery, etc).

👉 Consequência: Para dados de alta volumetria (> bilhões de linhas), ou para times que precisam escalar a leitura e escrita em paralelo, o DuckDB não acompanha.

---

### 5. Foco principal é análise local — OLAP, não OLTP

- DuckDB é orientado a consultas analíticas complexas (OLAP), não a sistemas transacionais (OLTP), ele brilha ao fazer `SELECT station, AVG(temp)` em 100 milhões de linha, mas não serve bem para registrar pedidos de e-commerce ou gerenciar usuários de um app em tempo real.

👉 Consequência: Não use DuckDB para aplicações com alta taxa de inserção, atualização ou leitura em tempo real.

---

### Use DuckDB com confiança para:

![alt text](image-5.png)

Quando se trata de uso do DuckDB como fonte de dados para dashboards — como Power BI, Metabase, Superset ou até Streamlit — a análise muda bastante, e a resposta é "depende do uso, mas com ressalvas importantes".

---

## ✅ DuckDB é uma excelente FONTE para dashboards... se usado da maneira certa

### 🟢 Vantagens

1. Leitura muito rápida:
- Consultas analíticas (`SELECT`, `GROUP BY`, `JOIN`) são extremamente otimizadas em DuckDB, principalmente em formatos como Parquet e CSV.
- Ideal para painéis que consultam dados prontos, agregados.
2. Compatível com ODBC/ODBC-like connectors:
- DuckDB oferece conectores (em evolução) para se integrar com BI tools, especialmente via drivers ODBC.
- Já existem métodos para conectar o Power BI via ODBC e o Metabase via JDBC/ODBC (com algum esforço).
3. Formato leve e portátil:
- O `.duckdb` é um único arquivo. Você pode gerar e compartilhar com o dashboard, sem precisar de um servidor de banco.
4. Integração com Parquet e CSV:
- DuckDB pode ser usado para consultar diretamente arquivos Parquet/CSV como se fossem tabelas — útil quando seu dashboard é alimentado por arquivos externos.

---

## ⚠️ Limitações e cuidados

### 1. Não é um servidor de banco — logo, sem pooling, DuckDB não escuta conexões TCP como PostgreSQL/MySQL, cada dashboard teria que abrir a base localmente, o que não escala para múltiplos usuários. Uma solução parcial seria o uso do DuckDB em cenários de *data refresh batch*, ou seja, você gera um CSV ou Parquet com DuckDB e usa esse arquivo como fonte no Power BI ou Metabase, que apontam para ele.

### 2. Sem controle de concorrência

- Se dois dashboards tentarem acessar simultaneamente o mesmo arquivo `.duckdb`, pode haver corrupção ou travamento, a recomendação é que evite `.duckdb` como fonte compartilhada de leitura concorrente em dashboards, prefira extrair e gerar `.parquet` ou `.csv` de leitura rápida.


## ✅ Recomendações práticas
![duckDB](image-4.png)

---

## 💡 Conclusão

DuckDB é extremamente eficaz para gerar datasets analíticos e alimentadores de dashboard, mas não é ideal como fonte de dados dinâmica e concorrente.

✅ Use DuckDB para processar e entregar dados prontos para visualização.

⚠️ Evite usá-lo como backend direto em dashboards multiusuário em produção.

💡 Melhor estratégia: DuckDB → Parquet → Dashboard.


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

🚀 André Matiello C. Caramanti - [matiello.andre@hotmail.com](mailto:matiello.andre@hotmail.com)

---

## LICENSE

[MIT License](https://andrematiello.notion.site/mit-license)
