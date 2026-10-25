USE SalesDataWarehouse;
GO

-- Correct missing city
UPDATE Dim_Customer
SET city = 'Wolfsburg'
WHERE customer_key = 3;

-- Correct duplicate customer ID
UPDATE Dim_Customer
SET customer_id = 105
WHERE customer_key = 5;

SELECT * FROM Dim_Customer;

SELECT * FROM Dim_Product;

SELECT * FROM Dim_Store;


-- Check total number of dates
SELECT COUNT(*) AS total_dates
FROM Dim_Date;

-- Check first 10 dates
SELECT TOP 10 *
FROM Dim_Date
ORDER BY full_date;

-- Check the date of our existing order
SELECT *
FROM Dim_Date
WHERE date_key = 20261001;

