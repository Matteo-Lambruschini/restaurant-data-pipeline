import subprocess
import sys

import pandas as pd


def test_pipeline_runs_successfully():
    result = subprocess.run(
        [sys.executable, "pipeline.py"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0


def test_sales_enriched_contains_expected_columns():
    sales = pd.read_csv("processed/sales_enriched.csv")

    expected_columns = {
        "sale_id",
        "date",
        "product_id",
        "quantity",
        "product_name",
        "category",
        "unit_price",
        "unit_cost",
        "revenue",
        "food_cost",
        "gross_profit",
        "gross_margin_pct"
    }

    assert expected_columns.issubset(sales.columns)


def test_revenue_calculation():
    sales = pd.read_csv("processed/sales_enriched.csv")

    expected_revenue = sales["quantity"] * sales["unit_price"]

    assert (sales["revenue"] == expected_revenue).all()


def test_gross_profit_calculation():
    sales = pd.read_csv("processed/sales_enriched.csv")

    expected_profit = sales["revenue"] - sales["food_cost"]

    assert (sales["gross_profit"] == expected_profit).all()


def test_no_invalid_quantities():
    sales = pd.read_csv("processed/sales_enriched.csv")

    assert (sales["quantity"] > 0).all()


def test_all_products_are_matched():
    sales = pd.read_csv("processed/sales_enriched.csv")

    assert sales["product_name"].notna().all()