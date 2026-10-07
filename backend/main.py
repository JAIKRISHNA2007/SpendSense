import os
import datetime

from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import Session

from anomaly import detect_anomaly
from database import Base, engine, get_db
from models import Expense

# Allowed categories from project.md section 2 & 7
ALLOWED_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Other",
]

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpendSense API", version="0.1.0")

# Configure CORS
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
origins = [
    frontend_origin,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if frontend_origin == "*" else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be strictly greater than 0")
    category: str = Field(..., description="Category must be one of the predefined list")
    merchant: Optional[str] = None
    note: Optional[str] = None
    date: datetime.date = Field(default_factory=datetime.date.today)

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        clean_value = value.strip().title()
        # Check against allowed list
        matched = next((c for c in ALLOWED_CATEGORIES if c.lower() == clean_value.lower()), None)
        if not matched:
            raise ValueError(f"Category '{value}' is invalid. Allowed: {', '.join(ALLOWED_CATEGORIES)}")
        return matched

    @field_validator("merchant", "note")
    @classmethod
    def clean_optional_strings(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        trimmed = value.strip()
        return trimmed if trimmed else None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: float
    category: str
    merchant: Optional[str] = None
    note: Optional[str] = None
    date: datetime.date
    is_anomaly: bool
    anomaly_explanation: Optional[str] = None
    z_score: Optional[float] = None


@app.get("/")
def read_root():
    return {"message": "SpendSense API is running", "categories": ALLOWED_CATEGORIES}


@app.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    # Newest first by date and id
    expenses = db.query(Expense).order_by(Expense.date.desc(), Expense.id.desc()).all()
    return expenses


@app.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate, db: Session = Depends(get_db)):
    # Fetch historical expenses for this category to pass to anomaly detection
    historical = db.query(Expense).filter(Expense.category == expense_in.category).all()
    
    # Compute anomaly stats
    anomaly_result = detect_anomaly(
        expense_amount=expense_in.amount,
        category=expense_in.category,
        historical_expenses=historical,
    )

    db_expense = Expense(
        amount=round(expense_in.amount, 2),
        category=expense_in.category,
        merchant=expense_in.merchant,
        note=expense_in.note,
        date=expense_in.date,
        is_anomaly=anomaly_result.get("is_anomaly", False),
        anomaly_explanation=anomaly_result.get("anomaly_explanation"),
        z_score=anomaly_result.get("z_score"),
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/analytics/anomalies", response_model=List[ExpenseResponse])
def get_anomalies(db: Session = Depends(get_db)):
    """
    Returns list of all flagged anomaly expenses, newest first.
    """
    anomalies = (
        db.query(Expense)
        .filter(Expense.is_anomaly == True)
        .order_by(Expense.date.desc(), Expense.id.desc())
        .all()
    )
    return anomalies

