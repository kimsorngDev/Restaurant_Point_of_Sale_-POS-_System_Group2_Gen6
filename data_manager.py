import json
import os 
import csv

def load_menu():
    try:
        with open("data/menu.json", "r") as file:
            menu = json.load(file)
        return menu

    except FileNotFoundError:
        print("Menu file not found.")
        return []

    except json.JSONDecodeError:
        print("Menu file contains invalid JSON.")
        return []

def load_tables():
    try:
        with open("data/tables.json", "r") as file:
            tables = json.load(file)
        return tables

    except FileNotFoundError:
        print("Tables file not found.")
        return []

    except json.JSONDecodeError:
        print("Tables file contains invalid JSON.")
        return []

def save_json(filename, data):
    try:
        with open("data/" + filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Data saved successfully.")

    except OSError:
        print("Error saving data.")

def load_orders():
    try:
        with open("data/orders.json", "r") as file:
            orders = json.load(file)
        return orders

    except FileNotFoundError:
        print("Orders file not found.")
        return []

    except json.JSONDecodeError:
        print("Orders file contains invalid JSON.")
        return []

def save_sales(order_id, receipt_id, date, total, currency, payment_method):
    try:
        with open("data/sales.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([order_id, receipt_id, date, total, currency, payment_method])
        print("Sales data saved.")

    except OSError:
        print("Error saving sales data.")

def load_sales():
    try:
        with open("data/sales.csv", "r") as file:
            reader = csv.DictReader(file)
            sales = []

            for row in reader:
                sales.append(row)

            return sales

    except FileNotFoundError:
        print("Sales file not found.")
        return []

def daily_sales_report(date):
    sales = load_sales()
    daily_sales = []
    usd_total = 0
    khr_total = 0

    for sale in sales:
        if sale["date"] == date:
            daily_sales.append(sale)

            if sale["currency"] == "USD":
                usd_total += float(sale["total"])
            elif sale["currency"] == "KHR":
                khr_total += float(sale["total"])

    totals = {
        "USD": usd_total,
        "KHR": khr_total
    }

    return daily_sales, totals


def monthly_sales_report(month):
    sales = load_sales()
    monthly_sales = []
    usd_total = 0
    khr_total = 0

    for sale in sales:
        if sale["date"].startswith(month):
            monthly_sales.append(sale)

            if sale["currency"] == "USD":
                usd_total += float(sale["total"])
            elif sale["currency"] == "KHR":
                khr_total += float(sale["total"])

    totals = {
        "USD": usd_total,
        "KHR": khr_total
    }

    return monthly_sales, totals


def calculate_total_sales():
    sales = load_sales()
    usd_total = 0
    khr_total = 0

    for sale in sales:
        if sale["currency"] == "USD":
            usd_total += float(sale["total"])
        elif sale["currency"] == "KHR":
            khr_total += float(sale["total"])

    return {
        "USD": usd_total,
        "KHR": khr_total
    }

def popular_items(orders=None):
    if orders is None:
        orders = load_orders()

    menu = load_menu()

    food_counts = {}
    drink_counts = {}

    for order in orders:
        for item in order["items"]:
            for menu_item in menu:
                if item["item_id"] == menu_item["item_id"]:

                    if menu_item["category"] == "Food":
                        name = item["name"]

                        if name in food_counts:
                            food_counts[name] += item["quantity"]
                        else:
                            food_counts[name] = item["quantity"]

                    elif menu_item["category"] == "Drink":
                        name = item["name"]

                        if name in drink_counts:
                            drink_counts[name] += item["quantity"]
                        else:
                            drink_counts[name] = item["quantity"]

    popular_food = ""
    popular_drink = ""
    food_quantity = 0
    drink_quantity = 0

    for name, quantity in food_counts.items():
        if quantity > food_quantity:
            food_quantity = quantity
            popular_food = name

    for name, quantity in drink_counts.items():
        if quantity > drink_quantity:
            drink_quantity = quantity
            popular_drink = name

    return popular_food, popular_drink