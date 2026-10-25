import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# SQL Server connection
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

# Read SQL Server tables
with engine.connect() as connection:
    orders_data = pd.read_sql(
        "SELECT * FROM Orders", connection
    )

    order_items_data = pd.read_sql(
        "SELECT * FROM Order_Items", connection
    )

print("ORDERS:")
print(orders_data.head())

print("\nORDER ITEMS:")
print(order_items_data.head())