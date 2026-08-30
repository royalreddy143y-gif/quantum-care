from app.core.config import settings
from app.database.session import SessionLocal, engine, Base
import app.models
from app.models.user import User
from app.models.patient import Patient
from app.core.security import get_password_hash


def seed_demo_data():
    """Seeds the local database with an initial demo researcher and test patients if empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        demo_email = settings.DEMO_USER_EMAIL
        demo_password = settings.DEMO_USER_PASSWORD
        demo_user = db.query(User).filter(User.email == demo_email).first()
        if not demo_user:
            demo_user = User(
                email=demo_email,
                hashed_password=get_password_hash(demo_password),
                full_name="Dr. Eleanor Vance, MD PhD",
                role="Principal AI Clinician",
                institution="Quantum Healthcare Discovery Institute",
                is_active=True
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)

            # Add two sample patients for immediate evaluation
            patient_1 = Patient(
                user_id=demo_user.id,
                patient_id="QC-2025-001",
                name="Arthur Pendelton",
                age=58,
                gender="Male",
                symptoms="Persistent dry cough, mild thoracic discomfort for 3 weeks",
                medical_history="Former smoker (15 pack-years), hypertension managed with ACE inhibitors",
                biomarkers={"cea": 3.8, "ldh": 190.0},
                genomics={"egfr_mutation": "negative", "kras": "wild_type"}
            )
            patient_2 = Patient(
                user_id=demo_user.id,
                patient_id="QC-2025-002",
                name="Clara Oswald",
                age=46,
                gender="Female",
                symptoms="Asymptomatic routine screening follow-up",
                medical_history="Family history of breast neoplasm in maternal aunt",
                biomarkers={"ca125": 18.2, "ca15_3": 14.5},
                genomics={"brca1_mutation": False, "brca2_mutation": False}
            )
            db.add_all([patient_1, patient_2])
            db.commit()
            print("Successfully seeded demo researcher and sample patients.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
