USE SalesSourceDB;
GO

INSERT INTO Orders
    (order_id, customer_id, store_id, order_date, order_status)
VALUES
    (1001, 101, 1, '2026-10-01', 'Completed');
GO

INSERT INTO Order_Items
    (order_item_id, order_id, product_id, quantity, unit_price)
VALUES
    (1, 1001, 10, 2, 800.00),
    (2, 1001, 20, 1, 25.00);
GO