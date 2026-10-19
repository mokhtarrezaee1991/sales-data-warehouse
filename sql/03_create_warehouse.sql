CREATE DATABASE SalesDataWarehouse;
GO

USE SalesDataWarehouse;
GO



CREATE TABLE Dim_Customer (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    email VARCHAR(255),
    registration_date DATE
);
GO

CREATE TABLE Dim_Product (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(150),
    category VARCHAR(100),
    unit_price DECIMAL(10,2)
);
GO

CREATE TABLE Dim_Store (
    store_key INT IDENTITY(1,1) PRIMARY KEY,
    store_id INT NOT NULL,
    store_name VARCHAR(150),
    city VARCHAR(100),
    country VARCHAR(100)
);
GO

CREATE TABLE Dim_Date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT,
    month INT,
    quarter INT,
    year INT
);
GO


CREATE TABLE Fact_Sales (
    sales_key INT IDENTITY(1,1) PRIMARY KEY,

    order_id INT NOT NULL,
    order_item_id INT NOT NULL,

    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    store_key INT NOT NULL,
    date_key INT NOT NULL,

    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,

    CONSTRAINT FK_Sales_Customer
        FOREIGN KEY (customer_key)
        REFERENCES Dim_Customer(customer_key),

    CONSTRAINT FK_Sales_Product
        FOREIGN KEY (product_key)
        REFERENCES Dim_Product(product_key),

    CONSTRAINT FK_Sales_Store
        FOREIGN KEY (store_key)
        REFERENCES Dim_Store(store_key),

    CONSTRAINT FK_Sales_Date
        FOREIGN KEY (date_key)
        REFERENCES Dim_Date(date_key)
);
GO