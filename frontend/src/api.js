const API_BASE = import.meta.env.VITE_API_URL || 'https://spendsense-1js4.onrender.com';

export async function getExpenses() {
  const response = await fetch(`${API_BASE}/expenses`);
  if (!response.ok) {
    throw new Error(`Failed to fetch expenses: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export async function createExpense(expenseData) {
  const response = await fetch(`${API_BASE}/expenses`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(expenseData),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to create expense: ${response.status}`);
  }
  return response.json();
}

export async function getAnalyticsSummary() {
  const response = await fetch(`${API_BASE}/analytics/summary`);
  if (!response.ok) {
    throw new Error(`Failed to fetch analytics summary: ${response.status}`);
  }
  return response.json();
}

export async function getAnomalies() {
  const response = await fetch(`${API_BASE}/analytics/anomalies`);
  if (!response.ok) {
    throw new Error(`Failed to fetch anomalies: ${response.status}`);
  }
  return response.json();
}
