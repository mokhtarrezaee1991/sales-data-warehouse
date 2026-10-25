import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# ==========================================
# 1. EXTRACT: Read source files
# ==========================================

customers_data = pd.read_csv("data/customers.csv")
products_data = pd.read_excel("data/products.xlsx")
stores_data = pd.read_csv("data/stores.csv")

customers_data["registration_date"] = pd.to_datetime(
    customers_data["registration_date"]
)


# ==========================================
# 2. CONNECT: Data Warehouse
# ==========================================

connection_url = URL.create(
    "mssql+pyodbc",
    host=r"localhost\SQLEXPRESS",
    database="SalesDataWarehouse",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Trusted_Connection": "yes",
        "TrustServerCertificate": "yes"
    }
)

engine = create_engine(connection_url)


# ==========================================
# 3. FUNCTION: Load only new records
# ==========================================

def load_new_records(source_data, table_name, id_column, connection):

    # Check duplicate IDs in source data
    if source_data[id_column].duplicated().any():
        raise ValueError(
            f"Duplicate IDs found in source data: {table_name}"
        )

    # Read existing IDs from warehouse
    existing_data = pd.read_sql(
        f"SELECT {id_column} FROM {table_name}",
        connection
    )

    # Find only new records
    new_data = source_data[
        ~source_data[id_column].isin(existing_data[id_column])
    ]

    # Load new records
    if not new_data.empty:
        new_data.to_sql(
            name=table_name,
            con=connection,
            if_exists="append",
            index=False
        )

        print(f"{table_name}: {len(new_data)} new records loaded.")

    else:
        print(f"{table_name}: No new records.")


# ==========================================
# 4. LOAD: Dimension tables
# ==========================================

with engine.begin() as connection:

    load_new_records(
        customers_data,
        "Dim_Customer",
        "customer_id",
        connection
    )

    load_new_records(
        products_data,
        "Dim_Product",
        "product_id",
        connection
    )

    load_new_records(
        stores_data,
        "Dim_Store",
        "store_id",
        connection
    )


# ==========================================
# 5. CLOSE CONNECTION
# ==========================================

engine.dispose()

print("\nDimension loading completed!")