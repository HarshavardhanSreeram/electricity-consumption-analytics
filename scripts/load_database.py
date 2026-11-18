
import pandas as pd
import sqlite3

# Load CSV files
customers = pd.read_csv("data/customers.csv")
consumption = pd.read_csv("data/consumption_records.csv")

# Create SQLite database
connection = sqlite3.connect("electricity_analytics.db")

# Load data into SQL tables
customers.to_sql(
    "customers",
    connection,
    if_exists="replace",
    index=False
)

consumption.to_sql(
    "consumption",
    connection,
    if_exists="replace",
    index=False
)

print("Database created successfully!")

# Verify customer table
print("\nCustomer Table:")
print(pd.read_sql("SELECT * FROM customers LIMIT 5", connection))

# Verify consumption table
print("\nConsumption Table:")
print(pd.read_sql("SELECT * FROM consumption LIMIT 5", connection))

connection.close()
