from datetime import date
from sqlalchemy import Boolean, Column, Date, Float, Integer, String
from database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    merchant = Column(String, nullable=True)
    note = Column(String, nullable=True)
    date = Column(Date, nullable=False, default=date.today)
    is_anomaly = Column(Boolean, default=False, nullable=False)
    anomaly_explanation = Column(String, nullable=True)
    z_score = Column(Float, nullable=True)
