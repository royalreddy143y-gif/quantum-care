# QuantumCare Setup & Installation Guide

This guide covers setting up **QuantumCare** for local development, evaluation, and grading.

---

## 1. Prerequisites

- **Python**: Version 3.10 or 3.11+
- **Node.js**: Version 18.x or 20.x+
- **npm** or **yarn**
- **Git**
- *(Optional)* **PostgreSQL 14+** (If omitted, system automatically falls back to built-in SQLite `quantumcare.db` so you can test immediately).

---

## 2. Backend Setup

1. Open terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   # Windows (PowerShell):
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS / Linux:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   Copy `.env.example` to `.env`:
   ```bash
   # Windows:
   copy ..\.env.example .env

   # macOS / Linux:
   cp ../.env.example .env
   ```

5. Seed demo account & sample clinical records:
   ```bash
   python -m app.utils.seed_data
   ```
   *Creates default login:*
   - **Email:** `demo@quantumcare.org`
   - **Password:** `QuantumCare2025!`

6. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Verify at `http://localhost:8000/docs`.

---

## 3. PostgreSQL Configuration (Optional)

If you wish to run on a local or cloud PostgreSQL instance:
1. Create a database:
   ```sql
   CREATE DATABASE quantumcare_db;
   ```
2. Update `.env` in the backend root:
   ```env
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/quantumcare_db
   ```
3. Run migrations:
   ```bash
   alembic upgrade head
   ```

---

## 4. Frontend Setup

1. Open a new terminal window and navigate to `frontend`:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Access the web application at:
   ```
   http://localhost:5173
   ```

---

## 5. Running the Complete Evaluation Flow

1. Open `http://localhost:5173`.
2. Click **"Get Started"** or **"Sign In"**.
3. Click the purple **"Autofill & Login"** button to log in as Dr. Eleanor Vance instantly.
4. On the Dashboard, click **"New Analysis"**.
5. Select a patient (e.g. *Arthur Pendelton*).
6. Click **"Load Sample Histology Scan"** (or drag and drop your own scan).
7. Click **"Launch Hybrid Quantum Pipeline"**.
8. Observe the 5-phase visual pipeline:
   - Preparing scan
   - Swin Transformer feature extraction
   - Feature reduction
   - PennyLane 4-qubit VQC execution
   - Result calculation
9. On the Result page, view:
   - Prediction & confidence
   - Prominent notice: *"AI Research Prediction – Not a Medical Diagnosis"*
   - Model mode badge (*"DEMO MODEL"*)
   - Quantum Telemetry (*⟨Z_i⟩ expectation measurements for 4 qubits*)
10. Click **"Download PDF"** to receive the official ReportLab generated report.
11. View previous runs in **"Analyses History"**.

---

## 6. Running Automated Tests

```bash
cd backend
pytest tests/ -v
```
All unit and integration tests (auth, patient CRUD, PennyLane VQC, Swin Transformer forward pass) will execute and report status.
