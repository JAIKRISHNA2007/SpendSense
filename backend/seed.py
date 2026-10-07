import datetime
from database import SessionLocal, engine, Base
from models import Expense

def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing expenses to have a clean, consistent dataset
        db.query(Expense).delete()
        db.commit()

        today = datetime.date.today()

        sample_expenses = [
            # Food (Normal: ₹120 - ₹450)
            {
                "amount": 180.0,
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
                "amount": 220.0,
                "category": "Food",
                "merchant": "Subway",
                "note": "Veg sub combo",
                "date": today - datetime.timedelta(days=11),
            },
            {
                "amount": 150.0,
                "category": "Food",
                "merchant": "Cafe Coffee Day",
                "note": "Cappuccino",
                "date": today - datetime.timedelta(days=8),
            },
            {
                "amount": 420.0,
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

            # Transport (Normal: ₹80 - ₹350)
            {
                "amount": 90.0,
                "category": "Transport",
                "merchant": "Namma Metro",
                "note": "Smartcard monthly recharge",
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
            # Transport ANOMALY (Deliberately high: ₹3,400)
            {
                "amount": 3400.0,
                "category": "Transport",
                "merchant": "Outstation Cabs",
                "note": "Emergency late-night airport taxi ride",
                "date": today - datetime.timedelta(days=2),
            },

            # Shopping (Normal: ₹400 - ₹1,400)
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
            # Shopping ANOMALY (Deliberately high: ₹8,500 electronics - section 8 example)
            {
                "amount": 8500.0,
                "category": "Shopping",
                "merchant": "Croma Electronics",
                "note": "Noise-cancelling wireless headphones",
                "date": today - datetime.timedelta(days=3),
            },

            # Bills (Normal: ₹600 - ₹1,600)
            {
                "amount": 699.0,
                "category": "Bills",
                "merchant": "Airtel Fiber",
                "note": "Monthly broadband bill",
                "date": today - datetime.timedelta(days=14),
            },
            {
                "amount": 1200.0,
                "category": "Bills",
                "merchant": "BESCOM Electricity",
                "note": "Monthly residential electricity bill",
                "date": today - datetime.timedelta(days=7),
            },
            # Bills ANOMALY (Deliberately high: ₹9,200)
            {
                "amount": 9200.0,
                "category": "Bills",
                "merchant": "Urban Company Services",
                "note": "Dual AC annual compressor overhaul & gas recharge",
                "date": today - datetime.timedelta(days=1),
            },

            # Entertainment (Normal: ₹250 - ₹650)
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

            # Health (Normal: ₹200 - ₹750)
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

        for item in sample_expenses:
            expense = Expense(
                amount=item["amount"],
                category=item["category"],
                merchant=item["merchant"],
                note=item["note"],
                date=item["date"],
                is_anomaly=False,
                anomaly_explanation=None,
                z_score=None,
            )
            db.add(expense)

        db.commit()
        print(f"Successfully seeded {len(sample_expenses)} expenses into SQLite database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
