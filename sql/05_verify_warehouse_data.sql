USE SalesDataWarehouse;
GO

-- Show sales fact table
SELECT * FROM Fact_Sales;

-- Count sales rows and calculate revenue
SELECT
    COUNT(*) AS sales_rows,
    SUM(total_amount) AS total_revenue
FROM Fact_Sales;

USE SalesDataWarehouse;
GO

-- Total sales and revenue
SELECT
    COUNT(*) AS sales_rows,
    SUM(total_amount) AS total_revenue
FROM Fact_Sales;

-- Revenue by product category
SELECT
    p.category,
    SUM(f.total_amount) AS total_revenue
FROM Fact_Sales f
JOIN Dim_Product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Revenue by store
SELECT
    s.store_name,
    SUM(f.total_amount) AS total_revenue
FROM Fact_Sales f
JOIN Dim_Store s
    ON f.store_key = s.store_key
GROUP BY s.store_name
ORDER BY total_revenue DESC;