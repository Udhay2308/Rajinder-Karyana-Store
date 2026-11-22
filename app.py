"""
app.py - Interactive Web Dashboard for Rajinder Karyana Store
Built for 1-Day B.Tech Take-Home Assignment
Runs locally on Flask without internet access needed.
"""

import os
import csv
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import inventory

app = Flask(__name__)
app.secret_key = "karyana-village-store-secret-key"

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.csv')


def get_current_ref_date(request_args=None):
    """Returns the reference date for calculations."""
    if request_args and request_args.get('ref_date'):
        try:
            return datetime.strptime(request_args.get('ref_date'), "%Y-%m-%d").date()
        except ValueError:
            pass
    return inventory.DEFAULT_REFERENCE_DATE


@app.route('/')
def dashboard():
    ref_date = get_current_ref_date(request.args)
    crit_days = int(request.args.get('crit_days', inventory.DEFAULT_EXPIRY_CRITICAL_DAYS))
    warn_days = int(request.args.get('warn_days', inventory.DEFAULT_EXPIRY_WARNING_DAYS))
    stockout_days = float(request.args.get('stockout_days', inventory.DEFAULT_STOCKOUT_RISK_DAYS))
    selected_category = request.args.get('category', 'ALL')
    search_query = request.args.get('q', '').strip().lower()

    summary = inventory.audit_inventory(
        DATA_FILE,
        ref_date=ref_date,
        crit_exp_days=crit_days,
        warn_exp_days=warn_days,
        stockout_days=stockout_days
    )

    # Filter items for main table if requested
    filtered_items = summary['all_items']
    if selected_category != 'ALL':
        filtered_items = [itm for itm in filtered_items if itm['category'].upper() == selected_category.upper()]
    if search_query:
        filtered_items = [
            itm for itm in filtered_items 
            if search_query in itm['item_name'].lower() 
            or search_query in itm['category'].lower() 
            or search_query in itm['shelf_location'].lower()
        ]

    categories = sorted(list(set(itm['category'] for itm in summary['all_items'])))

    return render_template(
        'index.html',
        summary=summary,
        items=filtered_items,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        ref_date=ref_date.strftime("%Y-%m-%d"),
        crit_days=crit_days,
        warn_days=warn_days,
        stockout_days=stockout_days
    )


@app.route('/update_stock', methods=['POST'])
@app.route('/restock', methods=['POST'])
def update_stock():
    """
    Handles stock updates:
    - RESTOCK: Incoming goods from distributor (+)
    - SELL: Customer sale (-)
    - RETURN: Returning expired/damaged goods to distributor (-)
    """
    item_id = request.form.get('item_id', '').strip()
    action_type = request.form.get('action_type', 'RESTOCK').upper()
    try:
        qty = int(request.form.get('qty', request.form.get('incoming_qty', 0)))
    except ValueError:
        flash("अमान्य मात्रा (Invalid quantity entered)", "error")
        return redirect(url_for('dashboard'))

    if qty <= 0:
        flash("कृपया कम से कम 1 मात्रा दर्ज करें (Please enter quantity >= 1)", "warning")
        return redirect(url_for('dashboard'))

    today_str = date.today().strftime("%Y-%m-%d")
    updated = False
    item_name = ""
    new_stock = 0

    rows = []
    with open(DATA_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            if r['item_id'] == item_id:
                try:
                    old_stock = int(float(r['current_stock']))
                except ValueError:
                    old_stock = 0
                
                item_name = r['item_name']
                if action_type == 'RESTOCK':
                    new_stock = old_stock + qty
                    r['current_stock'] = str(new_stock)
                    r['last_restocked_date'] = today_str
                    if "OUT OF STOCK" in r.get('notes', ''):
                        r['notes'] = f"Restocked +{qty} on {today_str}"
                    flash(f"📥 {item_name}: {qty} पैकेट नया स्टॉक जोड़ा गया (वर्तमान स्टॉक: {new_stock})", "success")
                elif action_type == 'SELL':
                    if old_stock < qty:
                        flash(f"⚠️ स्टॉक कम है! {item_name} केवल {old_stock} बचा है, {qty} नहीं बेच सकते।", "error")
                        return redirect(url_for('dashboard'))
                    new_stock = old_stock - qty
                    r['current_stock'] = str(new_stock)
                    if new_stock == 0:
                        r['notes'] = f"OUT OF STOCK - sold out on {today_str}"
                    flash(f"🛒 {item_name}: {qty} पैकेट बिक्री दर्ज हुई (बाकी स्टॉक: {new_stock})", "success")
                elif action_type == 'RETURN':
                    if old_stock < qty:
                        flash(f"⚠️ दुकान में {item_name} के केवल {old_stock} पैकेट हैं, {qty} वापस नहीं हो सकते।", "error")
                        return redirect(url_for('dashboard'))
                    new_stock = old_stock - qty
                    r['current_stock'] = str(new_stock)
                    r['notes'] = f"Returned {qty} packs to distributor on {today_str}"
                    flash(f"↩️ {item_name}: {qty} पैकेट डिस्ट्रीब्यूटर को वापस किए गए (बाकी स्टॉक: {new_stock})", "warning")
                
                updated = True
            rows.append(r)

    if updated:
        with open(DATA_FILE, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        flash("आइटम नहीं मिला (Item not found)", "error")

    return redirect(url_for('dashboard'))


@app.route('/api/summary')
def api_summary():
    """JSON endpoint for healthcheck and summary statistics."""
    ref_date = get_current_ref_date(request.args)
    summary = inventory.audit_inventory(DATA_FILE, ref_date=ref_date)
    return jsonify({
        'total_items': summary['total_items'],
        'out_of_stock_count': len(summary['out_of_stock']),
        'expiring_critical_count': len(summary['expiring_critical']),
        'expiring_warning_count': len(summary['expiring_warning']),
        'total_inventory_cost': summary['total_inventory_cost'],
        'at_risk_expiry_cost': summary['at_risk_expiry_cost'],
        'skipped_rows_count': len(summary['skipped_rows'])
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🚀 Starting Rajinder Karyana Store Dashboard on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)

