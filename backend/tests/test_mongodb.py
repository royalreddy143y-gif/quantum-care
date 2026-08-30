import pytest
from app.database.mongodb import (
    get_mongo_client,
    get_mongo_db,
    check_mongo_health,
    mongo_upsert_user,
    mongo_save_patient,
    mongo_save_analysis_record
)
from app.core.config import settings


def test_mongo_connection_and_health():
    """Verifies that MongoDB Atlas connects and reports healthy status."""
    if not settings.MONGODB_URI:
        pytest.skip("MONGODB_URI not configured in test environment")

    health = check_mongo_health()
    assert health["status"] == "healthy"
    assert health["connected"] is True
    assert health["database"] == settings.MONGODB_DB_NAME


def test_mongo_data_synchronization():
    """Tests writing and updating documents in MongoDB Atlas."""
    if not settings.MONGODB_URI:
        pytest.skip("MONGODB_URI not configured in test environment")

    # 1. Upsert Test User
    test_user = {
        "email": "automated_test@quantumcare.org",
        "full_name": "Dr. Test Runner",
        "role": "researcher",
        "institution": "Automated Testing Lab",
        "is_active": True
    }
    mongo_upsert_user(test_user)

    # 2. Save Test Patient
    test_patient = {
        "patient_id": "QC-TEST-MONGO-01",
        "name": "Alex Mercer",
        "age": 35,
        "gender": "Non-Binary",
        "symptoms": "Mild fatigue",
        "biomarkers": {"cea": 1.5},
        "genomics": {"brca1": False}
    }
    mongo_save_patient(test_patient)

    # 3. Save Test Analysis
    test_analysis = {
        "analysis_code": "QC-AN-TESTMONGO",
        "patient_id": "QC-TEST-MONGO-01",
        "target_condition": "Oncology Screening",
        "status": "COMPLETED"
    }
    test_prediction = {
        "prediction_label": "Normal / Non-Pathological",
        "confidence_score": 0.94,
        "risk_category": "Low",
        "quantum_features": [0.1, -0.2, 0.3, -0.4]
    }
    mongo_save_analysis_record(test_analysis, test_prediction)

    # Verify document exists in MongoDB Atlas
    db = get_mongo_db()
    assert db is not None
    user_doc = db.users.find_one({"email": "automated_test@quantumcare.org"})
    assert user_doc is not None
    assert user_doc["full_name"] == "Dr. Test Runner"

    analysis_doc = db.analyses.find_one({"analysis_code": "QC-AN-TESTMONGO"})
    assert analysis_doc is not None
    assert analysis_doc["prediction"]["risk_category"] == "Low"
