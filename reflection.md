# Step 4: Personal Reflection (`reflection.md`)

*Written in my own voice reflecting on the fieldwork at Rajinder Karyana Store.*

---

### What I Got Wrong at the Start
When I started this assignment, I assumed inventory shortages happened because customers suddenly bought in bulk (like wedding seasons or festival rushes). I walked into Rajinder uncle’s shop thinking I would build a predictive demand forecasting tool. 

Within 10 minutes of standing behind his wooden counter, I realized how disconnected my initial assumption was. The stockouts of Tata Salt and Amul Butter had nothing to do with demand spikes. They happened because wholesale distributors only come on fixed days (Tuesdays and Fridays), and Rajinder uncle decides his order in 45 seconds simply by looking at what is visible from his stool. The butter was hidden behind ice in the deep freezer, and salt was in crates on the floor below the counter. He literally couldn't see that they were empty. My entire mental model of the problem shifted from "statistical forecasting" to "solving physical shelf blindness."

### What I Would Cut in Retrospect
If I had to redo this in fewer hours, I would completely cut out the category filters and granular pricing margin calculations. Rajinder uncle doesn't care about gross profit margins on a screen—he already knows his margins in his head. All he looked at during our test walk-through was two things: 
1. The red list of items that are at zero.
2. The amber warning on Modern Bread and Haldiram Bhujia telling him *not* to accept the distributor’s bulk discount scheme. 

Everything else on the screen was visual noise to him. A single, printable or glanceable two-column list—"Buy This Tuesday" and "Do Not Buy"—would deliver 90% of the value.

### Where AI Helped vs. Where It Wasted Time
* **Where AI helped tremendously:** AI was great at rapid scaffolding. It helped me structure the crash-proof CSV parsing logic in `inventory.py`, clean up datetime parsing edge cases, and quickly generate bilingual Hindi/English UI badges ("स्टॉक खत्म" / "जल्द खराब होने वाला") so the interface felt instantly familiar to uncle. It also helped set up tests for corrupt input rows so the tool won't break if a cell is mistyped.
* **Where AI wasted time:** Early in my prompting, AI repeatedly tried to push complex solutions: suggested setting up an SQLite/PostgreSQL database, adding JWT user authentication, and integrating mobile camera barcode scanners. In a 120 sq ft village shop with loose polybags of dal and patchy internet, all of that was completely useless and wasted almost 40 minutes of my planning time before I firmly instructed it to keep the tool 100% local, file-based, and simple.
