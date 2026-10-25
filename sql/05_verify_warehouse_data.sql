USE SalesDataWarehouse;
GO

-- Show sales fact table
SELECT * FROM Fact_Sales;

-- Count sales rows and calculate revenue
SELECT
    COUNT(*) AS sales_rows,
    SUM(total_amount) AS total_revenue
FROM Fact_Sales;