import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.session import Base, get_db

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


def test_forgot_and_reset_password_flow():
    email = "recovery_test@quantumcare.org"
    
    # 1. Register account
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": "OldPassword123!",
        "full_name": "Dr. Recovery Tester",
        "role": "researcher",
        "institution": "Test Lab"
    })
    assert reg_res.status_code == 201

    # 2. Request recovery code
    res_forgot = client.post("/api/auth/forgot-password", json={"email": email})
    assert res_forgot.status_code == 200
    data = res_forgot.json()
    assert "reset_code" in data
    code = data["reset_code"]

    # 3. Reset password with code
    res_reset = client.post("/api/auth/reset-password", json={
        "email": email,
        "reset_code": code,
        "new_password": "NewSecretPassword456!"
    })
    assert res_reset.status_code == 200

    # 4. Verify login with new password
    res_login = client.post("/api/auth/login", json={
        "email": email,
        "password": "NewSecretPassword456!"
    })
    assert res_login.status_code == 200
    assert "access_token" in res_login.json()


def test_update_profile_and_change_password():
    email = "settings_test@quantumcare.org"
    
    # 1. Register and login
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": "InitialPass123!",
        "full_name": "Dr. Setting Initial",
        "role": "researcher",
        "institution": "Initial Hospital"
    })
    assert reg_res.status_code == 201

    res_login = client.post("/api/auth/login", json={
        "email": email,
        "password": "InitialPass123!"
    })
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Update Profile Name and Institution
    res_profile = client.put("/api/auth/profile", json={
        "full_name": "Dr. Setting Updated",
        "institution": "Advanced Quantum Oncology Center"
    }, headers=headers)
    assert res_profile.status_code == 200
    profile_data = res_profile.json()
    assert profile_data["full_name"] == "Dr. Setting Updated"
    assert profile_data["institution"] == "Advanced Quantum Oncology Center"

    # 3. Change Password
    res_change_pwd = client.put("/api/auth/change-password", json={
        "current_password": "InitialPass123!",
        "new_password": "BrandNewSecurePassword789!"
    }, headers=headers)
    assert res_change_pwd.status_code == 200

    # 4. Verify new password login
    res_relogin = client.post("/api/auth/login", json={
        "email": email,
        "password": "BrandNewSecurePassword789!"
    })
    assert res_relogin.status_code == 200
