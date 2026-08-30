# QuantumCare – Hybrid Quantum Machine Learning Platform for Early Disease Detection

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/frontend-React%2018%20%2B%20Vite-61dafb.svg)](https://react.dev)
[![PennyLane](https://img.shields.io/badge/quantum-PennyLane-purple.svg)](https://pennylane.ai)
[![PyTorch](https://img.shields.io/badge/ML-PyTorch%20%2B%20Swin-ee4c2c.svg)](https://pytorch.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Tagline:** *"Quantum Intelligence for Early Disease Detection"*

---

## 1. Project Description

**QuantumCare** is a full-stack educational and academic research prototype demonstrating how **Classical Deep Learning (Swin Transformer)** and **Quantum Machine Learning (PennyLane Variational Quantum Circuits)** can be combined for early pathology anomaly detection.

The platform provides an end-to-end clinical research workflow:
1. Secure researcher and clinician registration/authentication.
2. Patient registry with demographic, medical history, optional serum biomarker, and genomic profiling data.
3. Secure medical scan upload with raster image format and integrity validation.
4. Classical visual feature extraction via a **Swin Transformer** backbone (768-D).
5. Dimensionality reduction projecting latent visual vectors into 4 angular feature channels.
6. Quantum state preparation (Angle Embedding) and variational layer execution on a **4-Qubit PennyLane Variational Quantum Circuit (VQC)** with circular CNOT entanglement.
7. Observable Pauli-Z expectation value measurement \(\langle Z_i \rangle\).
8. Hybrid classical-quantum decision layer producing risk stratification (Low / Moderate / High) and confidence metrics.
9. Interactive web visualizer tracking each phase of execution.
10. Automatic generation of formatted, downloadable **ReportLab PDF research reports**.

---

## 2. Mandatory Medical Safety Disclaimer

> [!CAUTION]
> ### AI Research Prediction – Not a Medical Diagnosis
> QuantumCare is an **academic, educational, and computational research prototype**. It is **NOT** a certified medical diagnostic device, clinical software, or FDA/CE-approved platform.
> - Never use predictions or probability scores from this system for real-world clinical decision-making, diagnosis, or patient care.
> - The software makes no claim of clinical accuracy, medical efficacy, or guaranteed patient outcomes.
> - Real trained clinical models require formal institutional IRB oversight, clinical trials, and regulatory validation before any clinical deployment.

---

## 3. High-Level Architecture

```
                    QUANTUMCARE PLATFORM
                             │
                             ▼
               React + Vite Frontend Web App
        (Dashboard, Directory, Interactive Pipeline)
                             │
                             ▼ (REST API / JWT)
                   FastAPI Python Backend
                 (Auth, Pipeline, DB, Reports)
                 ┌───────────┴───────────┐
                 ▼                       ▼
      PostgreSQL / SQLite DB    Hybrid QML Pipeline
      (Users, Patients,         ┌────────┴────────┐
       Images, Analyses)        ▼                 ▼
                          Classical ML       Quantum ML
                        (Swin Transformer)  (PennyLane VQC)
                                └────────┬────────┘
                                         ▼
                               Feature Fusion Layer
                                         │
                                         ▼
                               Hybrid Prediction
                                         │
                                         ▼
                               PDF Report Generator
                                   (ReportLab)
```

---

## 4. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS, React Router DOM, Lucide Icons, Axios |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy, Alembic |
| **Database** | PostgreSQL (Production) / SQLite (Development automatic fallback) |
| **Classical ML** | PyTorch, torchvision (Swin Transformer), NumPy, Pandas, scikit-learn, Pillow |
| **Quantum ML** | PennyLane, `default.qubit` simulator, AngleEmbedding, Parameterized Rotations, Ring CNOTs |
| **Reports** | ReportLab (Vector PDF Generation with table layout and disclaimers) |
| **Testing** | Pytest, FastAPI TestClient, httpx |

---

## 5. Project Directory Structure

```
QuantumCare/
├── backend/
│   ├── app/
│   │   ├── api/             # REST route handlers (auth, patients, upload, predict, reports, health)
│   │   ├── core/            # Config settings and JWT security
│   │   ├── database/        # SQLAlchemy engine and session
│   │   ├── models/          # ORM models (User, Patient, Image, Analysis, Prediction, Report)
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── ml/              # Classical Swin-T model, preprocessing, feature extractor, hybrid model
│   │   ├── quantum/         # PennyLane VQC circuit, feature scaling, telemetry
│   │   ├── reports/         # ReportLab PDF generator
│   │   └── utils/           # Database seeding & helpers
│   ├── tests/               # Pytest suite
│   ├── alembic/             # Migration scripts
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI (Navbar, Sidebar, Card, Button, Modal, ImageUploader)
│   │   ├── context/         # AuthContext with token state
│   │   ├── layouts/         # DashboardLayout
│   │   ├── pages/           # Landing, Login, Register, Dashboard, Patients, Upload, Result, History, Report
│   │   ├── services/        # Axios API clients
│   │   └── utils/           # Medical disclaimer constants
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── ml_model/
│   ├── preprocessing/       # Augmentation transforms
│   ├── training/            # PyTorch training script with train/val/test split
│   ├── evaluation/          # Precision, Recall, F1, Confusion Matrix, ROC-AUC
│   ├── saved_models/        # Model checkpoint weights
│   └── README.md
│
├── quantum_ml/
│   ├── quantum_model.py     # Standalone PennyLane VQC circuit definition
│   ├── train_quantum.py     # Standalone variational training convergence demo
│   ├── evaluate_quantum.py  # Quantum circuit state auditor
│   └── README.md
│
├── dataset/
│   └── README.md            # Benchmark dataset guide (MedMNIST, ISIC, CBIS-DDSM) and licenses
│
├── docs/
│   ├── architecture.md      # Comprehensive architecture and mathematical formulation
│   ├── api.md               # OpenAPI endpoint contracts
│   └── setup.md             # Detailed platform installation instructions
│
├── .env.example
├── .gitignore
└── README.md
```

---

## 6. Environment Variables (`.env.example`)

```env
# Application Environment
ENVIRONMENT=development

# Database (PostgreSQL or SQLite fallback)
DATABASE_URL=sqlite:///./quantumcare.db

# JWT Security
SECRET_KEY=supersecretkey_change_in_production_min_32_bytes_long_12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Model Execution Mode: 'demo' (educational simulation) or 'research' (live PyTorch forward pass)
MODEL_MODE=demo

# Storage & Upload Limits
UPLOAD_DIR=./uploads
REPORTS_DIR=./generated_reports
MAX_UPLOAD_SIZE=10485760

# Quantum ML Configuration
QUANTUM_NUM_QUBITS=4
QUANTUM_NUM_LAYERS=2
```

---

## 7. Installation & Quickstart

### Step 1: Clone and Set Up Backend
```bash
cd backend
python -m venv .venv

# Activate virtual environment:
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies:
pip install -r requirements.txt

# Seed demo doctor and sample patients:
python -m app.utils.seed_data

# Start FastAPI server:
uvicorn app.main:app --reload --port 8000
```
Interactive API documentation will be live at `http://localhost:8000/docs`.

### Step 2: Set Up Frontend
Open a separate terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 8. Evaluation Credentials

For rapid grading and demonstration:
- **Email:** `demo@quantumcare.org`
- **Password:** `QuantumCare2025!`
*(You can also simply click the purple **"Autofill & Login"** button on the Login page to authenticate immediately)*.

---

## 9. Machine Learning & Quantum Workflows

### Running Standalone Quantum Circuit Training
```bash
python quantum_ml/train_quantum.py
```

### Auditing Quantum Expectation Measurements
```bash
python quantum_ml/evaluate_quantum.py
```

### Training the Hybrid Classical-Quantum Model
```bash
python ml_model/training/train.py --epochs 5 --batch_size 8
```

---

## 10. Automated Testing

Run the comprehensive Pytest test suite:
```bash
cd backend
pytest tests/ -v
```
Tests validate:
- Authentication & JWT token security
- Patient record creation and retrieval
- Image upload validation (MIME, size, integrity)
- Swin Transformer feature extraction
- PennyLane 4-qubit VQC execution and measurement bounds \([-1, 1]\)

---

## 11. Limitations & Future Enhancements

### Current Prototype Limitations
1. **Simulator Execution**: Quantum circuits currently execute on PennyLane's `default.qubit` statevector simulator rather than cryogenic quantum processing units (QPUs).
2. **Qubit Capacity**: Classical features are reduced to 4 dimensions to run smoothly on standard laptops without exponential statevector memory scaling.
3. **Pre-Clinical Status**: No clinical validation has been performed.

### Future Enhancements
- **Qiskit / IBM Quantum Hardware Integration**: Connecting PennyLane to cloud quantum backends (`qiskit.ibmq`).
- **Federated Quantum Learning**: Multi-hospital privacy-preserving training without sharing raw patient scans.
- **Automated Biomarker / Genomic Panel Sequencing**: Full multi-omics attention fusion across blood biomarkers (CA-125, PSA, CEA) and genomic mutations (BRCA1/2, EGFR).
- **Explainable AI (XAI)**: Grad-CAM visual heatmaps overlaying Swin Transformer attention windows on medical scans.

---

## 12. License & Acknowledgements
- Distributed under the MIT License.
- Designed as an advanced full-stack college project in Hybrid Quantum-Classical Artificial Intelligence.
