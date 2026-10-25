USE SalesDataWarehouse;
GO

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    SUM(total_amount) AS total_revenue,
    CAST(
        SUM(total_amount) /
        NULLIF(COUNT(DISTINCT order_id), 0)
        AS DECIMAL(12,2)
    ) AS average_order_value
FROM Fact_Sales;


-- Monthly sales analysis
SELECT
    d.year,
    d.month,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_units_sold,
    SUM(f.total_amount) AS total_revenue
FROM Fact_Sales f
INNER JOIN Dim_Date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month
ORDER BY
    d.year,
    d.month;
