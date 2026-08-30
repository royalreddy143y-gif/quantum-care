import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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


def test_register_and_login_success():
    # 1. Register
    reg_payload = {
        "email": "testdoctor@quantumcare.org",
        "password": "SecurePassword123!",
        "full_name": "Dr. Test Clinician",
        "role": "researcher",
        "institution": "University Medical AI Lab"
    }
    reg_resp = client.post("/api/auth/register", json=reg_payload)
    assert reg_resp.status_code == 201
    reg_data = reg_resp.json()
    assert reg_data["email"] == "testdoctor@quantumcare.org"
    assert "hashed_password" not in reg_data

    # 2. Login
    login_payload = {
        "email": "testdoctor@quantumcare.org",
        "password": "SecurePassword123!"
    }
    login_resp = client.post("/api/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_login_invalid_password():
    client.post("/api/auth/register", json={
        "email": "user@test.com",
        "password": "CorrectPassword123!",
        "full_name": "Test User"
    })
    bad_login = client.post("/api/auth/login", json={
        "email": "user@test.com",
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401
