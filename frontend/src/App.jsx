import { useState, useEffect, useCallback } from 'react';
import { getExpenses, createExpense } from './api';
import ExpenseForm from './components/ExpenseForm';
import ExpenseList from './components/ExpenseList';

function App() {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [serverError, setServerError] = useState(null);

  const fetchExpenses = useCallback(async () => {
    setLoading(true);
    setServerError(null);
    try {
      const data = await getExpenses();
      setExpenses(data);
    } catch (err) {
      console.error('Failed to fetch expenses:', err);
      setServerError(err.message || 'Unable to connect to backend server');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchExpenses();
  }, [fetchExpenses]);

  const handleExpenseAdded = async (newExpenseData) => {
    // Post to backend
    const createdExpense = await createExpense(newExpenseData);
    // Prepend to current list (newest first)
    setExpenses((prev) => [createdExpense, ...prev]);
    return createdExpense;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-white">
      {/* Top Navigation / Header */}
      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-20 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-slate-950 font-black text-xl shadow-lg shadow-emerald-500/20">
              ₹
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                SpendSense
                <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  Live &bull; Anomaly Engine
                </span>
              </h1>
              <p className="text-xs text-slate-400">Intelligent Expense Management & Anomaly Detection</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 text-xs px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800">
              <span
                className={`inline-block w-2.5 h-2.5 rounded-full ${
                  loading
                    ? 'bg-amber-400 animate-pulse'
                    : serverError
                    ? 'bg-rose-500'
                    : 'bg-emerald-400'
                }`}
              />
              <span className="text-slate-300 font-medium">
                {serverError ? 'Server Offline' : 'Backend Connected'}
              </span>
            </div>

            <button
              onClick={fetchExpenses}
              disabled={loading}
              title="Refresh expenses list from backend"
              className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition disabled:opacity-50"
            >
              ↻ Refresh
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto w-full px-6 py-8 flex-1 space-y-8">
        {serverError && (
          <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-800/80 text-rose-300 text-sm flex items-center justify-between shadow-lg">
            <div className="flex items-center gap-2">
              <span className="font-bold">Backend Connection Notice:</span>
              <span>{serverError}</span>
            </div>
            <button
              onClick={fetchExpenses}
              className="px-3 py-1 rounded bg-rose-900/60 hover:bg-rose-800 text-xs text-white border border-rose-700 font-semibold transition"
            >
              Retry
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Form */}
          <div className="lg:col-span-5">
            <ExpenseForm onExpenseAdded={handleExpenseAdded} />
          </div>

          {/* Right Column: Expense List */}
          <div className="lg:col-span-7">
            <ExpenseList expenses={expenses} isLoading={loading} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-4 px-6 text-center text-xs text-slate-500 bg-slate-950">
        SpendSense &bull; Personal Expense Management
      </footer>
    </div>
  );
}

export default App;
