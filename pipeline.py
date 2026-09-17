import pandas as pd
import sqlite3

# 1. EXTRACT - legge i dati grezzi
sales = pd.read_csv("data/sales.csv")

# 2. TRANSFORM - pulizia e trasformazione
sales["date"] = pd.to_datetime(sales["date"])
sales = sales.drop_duplicates()
sales["revenue"] = sales["quantity"] * sales["price"]

# 3. Salva una copia pulita
sales.to_csv("processed/sales_clean.csv", index=False)

# 4. LOAD - carica i dati nel database SQLite
connection = sqlite3.connect("database/restaurant.db")

sales.to_sql(
    "sales",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("Pipeline completata con successo.")