import os

import pandas as pd
import matplotlib.pyplot as plt

# Folder where charts are saved
os.makedirs("images", exist_ok=True)

# Load datasets
customers = pd.read_csv("data/customers.csv")
consumption = pd.read_csv("data/consumption_records.csv")

# Combine customer and consumption datasets
df = pd.merge(
    consumption,
    customers,
    on="customer_id",
    how="inner"
)

print("Combined Dataset:")
print(df.head())

print("\nDataset Shape:", df.shape)

# Statistical summary
print("\nStatistical Summary:")
print(df[[
    "units_consumed",
    "rate_per_unit",
    "total_bill"
]].describe())

# Monthly consumption analysis
monthly_data = df.groupby(
    "billing_month"
)["units_consumed"].sum()

print("\nMonthly Consumption:")
print(monthly_data)

# Average consumption by connection type
connection_analysis = df.groupby(
    "connection_type"
)["units_consumed"].mean()

print("\nAverage Consumption by Connection Type:")
print(connection_analysis)

# Payment status analysis
print("\nPayment Status:")
print(df["payment_status"].value_counts())


# --------------------------------------------
# DATA VISUALIZATION
# --------------------------------------------

# 1. Monthly Consumption Trend

plt.figure(figsize=(12, 6))

monthly_data.plot(
    kind="line",
    marker="o",
    linewidth=2
)

plt.title("Monthly Electricity Consumption - 2025")
plt.xlabel("Billing Month")
plt.ylabel("Units Consumed")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig("images/monthly_consumption.png")
plt.show()


# 2. Consumption by Connection Type

plt.figure(figsize=(8, 5))

connection_analysis.plot(
    kind="bar"
)

plt.title("Average Consumption by Connection Type")
plt.xlabel("Connection Type")
plt.ylabel("Average Units")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("images/connection_type_analysis.png")
plt.show()


# 3. Payment Status Distribution

payment_counts = df["payment_status"].value_counts()

plt.figure(figsize=(7, 7))

plt.pie(
    payment_counts,
    labels=payment_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Electricity Bill Payment Status")
plt.tight_layout()

plt.savefig("images/payment_status.png")
plt.show()

print("\nAll charts generated successfully!")