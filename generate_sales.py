import csv
import random
from datetime import date, timedelta

random.seed(42)

products = [
    "P001",
    "P002",
    "P003",
    "P004",
    "P005",
    "P006",
    "P007",
    "P008",
    "P009",
    "P010",
]

start_date = date(2026, 6, 1)

rows = []

for sale_id in range(1, 1501):
    random_day = start_date + timedelta(days=random.randint(0, 89))
    product_id = random.choice(products)
    quantity = random.randint(1, 5)

    rows.append([
        f"S{sale_id:05d}",
        random_day.isoformat(),
        product_id,
        quantity
    ])

with open("data/sales.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "sale_id",
        "date",
        "product_id",
        "quantity"
    ])

    writer.writerows(rows)

print("1500 synthetic sales generated successfully.")