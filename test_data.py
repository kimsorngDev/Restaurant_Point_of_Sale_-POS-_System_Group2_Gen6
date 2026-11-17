from data_manager import load_menu, load_tables, load_orders, load_sales, daily_sales_report, monthly_sales_report, calculate_total_sales, popular_items

menu = load_menu()
tables = load_tables()

print("Menu Data:")
print(menu)

print("Table Data:")
print(tables)

orders = load_orders()
print("Order Data")
print(orders)

test_order = [
    {
        "order_id": "001",
        "date": "2026-11-15",
        "table_number": "T01",
        "items": [
            {
                "item_id": "F01",
                "name": "Fried Rice",
                "quantity": 1,
                "price": 3.0
            }
        ],
        "subtotal": 3.0,
        "status": "New"
    }
]


print("Saved Order Data:")
print(load_orders())

#save_sales("001", "R001", "2026-11-15", 5.0, "USD", "Cash")

print("Sales Records:")
print(load_sales())

#save_sales("002", "R002", "2026-11-15", 20000, "KHR", "Cash")

print("Daily Sales Report:")
records, totals = daily_sales_report("2026-11-15")

print(records)
print("USD Total:", totals["USD"])
print("KHR Total:", totals["KHR"])

print("Monthly Sales Report:")
records, totals = monthly_sales_report("2026-11")

print(records)
print("USD Total:", totals["USD"])
print("KHR Total:", totals["KHR"])

print("Total Sales:")
totals = calculate_total_sales()

print("USD Total:", totals["USD"])
print("KHR Total:", totals["KHR"])

print("Testing actual popular_items function:")

test_orders = [
    {
        "items": [
            {"item_id": "F01", "name": "Fried Rice", "quantity": 2}
        ]
    },
    {
        "items": [
            {"item_id": "F01", "name": "Fried Rice", "quantity": 3},
            {"item_id": "D01", "name": "Iced Coffee", "quantity": 2}
        ]
    }
]

food, drink = popular_items(test_orders)

print("Popular Food:", food)
print("Popular Drink:", drink)




