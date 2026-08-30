# QuantumCare RESTful API Reference

The backend exposes a REST API powered by FastAPI with OpenAPI 3.0 specification. Interactive Swagger UI is hosted at `http://localhost:8000/docs`.

---

## 1. Authentication Endpoints

### `POST /api/auth/register`
Creates a new researcher/doctor account.
- **Request Body**:
  ```json
  {
    "email": "doctor@hospital.org",
    "password": "SecurePassword123!",
    "full_name": "Dr. Sarah Lin, MD",
    "institution": "Oncology Research Center",
    "role": "researcher"
  }
  ```
- **Response `201 Created`**:
  ```json
  {
    "id": 1,
    "email": "doctor@hospital.org",
    "full_name": "Dr. Sarah Lin, MD",
    "institution": "Oncology Research Center",
    "role": "researcher",
    "is_active": true,
    "created_at": "2025-08-27T10:00:00Z"
  }
  ```

### `POST /api/auth/login`
Authenticates researcher and issues JWT bearer token.
- **Request Body**:
  ```json
  {
    "email": "doctor@hospital.org",
    "password": "SecurePassword123!"
  }
  ```
- **Response `200 OK`**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer",
    "user": { ... }
  }
  ```

---

## 2. Patient Management Endpoints

All patient endpoints require `Authorization: Bearer <token>`.

### `POST /api/patients`
Registers a new patient record.
- **Request Body**:
  ```json
  {
    "patient_id": "QC-2025-001",
    "name": "Arthur Pendelton",
    "age": 58,
    "gender": "Male",
    "symptoms": "Persistent dry cough",
    "medical_history": "Former smoker",
    "biomarkers": { "cea": 3.8 },
    "genomics": { "kras": "wild_type" }
  }
  ```

### `GET /api/patients`
Lists accessible patient records.
- **Query Params**: `search` (string), `skip` (int), `limit` (int).

### `GET /api/patients/{patient_id}`
Retrieves a single patient record by database ID.

---

## 3. Medical Scan Ingestion

### `POST /api/upload`
Uploads and validates a medical scan image.
- **Content-Type**: `multipart/form-data`
- **Fields**:
  - `patient_id` (integer)
  - `image_type` (string, e.g. `medical_scan`, `histology`)
  - `file` (binary raster image, JPEG or PNG, max 10MB)
- **Response `201 Created`**:
  ```json
  {
    "id": 4,
    "filename": "scan_slice_01.png",
    "file_path": "/path/to/uploads/uuid_scan_slice_01.png",
    "mime_type": "image/png",
    "file_size": 245120,
    "image_type": "medical_scan",
    "uploaded_at": "2025-08-27T10:15:00Z"
  }
  ```

---

## 4. Hybrid Prediction & Analysis

### `POST /api/predict`
Executes end-to-end hybrid classical-quantum inference pipeline.
- **Request Body**:
  ```json
  {
    "patient_id": 1,
    "image_id": 4,
    "target_condition": "Pulmonary Nodule & Opacity",
    "override_mode": "demo"
  }
  ```
- **Response `200 OK`**:
  ```json
  {
    "id": 12,
    "analysis_code": "QC-AN-A93F12BC",
    "patient_id": 1,
    "image_id": 4,
    "user_id": 1,
    "status": "COMPLETED",
    "model_mode": "DEMO MODEL",
    "target_condition": "Pulmonary Nodule & Opacity",
    "created_at": "2025-08-27T10:16:00Z",
    "prediction": {
      "id": 12,
      "analysis_id": 12,
      "prediction_label": "Early-Stage Suspicious Anomaly",
      "confidence_score": 0.842,
      "risk_category": "Moderate",
      "classical_features": [0.3512, 1.2045, -0.421, 0.8841],
      "quantum_features": [0.6512, -0.214, 0.441, -0.098],
      "processing_time_ms": 142.5,
      "created_at": "2025-08-27T10:16:00Z"
    }
  }
  ```

---

## 5. Reports & System Health

### `GET /api/reports/{analysis_id}/pdf`
Generates and streams the formal ReportLab PDF analysis document.
- **Response**: `application/pdf` binary stream.

### `GET /api/health`
System diagnostic probe returning simulator status and safety notice.
- **Response `200 OK`**:
  ```json
  {
    "status": "online",
    "platform": "QuantumCare",
    "version": "1.0.0-research",
    "model_mode": "demo",
    "quantum_qubits": 4,
    "medical_safety_disclaimer": "AI Research Prediction – Not a Medical Diagnosis"
  }
  ```
