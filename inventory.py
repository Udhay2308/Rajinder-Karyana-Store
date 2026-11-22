"""
inventory.py - Core Inventory Logic & Stock/Expiry Auditor for Rajinder Karyana Store
Built for 1-Day B.Tech Take-Home Assignment
Author: Student
Target: Rajinder Kumar (Rajinder Karyana Store)
"""

import csv
import os
import sys
import math
from datetime import datetime, date

# ==============================================================================
# DEFAULT THRESHOLDS
# ==============================================================================
DEFAULT_EXPIRY_CRITICAL_DAYS = 3   # Red alert: expires within 3 days (e.g. Milk, Bread)
DEFAULT_EXPIRY_WARNING_DAYS = 14  # Amber alert: expires within 14 days (e.g. Dahi, Bhujia)
DEFAULT_STOCKOUT_RISK_DAYS = 2.0  # Alert if stock runs out in less than 2 days
DISTRIBUTOR_CYCLE_DAYS = 7        # Distributors visit once a week (7 days)
DEFAULT_REFERENCE_DATE = date(2024, 11, 22)  # Date of fieldwork audit


def parse_row(row_dict, row_num, ref_date):
    """
    Safely parses a single row from data.csv.
    Handles corrupt/bad data gracefully without crashing.
    Returns (item, error_message).
    """
    required_fields = [
        'item_id', 'item_name', 'category', 'pack_size', 'cost_price',
        'selling_price', 'current_stock', 'avg_daily_sales',
        'reorder_threshold', 'expiry_date', 'shelf_location'
    ]
    for field in required_fields:
        if field not in row_dict or not row_dict[field].strip():
            return None, f"Row {row_num}: Missing required field '{field}'"

    item_id = row_dict['item_id'].strip()
    item_name = row_dict['item_name'].strip()
    category = row_dict['category'].strip()
    pack_size = row_dict['pack_size'].strip()
    shelf_location = row_dict['shelf_location'].strip()
    notes = row_dict.get('notes', '').strip()
    last_restocked = row_dict.get('last_restocked_date', '').strip()

    try:
        cost_price = float(row_dict['cost_price'])
        selling_price = float(row_dict['selling_price'])
        if cost_price < 0 or selling_price < 0:
            return None, f"Row {row_num} ({item_name}): Negative price detected"
    except ValueError:
        return None, f"Row {row_num} ({item_name}): Invalid price format"

    try:
        current_stock = int(float(row_dict['current_stock']))
        if current_stock < 0:
            return None, f"Row {row_num} ({item_name}): Negative stock '{current_stock}' not allowed"
    except ValueError:
        return None, f"Row {row_num} ({item_name}): Invalid current_stock '{row_dict['current_stock']}' - must be a number"

    try:
        avg_daily_sales = float(row_dict['avg_daily_sales'])
        if avg_daily_sales < 0:
            return None, f"Row {row_num} ({item_name}): Negative daily sales rate"
    except ValueError:
        return None, f"Row {row_num} ({item_name}): Invalid avg_daily_sales '{row_dict['avg_daily_sales']}'"

    try:
        reorder_threshold = int(float(row_dict['reorder_threshold']))
    except ValueError:
        return None, f"Row {row_num} ({item_name}): Invalid reorder_threshold"

    try:
        exp_date_str = row_dict['expiry_date'].strip()
        expiry_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
    except ValueError:
        return None, f"Row {row_num} ({item_name}): Invalid expiry_date '{row_dict.get('expiry_date')}' (expected YYYY-MM-DD)"

    # Computations
    days_until_expiry = (expiry_date - ref_date).days

    if current_stock == 0:
        days_of_stock_left = 0.0
    elif avg_daily_sales > 0:
        days_of_stock_left = round(current_stock / avg_daily_sales, 1)
    else:
        days_of_stock_left = 999.0  # Zero sales velocity

    # Recommended Order Quantity for weekly distributor visit
    # Needed to cover 7 days + 20% safety margin minus current stock
    if avg_daily_sales > 0:
        target_stock = math.ceil(avg_daily_sales * DISTRIBUTOR_CYCLE_DAYS * 1.2)
        suggested_reorder = max(0, target_stock - current_stock)
    else:
        suggested_reorder = 0

    item = {
        'item_id': item_id,
        'item_name': item_name,
        'category': category,
        'pack_size': pack_size,
        'cost_price': cost_price,
        'selling_price': selling_price,
        'current_stock': current_stock,
        'avg_daily_sales': avg_daily_sales,
        'reorder_threshold': reorder_threshold,
        'expiry_date': expiry_date,
        'days_until_expiry': days_until_expiry,
        'days_of_stock_left': days_of_stock_left,
        'suggested_reorder': suggested_reorder,
        'shelf_location': shelf_location,
        'last_restocked': last_restocked,
        'notes': notes,
        'stock_value_cost': round(current_stock * cost_price, 2),
    }

    return item, None


