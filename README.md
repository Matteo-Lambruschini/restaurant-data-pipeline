# Restaurant Operations Data Pipeline

[![Pipeline Tests](https://github.com/Matteo-Lambruschini/restaurant-data-pipeline/actions/workflows/tests.yml/badge.svg)](https://github.com/Matteo-Lambruschini/restaurant-data-pipeline/actions/workflows/tests.yml)

An end-to-end data engineering project that simulates a restaurant operations pipeline using Python, Pandas, SQLite and SQL.

The project extracts raw sales and product data from CSV files, validates and transforms the data, calculates business metrics, creates analytical tables, and loads the results into a SQLite database for SQL analysis.

The dataset is synthetic and was generated specifically for this project.

---

## Project Overview

The pipeline processes:

- 1,500 synthetic sales records
- 10 restaurant products
- product categories
- selling prices
- unit food costs
- sales quantities
- transaction dates

The pipeline calculates operational KPIs including:

- Revenue
- Food cost
- Gross profit
- Food cost percentage
- Gross margin percentage
- Daily sales performance
- Product performance

---

## Data Pipeline

```text
Raw CSV files
      |
      v
Extract with Python / Pandas
      |
      v
Data validation
      |
      v
Data cleaning
      |
      v
Merge sales + product data
      |
      v
Calculate business metrics
      |
      v
Create analytical tables
      |
      v
Save processed data
      |
      v
Load into SQLite
      |
      v
      |
      v
SQL analysis
```
## Technologies

- Python
- Pandas
- SQL
- SQLite
- Git
- GitHub
- pytest
- GitHub Actions
- Docker
## Architecture Diagram

```mermaid
flowchart LR
    A[products.csv] --> C[Python / Pandas ETL]
    B[sales.csv] --> C

    C --> D[Data Validation]
    D --> E[Merge on product_id]
    E --> F[Business Metrics]

    F --> G[sales_enriched.csv]
    F --> H[(SQLite)]

    H --> I[sales_raw]
    H --> J[products]
    H --> K[sales]
    H --> L[daily_kpis]
    H --> M[product_performance]

    K --> N[SQL Analysis]
    L --> N
    M --> N
```
## Example Results

A successful pipeline run processes 1,500 synthetic sales records and produces the following results:

| Metric | Result |
|---|---:|
| Sales records processed | 1,500 |
| Total revenue | 72,930.00 |
| Total gross profit | 52,746.60 |
| Daily KPI records | 90 |
| Product performance records | 10 |

These results are generated from synthetic restaurant sales data created specifically for this project.
## Key SQL Insights

SQL analysis of the synthetic dataset highlights several operational patterns:

- **Pho** generated the highest product revenue: **14,075**
- **Pho** was also the highest-volume product with **563 units sold**
- The **Main** category generated the highest category revenue: **42,740**
- July produced the highest monthly revenue: **26,838**
- Monday generated the highest revenue by day of week: **12,530**
- Total gross profit across the dataset was **52,746.60**

### Top Products by Revenue

| Product | Units Sold | Revenue | Gross Profit |
|---|---:|---:|---:|
| Pho | 563 | 14,075 | 10,021.40 |
| Bo Bun | 406 | 11,368 | 7,957.60 |
| Fried Rice | 385 | 8,855 | 6,352.50 |
| Banh Mi | 469 | 8,442 | 6,097.00 |
| Dumplings | 453 | 7,248 | 5,073.60 |

### Monthly Revenue

| Month | Revenue | Gross Profit |
|---|---:|---:|
| 2026-06 | 24,141 | 17,405.50 |
| 2026-07 | 26,838 | 19,426.80 |
| 2026-08 | 21,951 | 15,914.30 |

These insights are based on synthetic data generated with a fixed random seed to keep the project reproducible.

## Automated Testing

The project includes automated tests built with `pytest`.

The test suite validates:

- successful end-to-end pipeline execution
- expected columns in the processed dataset
- revenue calculations
- gross profit calculations
- positive sales quantities
- successful product matching

Run the tests with:

```bash
python -m pytest
## Docker

The project can be built and executed inside a Docker container, providing a reproducible environment independent of the local Python installation.

### Build the Docker image

```bash
docker build -t restaurant-data-pipeline .
```

### Run the pipeline

```bash
docker run --rm restaurant-data-pipeline
```

A successful container execution produces:

```text
Pipeline completed successfully.
Sales processed: 1500
Total revenue: 72930.00
Total gross profit: 52746.60
Daily KPI records created: 90
Product performance records created: 10
```

The Docker image installs the project dependencies from `requirements.txt` and executes `pipeline.py` automatically.
## What I Learned

Building this project helped me develop practical experience with the core concepts of a data engineering workflow.

Key takeaways include:

- designing an end-to-end ETL pipeline
- working with multiple CSV data sources
- validating data before processing
- joining relational datasets using Pandas
- calculating operational and financial KPIs
- creating analytical tables for reporting
- loading transformed data into SQLite
- writing SQL queries for business analysis
- implementing structured logging and error handling
- writing automated tests with pytest
- using Git and GitHub for version control
- configuring continuous integration with GitHub Actions
- containerizing a Python data pipeline with Docker

The project also helped me understand the importance of reproducibility, data quality and automated validation in a data pipeline.


## Future Improvements

Possible future improvements include:

- moving from SQLite to PostgreSQL
- separating the pipeline into reusable Python modules
- adding configuration files and environment variables
- introducing more advanced data quality checks
- scheduling the pipeline automatically
- creating a dashboard for restaurant KPIs
- processing larger datasets
- adding cloud storage or cloud database integration
- expanding the CI pipeline with additional quality checks