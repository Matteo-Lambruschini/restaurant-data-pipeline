import pandas as pd

# Legge il file CSV
sales = pd.read_csv("data/sales.csv")

# Converte la colonna date in un vero formato data
sales["date"] = pd.to_datetime(sales["date"])

# Elimina eventuali righe duplicate
sales = sales.drop_duplicates()

# Calcola il fatturato di ogni riga
sales["revenue"] = sales["quantity"] * sales["price"]

# Mostra il risultato
print(sales)# Salva i dati puliti in un nuovo CSV
sales.to_csv("processed/sales_clean.csv", index=False)

print("\nFile pulito salvato in processed/sales_clean.csv")