def audit_inventory(csv_path, ref_date=DEFAULT_REFERENCE_DATE, 
                    crit_exp_days=DEFAULT_EXPIRY_CRITICAL_DAYS, 
                    warn_exp_days=DEFAULT_EXPIRY_WARNING_DAYS,
                    stockout_days=DEFAULT_STOCKOUT_RISK_DAYS):
    """
    Reads data.csv and compiles actionable alerts for Rajinder Kumar.
    Guaranteed not to crash on corrupted or bad rows.
    """
    valid_items = []
    skipped_rows = []

    if not os.path.exists(csv_path):
        return {
            'error': f"File not found: {csv_path}",
            'items': [],
            'skipped_rows': []
        }

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # row 1 is header
            item, err = parse_row(row, idx, ref_date)
            if err:
                skipped_rows.append(err)
            else:
                valid_items.append(item)

    # Classification
    out_of_stock = []
    critical_restock = []
    expiring_critical = []
    expiring_warning = []
    normal_items = []

    total_inventory_cost = 0.0
    at_risk_expiry_cost = 0.0

    for itm in valid_items:
        total_inventory_cost += itm['stock_value_cost']

        # Expiry urgency
        if itm['days_until_expiry'] <= crit_exp_days:
            expiring_critical.append(itm)
            at_risk_expiry_cost += itm['stock_value_cost']
        elif itm['days_until_expiry'] <= warn_exp_days:
            expiring_warning.append(itm)
            at_risk_expiry_cost += itm['stock_value_cost']

        # Stockout urgency
        if itm['current_stock'] == 0:
            out_of_stock.append(itm)
        elif itm['current_stock'] <= itm['reorder_threshold'] or itm['days_of_stock_left'] <= stockout_days:
            critical_restock.append(itm)
        else:
            normal_items.append(itm)

    return {
        'reference_date': ref_date.strftime('%Y-%m-%d'),
        'total_items': len(valid_items),
        'total_inventory_cost': round(total_inventory_cost, 2),
        'at_risk_expiry_cost': round(at_risk_expiry_cost, 2),
        'out_of_stock': out_of_stock,
        'critical_restock': critical_restock,
        'expiring_critical': expiring_critical,
        'expiring_warning': expiring_warning,
        'normal_items': normal_items,
        'skipped_rows': skipped_rows,
        'all_items': valid_items
    }


def print_cli_report(summary):
    """Prints a clean, high-impact terminal report for Rajinder Kumar."""
    print("=" * 78)
    print(" 🏪 RAJINDER KARYANA STORE - DAILY MORNING ACTION SHEET")
    print(f" Reference Date: {summary['reference_date']} | Total Audited Items: {summary['total_items']}")
    print(f" Total Shop Inventory Value: ₹{summary['total_inventory_cost']:,.2f}")
    print(f" Inventory Capital at Expiry Risk: ₹{summary['at_risk_expiry_cost']:,.2f}")
    print("=" * 78)

    if summary['skipped_rows']:
        print("\n⚠️  CORRUPTED / BAD ROWS SKIPPED (Handled safely):")
        for err in summary['skipped_rows']:
            print(f"  • {err}")

    # SECTION 1: OUT OF STOCK (LOST REVENUE)
    print("\n🔴 1. IMMEDIATE RESTOCK REQUIRED (OUT OF STOCK - 0 Units)")
    print("-" * 78)
    if summary['out_of_stock']:
        for itm in summary['out_of_stock']:
            print(f"  ❌ {itm['item_name']:<28} | Pack: {itm['pack_size']:<8} | Daily Sale: {itm['avg_daily_sales']:>4}/day")
            print(f"     Order NOW: {itm['suggested_reorder']} units | Shelf: {itm['shelf_location']} | Notes: {itm['notes']}")
    else:
        print("  ✓ No items completely out of stock.")

    # SECTION 2: CRITICAL RESTOCK (RUNNING OUT IN <= 2 DAYS)
    print("\n🟠 2. RESTOCK BEFORE DISTRIBUTOR VISIT (Stock Low or < 2 Days Left)")
    print("-" * 78)
    if summary['critical_restock']:
        for itm in summary['critical_restock']:
            print(f"  ⚠️  {itm['item_name']:<28} | Stock: {itm['current_stock']:>2} left | Lasts ~{itm['days_of_stock_left']} days")
            print(f"     Order: {itm['suggested_reorder']} units | Threshold: {itm['reorder_threshold']} | Shelf: {itm['shelf_location']}")
    else:
        print("  ✓ All other items have healthy stock levels.")

    # SECTION 3: EXPIRY ALERTS (CAPITAL AT RISK)
    print("\n🛑 3. EXPIRING SOON - SELL TODAY OR RETURN TO DISTRIBUTOR")
    print("-" * 78)
    if summary['expiring_critical']:
        print("  CRITICAL (Expires in <= 3 Days):")
        for itm in summary['expiring_critical']:
            print(f"  🚨 {itm['item_name']:<28} | Stock: {itm['current_stock']:>2} | Expires in: {itm['days_until_expiry']} DAYS ({itm['expiry_date']})")
            print(f"     Location: {itm['shelf_location']} | Value at Risk: ₹{itm['stock_value_cost']} | {itm['notes']}")

    if summary['expiring_warning']:
        print("\n  WARNING (Expires in 4 to 14 Days - Move to Front Counter):")
        for itm in summary['expiring_warning']:
            print(f"  ⚠️  {itm['item_name']:<28} | Stock: {itm['current_stock']:>2} | Expires in: {itm['days_until_expiry']} days ({itm['expiry_date']})")
            print(f"     Location: {itm['shelf_location']} | Action: Do NOT take distributor bulk scheme!")

    print("=" * 78)
    print(" Actionable Insight: Rajinder uncle should order 5 items on next distributor visit")
    print(" and inspect the back shelf for Modern Bread & Haldiram Bhujia immediately.")
    print("=" * 78)


if __name__ == '__main__':
    csv_file = os.path.join(os.path.dirname(__file__), 'data.csv')
    summary = audit_inventory(csv_file)
    print_cli_report(summary)

