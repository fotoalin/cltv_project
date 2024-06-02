import numpy as np
import pandas as pd

# Parameters
num_customers = 100000
min_orders_per_customer = 1
max_orders_per_customer = 15
start_date = pd.Timestamp("2015-01-01")
end_date = pd.Timestamp("2024-01-01")

# Generate customer_ids
customer_ids = np.arange(1, num_customers + 1)

# Generate random order data for each customer
data = []
np.random.seed(0)  # For reproducibility
for customer_id in customer_ids:
    num_orders = np.random.randint(min_orders_per_customer, max_orders_per_customer + 1)
    order_dates = pd.to_datetime(
        np.random.uniform(start_date.value, end_date.value, num_orders).astype(
            "datetime64[ns]"
        )
    )
    order_dates = np.sort(order_dates)  # Ensure the dates are in ascending order
    revenues = np.random.uniform(4, 150, num_orders)  # Random revenue between 4 and 150
    for order_id, (order_date, revenue) in enumerate(
        zip(order_dates, revenues), start=1
    ):
        data.append([order_id, customer_id, order_date, revenue])

# Create DataFrame
df = pd.DataFrame(data, columns=["order_id", "customer_id", "order_date", "revenue"])

# Save to an Excel file
file_path = (
    "/Users/webdevmac/Python Programming/CLTV_PROJECT/cltv_project/customer_data.xlsx"
)
df.to_excel(file_path, index=False)

file_path
