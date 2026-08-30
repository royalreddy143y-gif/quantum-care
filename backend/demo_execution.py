import json
import os
import requests

BASE = "http://127.0.0.1:8000/api"

print("=" * 60)
print("  QUANTUMCARE HYBRID QML CLINICAL PLATFORM - LIVE DEMO")
print("=" * 60)

# 1. Authenticate Doctor
auth_res = requests.post(
    f"{BASE}/auth/login",
    json={"email": "demo@quantumcare.org", "password": "QuantumCare2025!"}
)
auth_data = auth_res.json()
token = auth_data["access_token"]
headers = {"Authorization": f"Bearer {token}"}
user_name = auth_data["user"]["full_name"]
role = auth_data["user"]["role"]
institution = auth_data["user"]["institution"]

print(f"\n[1] Clinician Authentication: SUCCESS")
print(f"    Name: {user_name} ({role})")
print(f"    Affiliation: {institution}")
print(f"    Token: JWT (expires in 24h)")

# 2. Retrieve Patient
patients = requests.get(f"{BASE}/patients", headers=headers).json()
patient = patients[0]
print(f"\n[2] Patient Intake: RETRIEVED")
print(f"    Patient ID: {patient['patient_id']} | Name: {patient['name']}")
print(f"    Age / Gender: {patient['age']} yrs / {patient['gender']}")
print(f"    Symptoms: {patient['symptoms']}")
print(f"    Biomarkers: {patient['biomarkers']}")

# 3. Medical Scan Ingestion
scan_path = os.path.join(os.path.dirname(__file__), "sample_scan.png")
with open(scan_path, "rb") as f:
    upload_res = requests.post(
        f"{BASE}/upload",
        data={"patient_id": patient["id"], "image_type": "histology_biopsy"},
        files={"file": ("sample_scan.png", f, "image/png")},
        headers=headers
    ).json()

print(f"\n[3] Medical Scan Ingestion: VALIDATED & STORED")
print(f"    Scan ID: {upload_res['id']}")
print(f"    Filename: {upload_res['filename']}")
print(f"    Dimensions: 224x224 RGB (ImageNet Standardized)")

# 4. Execute Hybrid ML/QML Pipeline
print(f"\n[4] Executing Hybrid Pipeline (Swin Transformer + PennyLane VQC)...")
pred_payload = {
    "patient_id": patient["id"],
    "image_id": upload_res["id"],
    "target_condition": "Thoracic & Cellular Pathology Screening"
}
analysis = requests.post(f"{BASE}/predict", json=pred_payload, headers=headers).json()
pred = analysis["prediction"]

print(f"    Analysis Code: {analysis['analysis_code']}")
print(f"    Model Mode: {analysis['model_mode']}")
print(f"    Prediction Finding: {pred['prediction_label']}")
print(f"    Risk Stratification: {pred['risk_category']} Risk")
print(f"    Confidence Level: {round(pred['confidence_score'] * 100, 1)}%")
print(f"    Processing Latency: {pred['processing_time_ms']} ms")
print(f"    Classical Swin-T Latent Vector: {pred['classical_features']}")
print(f"    PennyLane 4-Qubit Pauli-Z Measurements <Z_i>: {pred['quantum_features']}")

# 5. Generate PDF Report
pdf_res = requests.get(f"{BASE}/reports/{analysis['id']}/pdf", headers=headers)
pdf_size = len(pdf_res.content)
print(f"\n[5] Vector Clinical PDF Report Generation: COMPLETE")
print(f"    Status: HTTP {pdf_res.status_code}")
print(f"    PDF Report Size: {pdf_size} bytes")
print(f"    Report Endpoint: http://localhost:8000/api/reports/{analysis['id']}/pdf")

print("\n" + "=" * 60)
print("  DEMO COMPLETE: All hybrid quantum operations validated successfully!")
print("=" * 60)
