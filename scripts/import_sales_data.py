import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# 1. Read generated CSV files
orders = pd.read_csv("data/generated/orders_generated.csv")
order_items = pd.read_csv("data/generated/order_items_generated.csv")

# 2. Connect to source database
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

# 3. Check for existing order IDs before importing
with engine.begin() as connection:
    existing_orders = pd.read_sql(
        "SELECT order_id FROM Orders",
        connection
    )

    existing_items = pd.read_sql(
        "SELECT order_item_id FROM Order_Items",
        connection
    )

    if orders["order_id"].duplicated().any():
        raise ValueError("Duplicate order IDs in generated data.")

    if order_items["order_item_id"].duplicated().any():
        raise ValueError("Duplicate order item IDs in generated data.")

    if orders["order_id"].isin(existing_orders["order_id"]).any():
        raise ValueError("Some order IDs already exist in SQL Server.")

    if order_items["order_item_id"].isin(
        existing_items["order_item_id"]
    ).any():
        raise ValueError("Some order item IDs already exist in SQL Server.")

    valid_order_ids = set(existing_orders["order_id"]) | set(orders["order_id"])

    if not order_items["order_id"].isin(valid_order_ids).all():
        raise ValueError("Some order items reference missing orders.")

    # 4. Insert parent records first
    orders.to_sql(
        "Orders",
        con=connection,
        if_exists="append",
        index=False
    )

    # 5. Insert child records
    order_items.to_sql(
        "Order_Items",
        con=connection,
        if_exists="append",
        index=False
    )

print("Sales data imported successfully!")

engine.dispose()