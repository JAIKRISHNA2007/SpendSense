# SpendSense

Intelligent Expense Management & Anomaly Detection system built for hackathons and rapid expense insight.

## Project Structure (Section 6)

```text
/backend
  main.py          # FastAPI app, routes
  models.py        # SQLAlchemy models (Expense model)
  anomaly.py       # mean/std + z-score logic + explanation builder
  database.py      # SQLite setup
/frontend
  src/
    App.jsx        # Main React component & status verification
    components/
      ExpenseForm.jsx
      ExpenseList.jsx
      Dashboard.jsx
      AnomalyBadge.jsx
    api.js         # API client for backend communication
project.md
README.md
.env.example
.gitignore
```

## Setup & Running the Servers

### 1. Backend (FastAPI + SQLite)

From the project root:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Windows (Command Prompt):
.\venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

The backend API will be running at:
- **Base URL:** http://localhost:8000
- **Expenses Endpoint:** http://localhost:8000/expenses
- **Interactive Docs:** http://localhost:8000/docs

---

### 2. Frontend (Vite + React + Tailwind CSS)

From the project root:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start Vite development server
npm run dev
```

The frontend will be running at:
- **Local URL:** http://localhost:5173

---

## Verifying Frontend-Backend Communication

1. Open `http://localhost:5173` in your browser.
2. The header badge will display **Backend Connected**.
3. The page automatically calls `GET /expenses` and displays:
   > `Successfully fetched 0 expense(s) from GET /expenses`
4. Click **Test GET /expenses** to re-trigger the call and verify live API communication.
