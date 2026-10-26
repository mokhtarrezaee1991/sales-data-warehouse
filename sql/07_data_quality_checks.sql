USE SalesDataWarehouse;
GO

SELECT
    customer_id,
    COUNT(*) AS occurrences
FROM Dim_Customer
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Check dimension row counts
SELECT 'Dim_Customer' AS table_name, COUNT(*) AS row_count
FROM Dim_Customer

UNION ALL

SELECT 'Dim_Product', COUNT(*)
FROM Dim_Product

UNION ALL

SELECT 'Dim_Store', COUNT(*)
FROM Dim_Store

UNION ALL

SELECT 'Dim_Date', COUNT(*)
FROM Dim_Date

UNION ALL

SELECT 'Fact_Sales', COUNT(*)
FROM Fact_Sales;