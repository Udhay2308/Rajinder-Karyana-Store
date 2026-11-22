# Kirana Stockout & Expiry Early-Warning System

**Target Person:** Rajinder Kumar (Sole Proprietor)  
**Shop Name:** Rajinder Karyana Store  
**Location:** Main Village Road (Rural/Semi-urban Village Store)  
**Date of Fieldwork:** November 22, 2024  
**Project Goal:** Eliminate unexpected stockouts of daily essentials and prevent inventory write-offs caused by distributor bulk-scheme expiration traps.

---

## 🎥 3-Minute Video Walkthrough
- **Screen Recording:** [Watch 3-minute Demo Walkthrough Video](https://youtu.be/placeholder-demo-rajinder-kirana) *(Replace with your unlisted YouTube or Google Drive video link)*

---

## 1. The Core Problem & Context
Rajinder Kumar has run a small, 120 sq ft village grocery store for 14 years. He relies purely on cash/local UPI, paper chits for distributor orders, and his own visual memory. He faces two persistent financial leaks:
1. **Sudden Out-of-Stock Disasters:** Fast-moving staples (like Tata Salt and Amul Butter) run out without warning because they are kept in blind spots (deep freezer or floor crates). When customers can't get basic items, they walk to a competing shop, causing permanent customer churn.
2. **Expired Inventory Loss:** Wholesale distributors visit once a week and offer bulk margin discounts (e.g., extra discount on full cartons of sliced bread or namkeen). Rajinder buys them, but village families prefer homemade roti, causing bread packs to sit on back shelves and expire unsold. Over 10% of his shop capital (₹1,045+ out of ₹10,191) was found locked in items expiring within days!

Existing tools like Khatabook or Vyapar failed him because they require heavy English typing, cloud account setup, and focus on GST billing rather than physical shelf-monitoring.

---

## 2. The One Useful Output
The tool produces a single, high-contrast **Daily Morning Action Sheet (दैनिक एक्शन शीट)**:
* **Section 1 (Red Alert - Restock Now):** Items at 0 units (e.g. Tata Salt, Amul Butter) with exact reorder quantities calculated for the weekly distributor cycle.
* **Section 2 (Amber Alert - Push to Front / Do Not Reorder):** Packaged items within 14 days of expiry (e.g. Modern Bread with 4 days left, Haldiram Bhujia with 12 days left) so Rajinder can move them to the front glass counter and reject distributor bulk schemes.
* **Quick Restock Updater:** A 1-click restock box allowing Rajinder to add incoming quantities when the delivery van arrives, persisting updates directly to `data.csv`.

---

## 3. How to Run the Tool

### Prerequisites
- Python 3.9+ (Standard Python library with Flask).
- No external internet or cloud account needed (runs 100% locally).

### Option A: Launch Interactive Bilingual Web Dashboard
```bash
python app.py
```
Open your browser at: **`http://127.0.0.1:5000`**

### Option B: Run Quick CLI Report (Terminal Only)
```bash
python inventory.py
```

### Option C: Run Crash-Proof Bad-Row Tolerance Test
```bash
python test_bad_row.py
```

---

## 4. Real Output Example (CLI Terminal Execution)

```text
==============================================================================
 🏪 RAJINDER KARYANA STORE - DAILY MORNING ACTION SHEET
 Reference Date: 2024-11-22 | Total Audited Items: 25
 Total Shop Inventory Value: ₹10,191.30
 Inventory Capital at Expiry Risk: ₹1,045.50
==============================================================================

🔴 1. IMMEDIATE RESTOCK REQUIRED (OUT OF STOCK - 0 Units)
------------------------------------------------------------------------------
  ❌ Tata Salt                    | Pack: 1kg      | Daily Sale:  2.9/day
     Order NOW: 25 units | Shelf: Middle Rack | Notes: OUT OF STOCK - distributor delivery delayed
  ❌ Amul Butter                  | Pack: 100g     | Daily Sale:  1.9/day
     Order NOW: 16 units | Shelf: Deep Freezer | Notes: OUT OF STOCK - sold out on Thursday

🟠 2. RESTOCK BEFORE DISTRIBUTOR VISIT (Stock Low or < 2 Days Left)
------------------------------------------------------------------------------
  ⚠️  Parle-G Gold                 | Stock:  7 left | Lasts ~1.7 days
     Order: 29 units | Threshold: 5 | Shelf: Front Glass Counter
  ⚠️  Amul Taaza Milk              | Stock:  3 left | Lasts ~0.5 days
     Order: 52 units | Threshold: 4 | Shelf: Deep Freezer
  ⚠️  Modern Sandwich Bread        | Stock:  9 left | Lasts ~1.8 days
     Order: 34 units | Threshold: 4 | Shelf: Back Shelf
  ⚠️  Patanjali Dant Kanti         | Stock:  2 left | Lasts ~5.0 days
     Order: 2 units | Threshold: 3 | Shelf: Side Rack

🛑 3. EXPIRING SOON - SELL TODAY OR RETURN TO DISTRIBUTOR
------------------------------------------------------------------------------
  CRITICAL (Expires in <= 3 Days):
  🚨 Amul Taaza Milk              | Stock:  3 | Expires in: 3 DAYS (2024-11-25)
     Location: Deep Freezer | Value at Risk: ₹76.5 | Expires in 3 days

  WARNING (Expires in 4 to 14 Days - Move to Front Counter):
  ⚠️  Modern Sandwich Bread        | Stock:  9 | Expires in: 4 days (2024-11-26)
     Location: Back Shelf | Action: Do NOT take distributor bulk scheme!
  ⚠️  Haldiram Aloo Bhujia         | Stock: 11 | Expires in: 12 days (2024-12-04)
     Location: Back Shelf | Action: Do NOT take distributor bulk scheme!
  ⚠️  Mother Dairy Dahi            | Stock:  6 | Expires in: 10 days (2024-12-02)
     Location: Deep Freezer | Action: Do NOT take distributor bulk scheme!
==============================================================================
 Actionable Insight: Rajinder uncle should order 5 items on next distributor visit
 and inspect the back shelf for Modern Bread & Haldiram Bhujia immediately.
==============================================================================
```

---

## 5. What the Tool Gets Wrong (Limitations & Edge Cases)

Every honest tool has clear boundaries. This tool **must NOT be trusted for**:
1. **Loose, Unpackaged Grains and Pulses:** The store sells open sacks of loose rice, loose sugar, and loose chana dal. These do not have batch expiry dates printed on them. Their freshness is judged purely by human visual and olfactory inspection (weevils, dampness), which this tool cannot measure.
2. **Seasonal Festival Spikes:** Daily sales rates (`avg_daily_sales`) assume normal daily village consumption. It will underestimate demand during Diwali, Eid, or local village wedding weeks when ghee, sugar, and milk sales spike 5x overnight.
3. **Distributor Minimum Order Quantities (MOQ):** The tool calculates exact optimal replenishment (e.g. order 16 packs of butter), but distributors only sell full master cartons (e.g., box of 30). Rajinder must still manually round to the distributor's minimum carton size.
4. **Physical Rodent / Leak Damage:** The tool tracks inventory numbers digitally. It cannot know if a rat nibbled the corner of an Everest Turmeric packet (`ITM014`) on the bottom shelf unless physically audited.

---

## 6. Verification & Automated Testing

The project includes automated validation to ensure the tool runs reliably in a real shop environment:

### Error Resilience Test
Run the test suite to verify that corrupt data rows (invalid numbers, missing fields, or incorrect date formats) are caught and reported without crashing the application:
```bash
python test_bad_row.py
```

### Configurable Parameters
All business thresholds (expiry alert horizons, stockout risk days, and weekly delivery cycles) are dynamic. They can be updated either in `inventory.py` or directly through the web interface controls, allowing the tool to adapt if distributor visit schedules change.

---

## 7. Project Structure
```text
├── research.md            # Step 1: 5-line problem statement, 2 failed solutions, 2 read sources
├── fieldwork.md           # Step 2: 30-min shop visit notes, 3 quotes, 1 big surprise, methodology
├── data.csv               # Raw data: 25 authentic rows with non-round counts and edge cases
├── inventory.py           # Core computation, restock forecasting & crash-proof parser
├── app.py                 # Flask web dashboard with live threshold adjuster and restock form
├── test_bad_row.py        # Crash-proof validation script for bad rows
├── bad_sample_data.csv    # Corrupted test dataset (strings in numbers, negative prices, bad dates)
├── reflection.md          # Step 4: Personal reflection on fieldwork, scope cuts, and AI usage
├── ai-chats/              # Exported AI prompt history and architecture deliberations
│   └── chat_history.md
├── assets/                # Fieldwork photographic evidence
│   └── README.txt
└── README.md              # Project overview, real outputs, architecture & limitations
```

