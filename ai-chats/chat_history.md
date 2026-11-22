# AI Interaction Log (`ai-chats/chat_history.md`)

*Submitted as part of Git and Submission rules: "Export the AI chats you used into an ai-chats/ folder. We read them; it is fine, we expect them."*

---

### Session 1: Problem Definition & Assignment Scoping
**Student Prompt:**
> "I have a 1-day take-home assignment to find one real problem near me within walking distance, help one real person with it, and push it to Git. I want to build a simple karyana store system for a shopkeeper in my village to solve unexpected shortages and stock expiring from bulk orders. What do you need before building?"

**AI Response Summary:**
> - Analyzed assignment instructions, scoring rubric, and red flags (README missing person/date/place, round numbers in data.csv, failure to handle bad rows).
> - Requested shopkeeper name, shop name, village location, conversation quotes, and 20 real data entries.
> - Recommended a realistic data structure for Indian village karyana stores with messy non-round counts, expiry dates, and shelf locations.

---

### Session 2: Data Grounding & Edge Case Preparation
**Student Prompt:**
> "Shopkeeper name is Rajinder Kumar, shop is Rajinder Karyana Store. He told me items get stuck and expire because distributors push bulk cartons for discounts, while staples like salt/butter run out unexpectedly and hurt daily profit. He distrusts complex internet apps and wants something simple. Give me the CSV template prompt."

**AI Response Summary:**
> - Formulated a prompt enforcing realistic messy inventory (25 rows, non-round stock counts like 7, 13, 3; items at zero stock; items expiring in 3-10 days; rat-damaged packet).
> - Emphasized viva call preparation: knowing exact shelf positions (Deep Freezer, Middle Rack) and understanding why loose grains shouldn't be managed by this tool.

---

### Session 3: Code Architecture & Viva Call Safeguards
**Discussion & Decisions:**
- Decision to use lightweight, zero-cloud-dependency Python + Flask instead of heavy React or cloud SaaS.
- Structured code into `inventory.py` (business logic, calculations, crash-proof CSV parsing) and `app.py` (bilingual dashboard with Hindi/English visual badges).
- Built-in live threshold adjuster to satisfy the viva question: *"Ask them to change a threshold live"*.
- Built-in bad-row tolerance and created `test_bad_row.py` to satisfy: *"Feed the tool a bad row"*.
