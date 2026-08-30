# QuantumCare – FastAPI Backend Service

This service provides the RESTful API, authentication, database persistence, ReportLab PDF generation, and the hybrid Swin Transformer + PennyLane Quantum ML inference engine.

---

## 1. Setup & Installation

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   Copy `.env.example` in project root to `.env` or set environment variables:
   ```bash
   MODEL_MODE=demo
   DATABASE_URL=sqlite:///./quantumcare.db
   ```

4. Seed initial demo doctor account and sample patients:
   ```bash
   python -m app.utils.seed_data
   ```

5. Launch development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

Interactive Swagger API docs are accessible at: `http://localhost:8000/docs`

---

## 2. API Endpoints

- **Auth**: `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`
- **Patients**: `GET /api/patients`, `POST /api/patients`, `GET /api/patients/{id}`, `PUT /api/patients/{id}`, `DELETE /api/patients/{id}`
- **Medical Scans**: `POST /api/upload` (Supports JPEG/PNG with integrity check)
- **Analyses**: `GET /api/analyses`, `POST /api/analyses`, `GET /api/analyses/{id}`
- **Inference**: `POST /api/predict` (Executes Hybrid Classical-Quantum Pipeline)
- **Reports**: `GET /api/reports/{id}/pdf` (Direct PDF stream download)
- **Health**: `GET /api/health`

---

## 3. Running Backend Tests

```bash
pytest tests/ -v
```
