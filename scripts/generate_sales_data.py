"""Generate reproducible synthetic orders and order items for SalesSourceDB.

Run from the sales-data-warehouse repository root:
    python scripts/generate_sales_data.py
"""
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
import csv
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'generated'
OUT.mkdir(parents=True, exist_ok=True)

rng = random.Random(42)
product_prices = {10: '800.00', 20: '25.00', 30: '35.00', 40: '240.00', 50: '65.00', 60: '75.00', 70: '90.00', 80: '120.00'}
start_date = date(2026, 1, 1)
end_date = date(2026, 12, 31)
span = (end_date - start_date).days

orders = []
items = []
next_item_id = 3  # Existing SalesSourceDB item IDs are 1 and 2.
for order_id in range(1002, 2002):
    customer_id = rng.randint(101, 105)
    store_id = rng.randint(1, 5)
    order_date = start_date + timedelta(days=rng.randint(0, span))
    status = rng.choices(['Completed', 'Cancelled'], weights=[95, 5], k=1)[0]
    orders.append([order_id, customer_id, store_id, order_date.isoformat(), status])
    for product_id in rng.sample(list(product_prices), k=rng.randint(1, 4)):
        items.append([next_item_id, order_id, product_id, rng.randint(1, 5), product_prices[product_id]])
        next_item_id += 1

for filename, header, rows in [
    ('orders_generated.csv', ['order_id','customer_id','store_id','order_date','order_status'], orders),
    ('order_items_generated.csv', ['order_item_id','order_id','product_id','quantity','unit_price'], items),
]:
    with (OUT / filename).open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

print(f'Generated {len(orders)} orders and {len(items)} order items in {OUT}')
