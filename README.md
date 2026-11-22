# Restaurant Point of Sale (POS) Console System
### Group 2 - Generation 6

A modular, interactive console-based Point of Sale (POS) system built in Python for restaurant dine-in and takeaway operations, table tracking, multi-currency billing (USD / KHR), receipt printing, sales reporting, and admin menu controls.

---

## Prerequisites

* Python 3.10 or higher (Python 3.13+ recommended)
* Uses only the Python standard library (json, csv, hashlib, datetime) - no pip install required.

---

## How to Run

Open your terminal in the project root directory and run:

```bash
python main.py
```

---

## Login Credentials

Log in with one of the pre-configured staff accounts:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| Admin | admin | admin123 | Full access: POS checkout, sales reports, and Admin Menu Management |
| Cashier | cashier | cashier123 | POS ordering, checkout (USD/KHR), receipts, and sales reports |
| Waiter | waiter | waiter123 | Table status viewing, order creation, and menu browsing |

---

## Console Navigation Guide

Once logged in, the main dashboard provides the following options:

```text
 1. View Restaurant Menu        - Display food and drink catalog with prices and stock status
 2. View Table Status           - View live table layout, seat capacity, and occupancy status
 3. Start New Order             - Create a new Dine-In order (auto-occupies table) or Takeaway order
 4. Manage Active Order         - Add items (by ID), update quantities, or remove items
 5. View Active Order Summary   - Display current subtotal and itemized list
 6. Proceed to Checkout & Pay   - Apply discount %, choose USD/KHR, pay (Cash/Card/KHQR),
                                  calculate change, print receipt, and release table
 7. Sales Reports               - View Daily report, Monthly report, Total revenue, and Popular items
 8. Admin Menu Management       - (Admin only) Add food/drink, edit prices/names, toggle stock, or delete
 9. Save All Data to Disk       - Manually sync all changes to JSON persistence files
 10. View Current Profile       - Show logged-in staff member details and role
 0. Logout & Exit               - End session and exit cleanly
```

---

## Billing and Checkout Flow (Option 6)

1. Discount: Enter a discount percentage (e.g., 10 for 10%, or 0 for none).
2. Currency: Select 1 for USD ($) or 2 for KHR (Riel) (Exchange rate: 1 USD = 4,000 KHR).
3. Payment Method: Select Cash, Card, or KHQR.
4. Amount Tendered: Enter customer payment. If insufficient, payment is rejected.
5. Receipt & Records:
   * An official itemized receipt is generated and displayed.
   * Dine-in tables are automatically released back to Available.
   * Transaction is recorded to data/sales.csv and data/orders.json.

---

## Automated Demo & Tests

Run without interactive prompts to verify system functionality:

```bash
# 1. Run full automated end-to-end POS workflow demo
python main.py --demo

# 2. Run Sprint 3 verification test suite (discounts, KHR/USD, receipts, reports)
python sprint3_test.py

# 3. Run sales reporting and popular items verification
python test_data.py

# 4. Run order management workflow test
python order_test.py
```
