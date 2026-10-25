import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# 1. Connect to SQL Server
connection_url = URL.create(
    "mssql+pyodbc",
    host=r"localhost\SQLEXPRESS",
    database="SalesSourceDB",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Trusted_Connection": "yes",
        "TrustServerCertificate": "yes"
    }
)

engine = create_engine(connection_url)

# 2. Extract data from SQL Server
with engine.connect() as connection:
    orders_data = pd.read_sql(
        "SELECT * FROM Orders",
        connection
    )

    order_items_data = pd.read_sql(
        "SELECT * FROM Order_Items",
        connection
    )

# 3. Transform: Merge orders and order items
sales_data = pd.merge(
    orders_data,
    order_items_data,
    on="order_id",
    how="inner",
    validate="one_to_many"
)

# 4. Transform: Calculate total revenue
sales_data["total_amount"] = (
    sales_data["quantity"] * sales_data["unit_price"]
)

# 5. Display results
print("TRANSFORMED SALES DATA:")
print(sales_data.to_string(index=False))

print("\nTOTAL REVENUE:")
print(sales_data["total_amount"].sum())

print("\nDATA SHAPE:")
print(sales_data.shape)