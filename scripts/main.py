
import pandas as pd
import numpy as np
import os

# Project initialization
print("Electricity Consumption & Billing Analytics")
print("--------------------------------------------")

# Generate sample customer data
np.random.seed(42)

customer_ids = range(1001, 1101)

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "customer_name": [f"Customer_{i}" for i in customer_ids],
    "city": np.random.choice(
        ["Hyderabad", "Bengaluru", "Chennai", "Pune"],
        100
    ),
    "connection_type": np.random.choice(
        ["Residential", "Commercial", "Industrial"],
        100
    )
})

# Display the first five records
print("\nCustomer Dataset:")
print(customers.head())

# Dataset information
print("\nDataset Shape:", customers.shape)

# Save dataset
os.makedirs("data", exist_ok=True)
customers.to_csv("data/customers.csv", index=False)

print("\nCustomer dataset generated successfully!")


# --------------------------------------------
# Generate Monthly Electricity Consumption Data
# --------------------------------------------

months = pd.date_range(
    start="2025-01-01",
    end="2025-12-01",
    freq="MS"
)

consumption_records = []

for customer_id in customer_ids:
    for month in months:

        units = np.random.randint(80, 601)

        rate_per_unit = np.random.choice(
            [4.5, 5.0, 5.5, 6.0, 7.0]
        )

        total_bill = round(units * rate_per_unit, 2)

        payment_status = np.random.choice(
            ["Paid", "Pending", "Overdue"],
            p=[0.75, 0.15, 0.10]
        )

        consumption_records.append({
            "customer_id": customer_id,
            "billing_month": month.strftime("%Y-%m"),
            "units_consumed": units,
            "rate_per_unit": rate_per_unit,
            "total_bill": total_bill,
            "payment_status": payment_status
        })

consumption_df = pd.DataFrame(consumption_records)

consumption_df.to_csv(
    "data/consumption_records.csv",
    index=False
)

print("\nConsumption Dataset:")
print(consumption_df.head())

print("\nConsumption Dataset Shape:", consumption_df.shape)

print("\nConsumption records generated successfully!")




# --------------------------------------------
# Data Quality Checks
# --------------------------------------------

print("\n========== DATA QUALITY CHECKS ==========")

# Check missing values
print("\nMissing Values:")
print(consumption_df.isnull().sum())

# Check duplicate records
print("\nDuplicate Records:")
print(consumption_df.duplicated().sum())

# Check total electricity units consumed
print("\nTotal Units Consumed:")
print(consumption_df["units_consumed"].sum())

# Check total revenue generated
print("\nTotal Billing Amount:")
print(consumption_df["total_bill"].sum())

# Check payment status distribution
print("\nPayment Status Distribution:")
print(consumption_df["payment_status"].value_counts())

print("\nData quality checks completed!")
