import React, { useState } from 'react';

const CATEGORIES = [
  'Food',
  'Transport',
  'Shopping',
  'Bills',
  'Entertainment',
  'Health',
  'Other',
];

const getTodayString = () => new Date().toISOString().split('T')[0];

export default function ExpenseForm({ onExpenseAdded }) {
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('Food');
  const [merchant, setMerchant] = useState('');
  const [note, setNote] = useState('');
  const [date, setDate] = useState(getTodayString());
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError(null);
    setSuccessMessage(null);

    const parsedAmount = parseFloat(amount);
    if (isNaN(parsedAmount) || parsedAmount <= 0) {
      setFormError('Please enter a valid amount greater than 0.');
      return;
    }

    if (!category || !CATEGORIES.includes(category)) {
      setFormError('Please select a valid category.');
      return;
    }

    if (!date) {
      setFormError('Please select a valid date.');
      return;
    }

    setIsSubmitting(true);
    try {
      await onExpenseAdded({
        amount: parsedAmount,
        category,
        merchant: merchant.trim() || null,
        note: note.trim() || null,
        date,
      });

      // Reset form
      setAmount('');
      setMerchant('');
      setNote('');
      setDate(getTodayString());
      setSuccessMessage('Expense added successfully!');
      setTimeout(() => setSuccessMessage(null), 3500);
    } catch (err) {
      setFormError(err.message || 'Failed to save expense. Please check input values.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            Add Expense
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">Record a new transaction with category and details</p>
        </div>
      </div>

      {formError && (
        <div className="mb-4 p-3 rounded-lg bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-start gap-2">
          <span className="font-bold">Error:</span>
          <span>{formError}</span>
        </div>
      )}

      {successMessage && (
        <div className="mb-4 p-3 rounded-lg bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 text-xs flex items-start gap-2">
          <span className="font-bold">Success:</span>
          <span>{successMessage}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Amount & Category in Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label htmlFor="expense-amount" className="block text-xs font-semibold text-slate-300 mb-1">
              Amount (₹) <span className="text-rose-400">*</span>
            </label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400 font-semibold text-sm">
                ₹
              </span>
              <input
                id="expense-amount"
                type="number"
                step="0.01"
                min="0.01"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
                className="w-full pl-8 pr-3 py-2 bg-slate-900/90 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition"
              />
            </div>
          </div>

          <div>
            <label htmlFor="expense-category" className="block text-xs font-semibold text-slate-300 mb-1">
              Category <span className="text-rose-400">*</span>
            </label>
            <select
              id="expense-category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2 bg-slate-900/90 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition"
            >
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Merchant & Date in Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label htmlFor="expense-merchant" className="block text-xs font-semibold text-slate-300 mb-1">
              Merchant / Payee
            </label>
            <input
              id="expense-merchant"
              type="text"
              placeholder="e.g. Swiggy, Uber, Amazon"
              value={merchant}
              onChange={(e) => setMerchant(e.target.value)}
              className="w-full px-3 py-2 bg-slate-900/90 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition"
            />
          </div>

          <div>
            <label htmlFor="expense-date" className="block text-xs font-semibold text-slate-300 mb-1">
              Date <span className="text-rose-400">*</span>
            </label>
            <input
              id="expense-date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
              className="w-full px-3 py-2 bg-slate-900/90 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition"
            />
          </div>
        </div>

        {/* Note */}
        <div>
          <label htmlFor="expense-note" className="block text-xs font-semibold text-slate-300 mb-1">
            Note / Description
          </label>
          <input
            id="expense-note"
            type="text"
            placeholder="e.g. Team dinner, weekly groceries"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            className="w-full px-3 py-2 bg-slate-900/90 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition"
          />
        </div>

        {/* Submit Button */}
        <button
          id="submit-expense-btn"
          type="submit"
          disabled={isSubmitting}
          className="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm rounded-lg shadow-md hover:shadow-emerald-600/30 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isSubmitting ? (
            <>
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Saving Expense...
            </>
          ) : (
            'Add Expense'
          )}
        </button>
      </form>
    </div>
  );
}
