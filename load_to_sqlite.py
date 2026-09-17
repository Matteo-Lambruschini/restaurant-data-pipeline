import pandas as pd
import sqlite3

# Legge il CSV pulito
sales = pd.read_csv("processed/sales_clean.csv")

# Crea/apre il database SQLite
connection = sqlite3.connect("database/restaurant.db")

# Carica i dati in una tabella chiamata sales
sales.to_sql("sales", connection, if_exists="replace", index=False)

# Chiude la connessione
connection.close()

print("Dati caricati correttamente nel database SQLite.")