# SpendSense — Intelligent Expense Management & Anomaly Detection

**Scope note:** This spec is deliberately cut down for a 2-hour vibe-coding hackathon. Build exactly what's here, in order. Nothing else, until it all works.

## 1. Overview
- **One-line:** A personal expense tracker that flags unusual spending and explains *why* it's unusual, in plain English.
- **Problem:** People track expenses but don't notice unusual spending until it's a problem. Most trackers show totals, not insight.
- **Target user:** A student or young professional managing personal expenses.
- **Key differentiator:** Explainable anomaly detection — not just "this is weird," but "this is weird *because* X," using simple, transparent statistics (no black-box ML).
- **Non-goals (do not build):** multi-user accounts, login/auth, bank sync, receipt OCR, mobile app, budgets/goals. All out of scope for 2 hours.

## 2. MVP — exactly 3 features

### Feature 1: Add & View Expenses
- **Flow:** User fills a form (amount, category, merchant, date, note) → saved → appears in a list, newest first.
- **Categories (fixed list):** Food, Transport, Shopping, Bills, Entertainment, Health, Other.
- **Acceptance:** Can add an expense and see it immediately in the list and in the dashboard totals.

### Feature 2: Dashboard & Analytics
- **Flow:** On load, show total spend, spend-by-category (bar or pie chart), and spend-over-time (line chart).
- **Data:** Computed from all stored expenses.
- **Acceptance:** Adding a new expense updates the charts without a page reload if possible (otherwise on refresh).

### Feature 3: Explainable Anomaly Detection
- **Logic (statistical, not ML-model-based — fast and explainable):**
  1. For each category, compute mean and standard deviation of past expense amounts (need ≥3 prior expenses in that category to evaluate; otherwise skip — "cold start").
  2. For a new expense, compute `z = (amount - mean) / std`.
  3. Flag as anomaly if `z > 2` (unusually high) — also flag if amount is more than `3×` the category average, whichever is simpler to implement first.
  4. **Risk levels:** `z 2–3` = Medium, `z > 3` = High.
- **Explanation template (generate this string, show it in the UI):**
  > "₹{amount} on {category} is unusual — that's {ratio}× your usual {category} spend of ₹{mean}."
- **Acceptance:** Adding an expense that's far above a category's average shows a visible flag + the explanation sentence next to that expense.

## 3. Tech stack (decided — do not deviate)
- **Frontend:** React + Vite + Tailwind CSS — fast to scaffold, looks clean fast.
- **Backend:** FastAPI (Python) — pairs naturally with the stats/anomaly logic (pandas/numpy).
- **Database:** SQLite via SQLAlchemy — zero setup, file-based, good enough for a demo.
- **Charts:** Recharts (frontend).
- **Auth:** None. Single implicit user. (Saves 30+ minutes — do not add this.)
- **Deployment:** Frontend → Vercel. Backend → Render free tier (or just run locally and demo from laptop if deploy time runs out — a working local demo beats a broken deployed one).

## 4. Data model (SQLite)
```
Expense
- id: integer, primary key, autoincrement
- amount: float, not null
- category: string, not null
- merchant: string, nullable
- note: string, nullable
- date: date, not null, default = today
- is_anomaly: boolean, default false
- anomaly_explanation: string, nullable
- z_score: float, nullable
```
No other tables needed for the MVP.

## 5. API endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | /expenses | list all expenses, newest first |
| POST | /expenses | add a new expense; server computes anomaly fields before saving |
| GET | /analytics/summary | total spend, spend by category, spend over time |
| GET | /analytics/anomalies | list of flagged expenses |

Keep request/response bodies simple JSON. No pagination needed for a demo dataset.

## 6. Project structure
```
/backend
  main.py          # FastAPI app, routes
  models.py        # SQLAlchemy models
  anomaly.py       # mean/std + z-score logic + explanation string builder
  database.py      # SQLite setup
/frontend
  src/
    App.jsx
    components/
      ExpenseForm.jsx
      ExpenseList.jsx
      Dashboard.jsx
      AnomalyBadge.jsx
    api.js         # fetch calls to backend
project.md
README.md
.env.example
```

## 7. Security (minimum viable, still do these)
- Validate all inputs server-side (amount > 0, category in allowed list, date is valid).
- No secrets or API keys in code — use `.env`, add `.env` to `.gitignore`.
- Enable CORS only for your frontend's origin.
- Sanitize/escape any text shown in the UI (React does this by default — don't use `dangerouslySetInnerHTML`).
- No sensitive data logged to console in production build.

## 8. Seed data (do this early!)
Before building anomaly detection, seed ~15–20 sample expenses with realistic category patterns (e.g. Food ₹150–400 range) PLUS 2–3 deliberately unusual ones (e.g. one ₹8,500 "Electronics-like" Shopping entry). This lets you demo anomaly detection immediately without manually typing 20 entries live.

## 9. Build order (follow this exactly)
1. Scaffold backend (FastAPI + SQLite + Expense model). Verify with one manual POST/GET.
2. Scaffold frontend (Vite + Tailwind). Verify it talks to backend (fetch /expenses).
3. Build ExpenseForm + ExpenseList — Feature 1 fully working.
4. Add seed data script, run it.
5. Build Dashboard with charts — Feature 2 fully working.
6. Build anomaly.py (z-score + explanation) — wire into POST /expenses — Feature 3 fully working.
7. Polish UI: empty states, loading states, anomaly badges (red/orange), clean header.
8. Deploy (or prep local demo). Write 5-line README.

## 10. Definition of Done
- [ ] Can add an expense and see it in the list instantly
- [ ] Dashboard shows accurate totals and charts that update with new data
- [ ] A clearly unusual expense gets flagged with a human-readable explanation
- [ ] No crashes on empty form submit, negative amount, or missing category
- [ ] No secrets in the repo
- [ ] App is either deployed with a live link, or runs cleanly with one command for a local demo
- [ ] README has: what it does, how to run it, one screenshot
