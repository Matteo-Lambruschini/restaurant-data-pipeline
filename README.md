# Restaurant Operations Data Pipeline

A small end-to-end data engineering project built with Python, Pandas, SQLite and SQL.

The project simulates a restaurant sales data pipeline that extracts raw sales data from CSV files, cleans and transforms the data, stores the processed data in SQLite, and enables analysis using SQL queries.

## Pipeline

Raw CSV data
→ Extract with Python/Pandas
→ Clean and transform data
→ Calculate revenue
→ Save processed CSV
→ Load into SQLite
→ Query data with SQL

## Technologies

- Python
- Pandas
- SQLite
- SQL
- Git

## Project Structure

```text
restaurant-data-pipeline/
├── data/
│   └── sales.csv
├── processed/
│   └── sales_clean.csv
├── database/
│   └── restaurant.db
├── sql/
│   └── queries.sql
├── pipeline.py
├── read_csv.py
├── transform_sales.py
├── load_to_sqlite.py
├── requirements.txt
└── README.md