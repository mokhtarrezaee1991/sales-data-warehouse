import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# ==========================================
# 1. TRANSFORM: Generate date dimension
# ==========================================

dates = pd.date_range(
    start="2026-01-01",
    end="2026-12-31",
    freq="D"
)

date_data = pd.DataFrame({
    "full_date": dates
})

# Create date attributes
date_data["date_key"] = date_data["full_date"].dt.strftime("%Y%m%d").astype(int)
date_data["day"] = date_data["full_date"].dt.day
date_data["month"] = date_data["full_date"].dt.month
date_data["quarter"] = date_data["full_date"].dt.quarter
date_data["year"] = date_data["full_date"].dt.year

# Arrange columns
date_data = date_data[
    ["date_key", "full_date", "day", "month", "quarter", "year"]
]

print("DATE DIMENSION:")
print(date_data.head())

print("\nTotal dates:", len(date_data))


# ==========================================
# 2. CONNECT: SQL Server Data Warehouse
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
# 3. LOAD: Dim_Date
# ==========================================

with engine.begin() as connection:

    # Check whether the table already contains data
    result = connection.execute(
        text("SELECT COUNT(*) FROM Dim_Date")
    )

    existing_rows = result.scalar_one()

    if existing_rows == 0:

        date_data.to_sql(
            name="Dim_Date",
            con=connection,
            if_exists="append",
            index=False
        )

        print("\nDim_Date loaded successfully!")

    else:
        print("\nDim_Date already contains data. Loading skipped.")


# ==========================================
# 4. CLOSE CONNECTION
# ==========================================

engine.dispose()

print("\nDate ETL process completed!")