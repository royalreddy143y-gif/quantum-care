import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_db

from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def get_authenticated_header():
    client.post("/api/auth/register", json={
        "email": "doc@quantumcare.org",
        "password": "Password123!",
        "full_name": "Dr. Patient Tester"
    })
    login_resp = client.post("/api/auth/login", json={
        "email": "doc@quantumcare.org",
        "password": "Password123!"
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_retrieve_patient():
    headers = get_authenticated_header()

    # 1. Create Patient
    payload = {
        "patient_id": "QC-TEST-001",
        "name": "Jane Doe",
        "age": 42,
        "gender": "Female",
        "symptoms": "Mild persistent headache",
        "medical_history": "No major chronic conditions",
        "biomarkers": {"cea": 2.1},
        "genomics": {"brca1_mutation": False}
    }
    create_resp = client.post("/api/patients", json=payload, headers=headers)
    assert create_resp.status_code == 201
    created_patient = create_resp.json()
    assert created_patient["patient_id"] == "QC-TEST-001"
    p_id = created_patient["id"]

    # 2. Retrieve Patient List
    list_resp = client.get("/api/patients", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # 3. Retrieve Specific Patient
    get_resp = client.get(f"/api/patients/{p_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Jane Doe"
