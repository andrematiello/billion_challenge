![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-FINAL-lightgrey)

<p align="right">
  <a href="README.md">
    <img src="assets/br.png" width="18" alt="Versão em português" title="Versão em português"> Português
  </a>
</p>

> A Data Engineering project focused on **local ETL, benchmarking, interactive data visualization, and strategic use of DuckDB**, designed as a realistic case study for a professional portfolio.

# ONE BILLION ROWS CHALLENGE – PYTHON EDITION 🐍

## TABLE OF CONTENTS

- [ONE BILLION ROWS CHALLENGE – PYTHON EDITION 🐍](#one-billion-rows-challenge--python-edition-)
  - [TABLE OF CONTENTS](#table-of-contents)
  - [ABOUT THE PROJECT](#about-the-project)
  - [INSPIRATION](#inspiration)
  - [BUSINESS PROBLEM](#business-problem)
  - [PROPOSED CHALLENGE](#proposed-challenge)
    - [GENERAL OPERATION](#general-operation)
    - [OUTPUT FILE](#output-file)
    - [INTERESTING TECHNICAL HIGHLIGHTS](#interesting-technical-highlights)

## ABOUT THE PROJECT

✨ This project is a hands-on journey in data engineering that processes 1 billion records, extracting aggregated temperature statistics with high performance and scalability in Python.
It was developed as an advanced applied engineering exercise, demonstrating how to efficiently process a massive 1-billion-row CSV file (~14 GB) using Python — focused on simple computations like aggregations (min, mean, max) and sorting, while making efficient use of system resources.

As a visual and analytical complement, the project includes an interactive Streamlit dashboard, built for portfolio purposes. Although not intended for production use, the dashboard allows users to visually explore temperature statistics by weather station, featuring a dynamic data table, bar charts for average/min/max temperatures, and a scatter plot for thermal extremes — all rendered responsively, running locally without the need for cloud infrastructure.

This project serves as a realistic case study for data engineers, data scientists, and developers interested in large-scale file processing, chunking strategies, benchmarking Python libraries, and using modern analytical engines like DuckDB. While the One Billion Row Challenge is not a business dataset, it simulates real-world scenarios faced by companies dealing with high-volume transactional, sensor, or operational data.

The entire challenge was executed on a local homelab environment, powered by a Dell Optiplex 7020, running Ubuntu Server, with an Intel Core i5-14500T processor and 16 GiB of RAM.

## INSPIRATION

This challenge was inspired by the original [1BRC](https://github.com/gunnarmorling/1brc) project proposed by Gunnar Morling in Java. Later, it was adapted to Python by Luciano Vasconcelos in the repository [One-Billion-Row-Challenge-Python](https://github.com/lvgalvao/One-Billion-Row-Challenge-Python), as part of a workshop within the educational context of Jornada de Dados (2024).

---

## BUSINESS PROBLEM

Below are the main business challenges addressed by this case:

🔹 **Processing Large Volumes of Raw Data**

Many companies regularly deal with data files in formats like `.csv`, `.json`, or `.parquet` containing millions or even billions of rows — especially in sectors like retail, energy, climatology, IoT, and telecom. This project demonstrates how to read, clean, and aggregate massive files without having to load everything into memory or rely on expensive compute clusters.

🔹 **Efficient Aggregation of Operational Statistics**

Operational data analysis often requires calculating average, maximum, and minimum values. While conceptually simple, these operations become challenging at scale across multiple keys. This case presents optimized aggregation strategies using tools like DuckDB and chunked Pandas, simulating large-scale calculation of operational KPIs.

🔹 **Performance and Efficient Resource Utilization**

Data projects don’t always run in high-performance environments. Teams frequently face constraints in RAM, CPU, or disk I/O, especially on local machines, intermediate servers, or scheduled jobs. This case explores low-memory strategies, chunking, and columnar engines (like DuckDB) that enable high performance on everyday hardware.

🔹 **Validating Analytical Architectures for Batch Processing**

Before moving to the cloud, teams often need to validate if a given architecture (e.g., local processing + `.parquet` export) meets SLAs for time and cost. This project offers a complete and reproducible sandbox to test pipelines, benchmark file formats, and compare reading and aggregation approaches.

🔹 **Training and Upskilling Data Engineering Teams**

Mature data teams require practical and challenging real-world cases — beyond small notebooks or toy datasets. This project serves as an advanced case study to train data engineers, analysts, and data scientists in performance optimization, data architecture, and clean coding practices.

🔹 **Exporting Data for BI and Visualizations**

A common final step is to convert raw files into efficient formats for BI dashboards (like clean `.csv` or optimized `.parquet`). This project generates standardized and sorted outputs ready for ingestion into Power BI, Metabase, Superset, or cloud solutions, ensuring fast and lightweight consumption.

🔹 **Interactive Visualization with Local Dashboards**

Beyond efficient data processing, the project includes a fully interactive **Streamlit** dashboard that loads the processed data and provides dynamic charts. Users can explore aggregate metrics per weather station through bar charts (min, avg, max temperatures) and a scatter plot for thermal extremes — all rendered instantly, without external servers. This local-first approach facilitates exploratory data analysis and demonstrates how to deliver analytical value even on simple infrastructure.

---

## PROPOSED CHALLENGE

The core challenge of this project is to design a robust, efficient, and scalable Python solution capable of processing **1 billion temperature records**, simulating a real-world high-volume data engineering scenario. The main goals include extracting aggregated statistics per weather station, with a strong emphasis on performance, resource-conscious computing, and final analytical delivery in multiple formats. Key technical objectives are:

🔹 Efficiently read an input file containing 1 billion rows, simulating massive meteorological sensor data, even under constrained system resources.

🔹 Compute aggregated statistics per station, including Minimum Temperature, Maximum Temperature, and Average Temperature (with 2-decimal precision).

🔹 Alphabetically sort the results by station name, ensuring legibility and analytical structure in the output files.

🔹 Export final results in both `.csv` (universally compatible) and `.parquet` (high-performance, efficient compression) formats.

🔹 Compare different technical approaches, evaluating Execution Time, RAM Usage, and Output File Sizes — always with scalability and stability in mind.

These comparisons cover implementations from raw Python to DuckDB, including Pandas, manual chunking, and PyArrow, highlighting trade-offs, expected behaviors, and performance patterns in large-scale analytical pipelines.

---

### GENERAL OPERATION

The synthetic dataset generation with 1 billion rows was carefully designed to simulate realistic conditions of massive ingestion of sensor data, applying efficient write strategies and performance control. Below is the detailed operational flow:

🔹 **Input Argument Validation**
The main script (`create_measurements.py`) validates whether a numeric argument was passed representing the desired number of rows (e.g., `1_000_000_000`), ensuring flexibility and scalability.

🔹 **Retrieving Weather Station Names**
Station names are extracted from the `model.csv` file, which contains a list of real locations. Lines starting with `#` are ignored, and duplicates are automatically removed to ensure a clean set of valid stations.

🔹 **Final File Size Estimation**
Before generation starts, the system estimates the required disk space based on the number of stations, average characters per line, and data format — helping in infrastructure planning.

🔹 **Synthetic Generation of Random Temperatures**
Each row is assigned a floating-point temperature between -99.9°C and 99.9°C, simulating sensor readings. Station names are randomly selected with `random.choices()` using uniform distribution.

🔹 **Writing the `data/weather_stations.csv` File**
Measurements are written in batches directly to disk in semicolon-delimited format (`;`). Each line contains the station name and the temperature, ensuring consistency and portability.

🔹 **Batch Processing (100 Million per Chunk)**
Data is written in chunks of 100,000,000 rows to reduce I/O pressure and drastically improve write performance. A `tqdm` progress bar provides real-time feedback.

🔹 **Monitoring and Performance Logging**
At the end of execution, the script prints total time elapsed and the actual file size, validating the initial estimate and allowing benchmarking of the generation process.

---

### OUTPUT FILE

The file `data/weather_stations.csv` was generated in 6 minutes and 5 seconds, totaling 14.8 GiB with 1 billion rows. Each record includes a `string` station name and a `float` temperature with two decimal precision.

```text
<station_name>;<temperature>
```

```text
Stockholm;-5.32
São Paulo;25.85
Cape Town;19.01
```
---

### INTERESTING TECHNICAL HIGHLIGHTS

Throughout this project, several best practices in data engineering were applied, combining performance, clarity, and adaptability. From data generation to reading and processing strategies, each step reflects real-world challenges faced by data engineers working under resource constraints.

During data generation, the script avoids the traditional use of round(), instead opting for string interpolation (f"{x:.1f}") to control decimal precision more efficiently. Station names are selected using random.choices() to simulate geographic uniformity, and batch writing drastically reduces I/O time — an essential optimization when dealing with massive files.

Before any data is generated, the script provides an accurate estimate of expected disk usage, aiding infrastructure planning. Throughout execution, informative messages and a progress bar keep the user well informed, and robust validations are available via command-line help.

In the processing stage, multiple approaches were implemented to compare performance, scalability, and memory usage — from real-time line-by-line reading with in-memory aggregation (ideal for low-RAM machines), to manual chunking and Pandas-based strategies for greater control in iterative pipelines.

The project also integrates DuckDB, a modern embedded columnar engine capable of executing SQL queries directly on .csv and .parquet files, delivering near-distributed-system performance without the complexity of managing a cluster.

This combination of techniques offers a valuable case study for those looking to learn or teach real-world data engineering with a focus on performance, sound architectural choices, and technical mastery of the modern Python stack.

---
