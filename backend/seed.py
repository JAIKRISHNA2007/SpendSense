import datetime
from anomaly import detect_anomaly
from database import Base, SessionLocal, engine
from models import Expense


def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Clear existing expenses to ensure a fresh, consistent dataset
        db.query(Expense).delete()
        db.commit()

        today = datetime.date.today()

        sample_expenses = [
            # Food (Normal baseline: ₹180 - ₹340)
            {
                "amount": 220.0,
                "category": "Food",
                "merchant": "Chai Point",
                "note": "Snacks & ginger tea with colleagues",
                "date": today - datetime.timedelta(days=16),
            },
            {
                "amount": 340.0,
                "category": "Food",
                "merchant": "Swiggy",
                "note": "Biryani lunch order",
                "date": today - datetime.timedelta(days=14),
            },
            {
                "amount": 240.0,
                "category": "Food",
                "merchant": "Subway",
                "note": "Veg sub combo",
                "date": today - datetime.timedelta(days=11),
            },
            {
                "amount": 190.0,
                "category": "Food",
                "merchant": "Cafe Coffee Day",
                "note": "Cappuccino",
                "date": today - datetime.timedelta(days=8),
            },
            {
                "amount": 310.0,
                "category": "Food",
                "merchant": "Zomato",
                "note": "Dinner pizza delivery",
                "date": today - datetime.timedelta(days=4),
            },
            {
                "amount": 260.0,
                "category": "Food",
                "merchant": "Haldiram's",
                "note": "Quick lunch",
                "date": today - datetime.timedelta(days=1),
            },

            # Transport (Normal: ₹90 - ₹260, Deliberate Anomaly: ₹3,400)
            {
                "amount": 90.0,
                "category": "Transport",
                "merchant": "Namma Metro",
                "note": "Smartcard recharge",
                "date": today - datetime.timedelta(days=15),
            },
            {
                "amount": 140.0,
                "category": "Transport",
                "merchant": "Uber Auto",
                "note": "Ride to metro station",
                "date": today - datetime.timedelta(days=12),
            },
            {
                "amount": 260.0,
                "category": "Transport",
                "merchant": "Ola Cab",
                "note": "Ride to client meeting",
                "date": today - datetime.timedelta(days=9),
            },
            {
                "amount": 180.0,
                "category": "Transport",
                "merchant": "Rapido",
                "note": "Commute home during peak rain",
                "date": today - datetime.timedelta(days=5),
            },
            {
                "amount": 3400.0,
                "category": "Transport",
                "merchant": "Outstation Cabs",
                "note": "Emergency late-night airport taxi ride",
                "date": today - datetime.timedelta(days=2),
            },

            # Shopping (Normal: ₹550 - ₹1,250, Deliberate Anomaly: ₹8,500)
            {
                "amount": 550.0,
                "category": "Shopping",
                "merchant": "Decathlon",
                "note": "Running socks & water bottle",
                "date": today - datetime.timedelta(days=13),
            },
            {
                "amount": 899.0,
                "category": "Shopping",
                "merchant": "Myntra",
                "note": "Cotton casual shirt",
                "date": today - datetime.timedelta(days=10),
            },
            {
                "amount": 1250.0,
                "category": "Shopping",
                "merchant": "Amazon",
                "note": "Ergonomic laptop stand",
                "date": today - datetime.timedelta(days=6),
            },
            {
                "amount": 8500.0,
                "category": "Shopping",
                "merchant": "Croma Electronics",
                "note": "Noise-cancelling wireless headphones",
                "date": today - datetime.timedelta(days=3),
            },

            # Bills (Normal: ₹699 - ₹1,200, Deliberate Anomaly: ₹9,200)
            {
                "amount": 699.0,
                "category": "Bills",
                "merchant": "Airtel Fiber",
                "note": "Monthly broadband bill",
                "date": today - datetime.timedelta(days=16),
            },
            {
                "amount": 1200.0,
                "category": "Bills",
                "merchant": "BESCOM Electricity",
                "note": "Monthly residential electricity bill",
                "date": today - datetime.timedelta(days=10),
            },
            {
                "amount": 950.0,
                "category": "Bills",
                "merchant": "Indane Gas",
                "note": "LPG cylinder refill",
                "date": today - datetime.timedelta(days=6),
            },
            {
                "amount": 9200.0,
                "category": "Bills",
                "merchant": "Urban Company Services",
                "note": "Dual AC annual compressor overhaul & gas recharge",
                "date": today - datetime.timedelta(days=1),
            },

            # Entertainment (Normal: ₹320 - ₹499)
            {
                "amount": 320.0,
                "category": "Entertainment",
                "merchant": "BookMyShow",
                "note": "Weekend movie ticket",
                "date": today - datetime.timedelta(days=12),
            },
            {
                "amount": 499.0,
                "category": "Entertainment",
                "merchant": "Steam Games",
                "note": "Indie game discount sale",
                "date": today - datetime.timedelta(days=7),
            },

            # Health (Normal: ₹350 - ₹600)
            {
                "amount": 350.0,
                "category": "Health",
                "merchant": "Apollo Pharmacy",
                "note": "Multivitamins & basic first aid kit",
                "date": today - datetime.timedelta(days=10),
            },
            {
                "amount": 600.0,
                "category": "Health",
                "merchant": "Practo Clinic",
                "note": "Routine dental consultation checkup",
                "date": today - datetime.timedelta(days=5),
            },

            # Other
            {
                "amount": 250.0,
                "category": "Other",
                "merchant": "Local Print Shop",
                "note": "Document spiral binding & photocopies",
                "date": today - datetime.timedelta(days=3),
            },
        ]

        # Sort chronologically (oldest first) so that prior expenses form the baseline
        sample_expenses.sort(key=lambda x: x["date"])

        flagged_count = 0
        for item in sample_expenses:
            # Query prior expenses already inserted for this category
            prior_category_expenses = (
                db.query(Expense)
                .filter(Expense.category == item["category"])
                .all()
            )

            # Compute anomaly status using anomaly detection logic
            anomaly_data = detect_anomaly(
                expense_amount=item["amount"],
                category=item["category"],
                historical_expenses=prior_category_expenses,
            )

            if anomaly_data.get("is_anomaly"):
                flagged_count += 1

            expense = Expense(
                amount=item["amount"],
                category=item["category"],
                merchant=item["merchant"],
                note=item["note"],
                date=item["date"],
                is_anomaly=anomaly_data.get("is_anomaly", False),
                anomaly_explanation=anomaly_data.get("anomaly_explanation"),
                z_score=anomaly_data.get("z_score"),
            )
            db.add(expense)
            db.commit()

        print(
            f"Successfully seeded {len(sample_expenses)} expenses into SQLite database "
            f"({flagged_count} flagged as deliberate anomalies)."
        )
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
