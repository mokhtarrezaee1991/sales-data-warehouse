import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# ==========================================
# 1. DATABASE CONNECTION
# ==========================================

def get_engine(database):
    connection_url = URL.create(
        "mssql+pyodbc",
        host=r"localhost\SQLEXPRESS",
        database=database,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Trusted_Connection": "yes",
            "TrustServerCertificate": "yes"
        }
    )

    return create_engine(connection_url)


source_engine = get_engine("SalesSourceDB")
warehouse_engine = get_engine("SalesDataWarehouse")


# ==========================================
# 2. EXTRACT: Read source tables
# ==========================================

with source_engine.connect() as connection:
    orders = pd.read_sql(
        "SELECT * FROM Orders", connection
    )

    order_items = pd.read_sql(
        "SELECT * FROM Order_Items", connection
    )


# ==========================================
# 3. TRANSFORM: Merge and calculate revenue
# ==========================================

sales = pd.merge(
    orders,
    order_items,
    on="order_id",
    how="inner",
    validate="one_to_many"
)

# Only completed orders
sales = sales[sales["order_status"] == "Completed"].copy()

sales["total_amount"] = (
    sales["quantity"] * sales["unit_price"]
)

sales["date_key"] = (
    pd.to_datetime(sales["order_date"])
    .dt.strftime("%Y%m%d")
    .astype(int)
)


# ==========================================
# 4. EXTRACT: Read warehouse dimensions
# ==========================================

with warehouse_engine.connect() as connection:

    dim_customer = pd.read_sql(
        "SELECT customer_key, customer_id FROM Dim_Customer",
        connection
    )

    dim_product = pd.read_sql(
        "SELECT product_key, product_id FROM Dim_Product",
        connection
    )

    dim_store = pd.read_sql(
        "SELECT store_key, store_id FROM Dim_Store",
        connection
    )

    dim_date = pd.read_sql(
        "SELECT date_key FROM Dim_Date",
        connection
    )


# ==========================================
# 5. TRANSFORM: Find surrogate keys
# ==========================================

sales = sales.merge(
    dim_customer,
    on="customer_id",
    how="left",
    validate="many_to_one"
)

sales = sales.merge(
    dim_product,
    on="product_id",
    how="left",
    validate="many_to_one"
)

sales = sales.merge(
    dim_store,
    on="store_id",
    how="left",
    validate="many_to_one"
)

sales = sales.merge(
    dim_date,
    on="date_key",
    how="left",
    validate="many_to_one"
)

# Check missing dimension keys
key_columns = [
    "customer_key",
    "product_key",
    "store_key"
]

if sales[key_columns].isnull().any().any():
    raise ValueError("Missing dimension keys. Check source data.")

if len(sales) != len(sales.merge(dim_date, on="date_key", how="inner")):
    raise ValueError("Some order dates are missing in Dim_Date.")


# ==========================================
# 6. PREPARE FACT TABLE
# ==========================================

fact_sales = sales[
    [
        "order_id",
        "order_item_id",
        "customer_key",
        "product_key",
        "store_key",
        "date_key",
        "quantity",
        "unit_price",
        "total_amount"
    ]
].copy()

for column in key_columns:
    fact_sales[column] = fact_sales[column].astype(int)

print("FACT SALES DATA:")
print(fact_sales.to_string(index=False))


# ==========================================
# 7. LOAD: Insert only new order items
# ==========================================

with warehouse_engine.begin() as connection:

    existing_items = pd.read_sql(
        "SELECT order_item_id FROM Fact_Sales",
        connection
    )

    new_sales = fact_sales[
        ~fact_sales["order_item_id"].isin(
            existing_items["order_item_id"]
        )
    ]

    if not new_sales.empty:
        new_sales.to_sql(
            name="Fact_Sales",
            con=connection,
            if_exists="append",
            index=False
        )

        print(f"\n{len(new_sales)} sales rows loaded!")
    else:
        print("\nNo new sales rows to load.")


source_engine.dispose()
warehouse_engine.dispose()

print("\nFact Sales ETL completed!")