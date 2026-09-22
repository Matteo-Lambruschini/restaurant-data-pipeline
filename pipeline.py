import pandas as pd
import sqlite3
from pathlib import Path
import logging
# -----------------------------
# LOGGING
# -----------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# -----------------------------
# PATHS
# -----------------------------

DATA_DIR = Path("data")
PROCESSED_DIR = Path("processed")
DATABASE_DIR = Path("database")

PROCESSED_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)


# -----------------------------
# EXTRACT
# -----------------------------
logger.info("Pipeline started.")
logger.info("Loading source CSV files.")

try:
    sales = pd.read_csv(DATA_DIR / "sales.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")

    logger.info(
        "Loaded %s sales records and %s products.",
        len(sales),
        len(products)
    )

except Exception:
    logger.exception("Failed to load source CSV files.")
    raise

# -----------------------------
# DATA VALIDATION
# -----------------------------

required_sales_columns = {
    "sale_id",
    "date",
    "product_id",
    "quantity"
}

required_product_columns = {
    "product_id",
    "product_name",
    "category",
    "unit_price",
    "unit_cost"
}

missing_sales_columns = required_sales_columns - set(sales.columns)
missing_product_columns = required_product_columns - set(products.columns)

if missing_sales_columns:
    raise ValueError(
        f"Missing columns in sales.csv: {missing_sales_columns}"
    )

if missing_product_columns:
    raise ValueError(
        f"Missing columns in products.csv: {missing_product_columns}"
    )


# -----------------------------
# TRANSFORM
# -----------------------------

sales["date"] = pd.to_datetime(sales["date"])
sales["quantity"] = pd.to_numeric(sales["quantity"])

products["unit_price"] = pd.to_numeric(products["unit_price"])
products["unit_cost"] = pd.to_numeric(products["unit_cost"])

sales = sales.drop_duplicates()
products = products.drop_duplicates()

if (sales["quantity"] <= 0).any():
    raise ValueError("Quantity must always be greater than zero.")

if products["product_id"].duplicated().any():
    raise ValueError("Duplicate product_id found in products.csv.")


# -----------------------------
# MERGE SALES + PRODUCTS
# -----------------------------

sales_enriched = sales.merge(
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
    
)
logger.info(
    "Sales and product data merged successfully."
)

if sales_enriched["product_name"].isna().any():
    raise ValueError(
        "Some product IDs in sales.csv do not exist in products.csv."
    )


# -----------------------------
# BUSINESS METRICS
# -----------------------------

sales_enriched["revenue"] = (
    sales_enriched["quantity"]
    * sales_enriched["unit_price"]
)

sales_enriched["food_cost"] = (
    sales_enriched["quantity"]
    * sales_enriched["unit_cost"]
)

sales_enriched["gross_profit"] = (
    sales_enriched["revenue"]
    - sales_enriched["food_cost"]
)

sales_enriched["gross_margin_pct"] = (
    sales_enriched["gross_profit"]
    / sales_enriched["revenue"]
    * 100
).round(2)


# -----------------------------
# ANALYTICAL TABLES
# -----------------------------

daily_kpis = (
    sales_enriched
    .groupby("date", as_index=False)
    .agg(
        sales_records=("sale_id", "count"),
        units_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        food_cost=("food_cost", "sum"),
        gross_profit=("gross_profit", "sum")
    )
)

daily_kpis["food_cost_pct"] = (
    daily_kpis["food_cost"]
    / daily_kpis["revenue"]
    * 100
).round(2)

daily_kpis["gross_margin_pct"] = (
    daily_kpis["gross_profit"]
    / daily_kpis["revenue"]
    * 100
).round(2)


product_performance = (
    sales_enriched
    .groupby(
        [
            "product_id",
            "product_name",
            "category"
        ],
        as_index=False
    )
    .agg(
        units_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        food_cost=("food_cost", "sum"),
        gross_profit=("gross_profit", "sum")
    )
)

product_performance["food_cost_pct"] = (
    product_performance["food_cost"]
    / product_performance["revenue"]
    * 100
).round(2)

product_performance["gross_margin_pct"] = (
    product_performance["gross_profit"]
    / product_performance["revenue"]
    * 100
).round(2)

logger.info(
    "Analytical tables created: %s daily KPI records and %s product records.",
    len(daily_kpis),
    len(product_performance)
)

# -----------------------------
# SAVE PROCESSED DATA
# -----------------------------

sales_enriched.to_csv(
    PROCESSED_DIR / "sales_enriched.csv",
    index=False
)


# -----------------------------
# LOAD INTO SQLITE
# -----------------------------
try:
    with sqlite3.connect(
        DATABASE_DIR / "restaurant.db"
    ) as connection:

        sales.to_sql(
            "sales_raw",
            connection,
            if_exists="replace",
            index=False
        )

        products.to_sql(
            "products",
            connection,
            if_exists="replace",
            index=False
        )

        sales_enriched.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False
        )

        daily_kpis.to_sql(
            "daily_kpis",
            connection,
            if_exists="replace",
            index=False
        )

        product_performance.to_sql(
            "product_performance",
            connection,
            if_exists="replace",
            index=False
        )

    logger.info("SQLite database updated successfully.")

except Exception:
    logger.exception("Failed to update SQLite database.")
    raise
logger.info("Pipeline completed successfully.")
# -----------------------------
# PIPELINE SUMMARY
# -----------------------------

print("Pipeline completed successfully.")
print(f"Sales processed: {len(sales_enriched)}")
print(
    f"Total revenue: "
    f"{sales_enriched['revenue'].sum():.2f}"
)
print(
    f"Total gross profit: "
    f"{sales_enriched['gross_profit'].sum():.2f}"
)
print(f"Daily KPI records created: {len(daily_kpis)}")
print(
    f"Product performance records created: "
    f"{len(product_performance)}"
)