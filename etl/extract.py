import pandas as pd

# Read the CSV file
customers_data=pd.read_csv("data/customers.csv")
stores_data=pd.read_csv("data/stores.csv")
products_data=pd.read_excel("data/products.xlsx")

#read the first 5 rows
print(customers_data.head())
print(stores_data.head())
print(products_data.head())

print("-----------------------------------------------------------------------------------")

print(customers_data.shape)

print("-----------------------------------------------------------------------------------")

print(customers_data.dtypes)

customers_data["registration_date"]=pd.to_datetime(customers_data["registration_date"])
print("-----------------------------------------------------------------------------------")
print(customers_data.dtypes)
print("-----------------------------------------------------------------------------------")
print(customers_data["customer_id"].duplicated().sum())
print("-----------------------------------------------------------------------------------")
print(customers_data.isnull().sum())

