import pandas as pd

# Create a sample DataFrame
data = {
    "order_id": [101, 102, 103, 104, 105],
    "customer_id": [1, 1, 2, 2, 3],
    "order_date": [
        "2015-01-01",
        "2016-02-15",
        "2017-03-20",
        "2018-04-25",
        "2019-05-30",
    ],
    "revenue": [1000, 1500, 2000, 2500, 3000],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to an Excel file
file_path = "/Users/webdevmac/Python Programming/CLTV_PROJECT/cltv_project/cltv_app/static/sample_files/customer_data.xlsx"
df.to_excel(file_path, index=False)
