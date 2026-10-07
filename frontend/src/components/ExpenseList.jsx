import React from 'react';
import AnomalyBadge from './AnomalyBadge';

const CATEGORY_COLORS = {
  Food: 'bg-amber-500/10 text-amber-300 border-amber-500/30',
  Transport: 'bg-sky-500/10 text-sky-300 border-sky-500/30',
  Shopping: 'bg-purple-500/10 text-purple-300 border-purple-500/30',
  Bills: 'bg-blue-500/10 text-blue-300 border-blue-500/30',
  Entertainment: 'bg-pink-500/10 text-pink-300 border-pink-500/30',
  Health: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30',
  Other: 'bg-slate-500/10 text-slate-300 border-slate-500/30',
};

const formatDate = (dateString) => {
  if (!dateString) return '—';
  try {
    const parts = dateString.split('-');
    if (parts.length === 3) {
      const year = parts[0];
      const month = parseInt(parts[1], 10) - 1;
      const day = parseInt(parts[2], 10);
      const d = new Date(year, month, day);
      return d.toLocaleDateString('en-IN', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });
    }
    return dateString;
  } catch {
    return dateString;
  }
};

export default function ExpenseList({ expenses = [], isLoading = false }) {
  const totalAmount = expenses.reduce((sum, item) => sum + (Number(item.amount) || 0), 0);

  return (
    <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 pb-4 border-b border-slate-700/60">
        <div>
          <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
            Expense History
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">Showing all recorded transactions, newest first</p>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-medium px-3 py-1 rounded-full bg-slate-900/90 text-slate-300 border border-slate-700">
            {expenses.length} {expenses.length === 1 ? 'transaction' : 'transactions'}
          </span>
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
            Total: ₹{totalAmount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </span>
        </div>
      </div>

      {isLoading ? (
        <div className="py-12 text-center">
          <div className="w-7 h-7 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-slate-400 text-sm">Loading expenses...</p>
        </div>
      ) : expenses.length === 0 ? (
        <div className="text-center py-12 border border-dashed border-slate-700/80 rounded-xl bg-slate-900/30">
          <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center mx-auto mb-3 text-slate-400 text-xl font-bold">
            ₹
          </div>
          <h3 className="text-slate-200 font-semibold text-sm">No expenses recorded yet</h3>
          <p className="text-slate-400 text-xs mt-1 max-w-sm mx-auto">
            Use the form above to add your first expense and start tracking your spending.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-700/60 text-xs text-slate-400 font-semibold uppercase tracking-wider">
                <th className="pb-3 pl-2">Category</th>
                <th className="pb-3">Merchant</th>
                <th className="pb-3">Date</th>
                <th className="pb-3">Note</th>
                <th className="pb-3 text-right pr-2">Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/40">
              {expenses.map((expense) => {
                const categoryClass =
                  CATEGORY_COLORS[expense.category] || CATEGORY_COLORS.Other;

                return (
                  <tr
                    key={expense.id}
                    className="hover:bg-slate-700/30 transition group"
                  >
                    <td className="py-3.5 pl-2 font-medium">
                      <div className="flex items-center gap-2">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${categoryClass}`}
                        >
                          {expense.category}
                        </span>
                        {expense.is_anomaly && (
                          <AnomalyBadge
                            level={
                              expense.z_score && expense.z_score > 3
                                ? 'High'
                                : 'Medium'
                            }
                          />
                        )}
                      </div>
                      {expense.is_anomaly && expense.anomaly_explanation && (
                        <p className="text-[11px] text-amber-300/90 mt-1 pl-1">
                          {expense.anomaly_explanation}
                        </p>
                      )}
                    </td>

                    <td className="py-3.5 text-slate-300 font-medium">
                      {expense.merchant || (
                        <span className="text-slate-500 italic">None</span>
                      )}
                    </td>

                    <td className="py-3.5 text-slate-400 text-xs whitespace-nowrap">
                      {formatDate(expense.date)}
                    </td>

                    <td className="py-3.5 text-slate-400 text-xs max-w-xs truncate">
                      {expense.note || (
                        <span className="text-slate-600">—</span>
                      )}
                    </td>

                    <td className="py-3.5 pr-2 text-right whitespace-nowrap">
                      <span className="font-bold text-white text-base tracking-tight">
                        ₹
                        {Number(expense.amount).toLocaleString('en-IN', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
