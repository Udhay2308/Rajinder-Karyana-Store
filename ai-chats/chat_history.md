# AI Interaction Log (`ai-chats/chat_history.md`)

*Exported AI interaction history documenting how AI was used for research framing, code scaffolding, and dashboard development.*

---

### Session 1: Problem Scoping & Fieldwork Preparation
**Student:**
> "I am doing a take-home project to solve a real problem for a shopkeeper in my village. The shopkeeper is Rajinder Kumar who runs Rajinder Karyana Store. He keeps running out of essentials like salt and milk, while bread and packaged snacks expire because distributors push bulk cartons for discounts. He doesn't trust complex online accounting apps. I am heading to his shop to audit his stock. What columns should I record in my notebook so I can later turn it into a clean CSV for analysis?"

**AI Assistant:**
> - Suggested recording standard operational fields: item identifier, brand/name, category, pack size, cost price, selling price, physical shelf location, current counted stock, estimated daily sales, minimum threshold, printed batch expiry date, and qualitative condition notes (e.g., damaged packs or out-of-stock reasons).
> - Emphasized recording exact shelf positions (Deep Freezer, Floor Crates, Back Shelves) to help identify physical visibility blind spots in the store.

---

### Session 2: Formatting Fieldwork Data & Core Inventory Logic
**Student:**
> "I just finished the physical audit with Rajinder uncle at his shop. We spent 30 minutes counting items across the front counter, deep freezer, and back racks. I have 25 items recorded with exact prices, remaining counts, daily sales, and printed expiry dates. For example, Tata Salt and Amul Butter are at 0 stock, Modern Bread expires in 4 days, and Everest Turmeric had a rat-nibbled corner on the bottom shelf. 
> Here is my raw data table from the notebook [provides 25 items]. 
> How should I write a Python script (`inventory.py`) to parse this CSV, calculate days of stock left, flag items near expiry, and suggest reorder quantities for his weekly distributor delivery?"

**AI Assistant:**
> - Structured `inventory.py` to parse `data.csv` using Python's standard `csv.DictReader`.
> - Implemented business calculations:
>   - Days of stock left: `current_stock / avg_daily_sales`.
>   - Reorder calculation: buffer for weekly distributor delivery cycle (7 days) minus current inventory.
>   - Expiry categorization: Critical (≤ 3 days) and Warning (4–14 days).
> - Added validation logic to catch corrupt/bad rows gracefully (e.g., empty fields or non-numeric values) so the script never crashes on malformed data.

---

### Session 3: Bilingual Web Dashboard & Restock Flow
**Student:**
> "Rajinder uncle is not comfortable reading English technical tables or complex software. I want a clean, high-contrast dashboard with Hindi and English labels ('स्टॉक खत्म', 'जल्द खराब होने वाला') that highlights urgent actions. Also, when new stock arrives, he should be able to update stock with one click. How should I build this with Flask?"

**AI Assistant:**
> - Designed a lightweight Flask app (`app.py`) with a self-contained HTML/CSS dashboard (`templates/index.html`) requiring no external CDN or cloud dependencies.
> - Built high-contrast visual alert cards for Out-of-Stock and Expiring items.
> - Added an interactive "+ Add Stock" form on every table row that updates `data.csv` directly when goods are delivered.
> - Included dynamic store controls to adjust warning thresholds without code modification.
> - Created `test_bad_row.py` to verify data parsing robustness against malformed input rows.
