import math
from typing import Any, Dict, List, Optional


def detect_anomaly(
    expense_amount: float,
    category: str,
    historical_expenses: List[Any],
) -> Dict[str, Optional[Any]]:
    """
    Statistical anomaly detection based on z-score and ratio against historical category spend.
    - Requires at least 3 historical expenses in the category (cold start check).
    - Flagged if z_score > 2.0 or amount > 3.0 * mean.
    - Risk levels: Medium (z 2-3), High (z > 3).
    - Explanation template:
      '₹{amount} on {category} is unusual — that's {ratio}× your usual {category} spend of ₹{mean}.'
    """
    # Extract amounts from historical records
    amounts = []
    for exp in historical_expenses:
        if isinstance(exp, dict):
            val = exp.get("amount")
        else:
            val = getattr(exp, "amount", None)
        if val is not None and float(val) > 0:
            amounts.append(float(val))

    # Need >= 3 prior expenses in that category to evaluate; otherwise skip ("cold start")
    if len(amounts) < 3:
        return {
            "is_anomaly": False,
            "anomaly_explanation": None,
            "z_score": None,
        }

    n = len(amounts)
    mean = sum(amounts) / n
    variance = sum((x - mean) ** 2 for x in amounts) / n
    std = math.sqrt(variance)

    # Calculate z-score
    if std > 0:
        z_score = (expense_amount - mean) / std
    else:
        z_score = 0.0

    ratio = expense_amount / mean if mean > 0 else 1.0

    # Flag as anomaly if z > 2 or amount is more than 3x the category average
    is_anomaly = bool((z_score > 2.0) or (ratio >= 3.0))

    if not is_anomaly:
        return {
            "is_anomaly": False,
            "anomaly_explanation": None,
            "z_score": round(z_score, 2) if z_score > 0 else None,
        }

    # Format numbers for clean human-readable explanation
    # e.g. "₹8,500 on Shopping is unusual — that's 9.4× your usual Shopping spend of ₹900."
    formatted_amount = f"₹{expense_amount:,.2f}".replace(".00", "")
    formatted_mean = f"₹{mean:,.2f}".replace(".00", "")
    formatted_ratio = f"{ratio:.1f}"

    explanation = (
        f"{formatted_amount} on {category} is unusual — that's {formatted_ratio}× "
        f"your usual {category} spend of {formatted_mean}."
    )

    return {
        "is_anomaly": True,
        "anomaly_explanation": explanation,
        "z_score": round(z_score, 2),
    }
