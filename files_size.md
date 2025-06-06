### com 100 milhões de registros, em 8883 stations

```bash
du -ah data/ | grep -v '/$' | sort -hr
```
1.5G    data/weather_stations.csv
808K    data/model.csv


252K    data/measurements_python.csv
116K    data/measurements_python.parquet

252K    data/measurements_python_chunk.csv
116K    data/measurements_python_chunk.parquet

252K    data/measurements_pandas.csv
116K    data/measurements_pandas.parquet

252K    data/measurements_pandas_chunk.csv
116K    data/measurements_pandas_chunk.parquet

236K    data/measurements_duckDB.csv
100K    data/measurements_duckDB.parquet



52K     data/files_sizes_chart.png
