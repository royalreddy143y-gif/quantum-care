# QuantumCare – React & Vite Frontend Application

A healthcare technology web platform built with React, Vite, and Tailwind CSS for hybrid classical-quantum medical image analysis.

---

## 1. Setup & Installation

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Configure environment (optional, defaults to `http://localhost:8000/api`):
   Create `.env`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

3. Launch development server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

---

## 2. Key Pages & Features

- **Landing Page (`/`)**: Hero banner, clinical challenges, Swin Transformer & PennyLane VQC explanation, interactive 8-step workflow, and prominent disclaimers.
- **Authentication (`/login`, `/register`)**: JWT authentication, validation, and a **1-click "Autofill & Login"** demo doctor button.
- **Dashboard (`/dashboard`)**: Metric cards, active simulator status, recent analyses, quick actions.
- **Patient Management (`/patients`, `/patients/:id`)**: Searchable directory, detailed profiles, clinical history, and optional multi-omics panels.
- **New Analysis (`/analyses/new`)**: Drag-and-drop scan uploader with client-side image preview and format validation, plus a **"Load Sample Histology Scan"** button for immediate testing without finding an external file.
- **Interactive Pipeline Runner (`/analyses/process`)**: Visual 5-stage progress stepper tracking preprocessing, Swin-T feature extraction, PennyLane VQC execution, and hybrid classification.
- **Analysis Result (`/analyses/:id/result`)**: Risk categorization, confidence gauges, 4-qubit Pauli-Z measurement telemetry, and direct PDF download.
- **Audit History (`/history`)**: Filterable audit trail of previous evaluations.
- **Printable Report (`/analyses/:id/report`)**: Formatted clinical research report with built-in print styling and PDF download.
- **Technology Guide (`/technology`)**: Pedagogical breakdown of Swin Transformer attention windows and quantum Hilbert-space statevectors.

---

## 3. Medical Safety Mandate
Every diagnostic prediction page and report view displays the non-negotiable safety notice:
> **"AI Research Prediction – Not a Medical Diagnosis"**
