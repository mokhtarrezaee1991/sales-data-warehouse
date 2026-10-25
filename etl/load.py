import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# ==========================================
# 1. EXTRACT: Read source files
# ==========================================

# Customers - already loaded into Data Warehouse
# customers_data = pd.read_csv("data/customers.csv")

# Products - Excel
products_data = pd.read_excel("data/products.xlsx")

# Stores - CSV
stores_data = pd.read_csv("data/stores.csv")


# ==========================================
# 2. TRANSFORM: Prepare data
# ==========================================

# Customer date conversion - already completed
# customers_data["registration_date"] = pd.to_datetime(
#     customers_data["registration_date"]
# )

print("PRODUCTS:")
print(products_data.head())

print("\nSTORES:")
print(stores_data.head())


# ==========================================
# 3. CONNECT: SQL Server Data Warehouse
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
# 4. LOAD: Dim_Customer
# ==========================================

# Already loaded - do not execute again

# customers_data.to_sql(
#     name="Dim_Customer",
#     con=engine,
#     if_exists="append",
#     index=False
# )

# print("Customer data loaded successfully!")


# ==========================================
# 5. LOAD: Dim_Product
# ==========================================

products_data.to_sql(
    name="Dim_Product",
    con=engine,
    if_exists="append",
    index=False
)

print("\nProduct data loaded successfully!")


# ==========================================
# 6. LOAD: Dim_Store
# ==========================================

stores_data.to_sql(
    name="Dim_Store",
    con=engine,
    if_exists="append",
    index=False
)

print("Store data loaded successfully!")


# ==========================================
# 7. CLOSE CONNECTION
# ==========================================

engine.dispose()

print("\nETL loading process completed!")