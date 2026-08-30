# QuantumCare System Architecture & Theoretical Foundations

This document provides a comprehensive technical breakdown of **QuantumCare – Hybrid Quantum Machine Learning Platform for Early Disease Detection**.

---

## 1. High-Level Architecture

```
                                  [Clinician / Doctor Web Browser]
                                                 │
                                                 ▼ (HTTP / JSON / Multi-Part)
                            ┌─────────────────────────────────────────┐
                            │      React 18 + Vite Web Application     │
                            │  Tailwind CSS • Lucide • React Router   │
                            └────────────────────┬────────────────────┘
                                                 │ REST API / Bearer JWT
                                                 ▼
                            ┌─────────────────────────────────────────┐
                            │         FastAPI Backend Engine          │
                            │   Uvicorn • Pydantic v2 • ReportLab     │
                            └─────────┬─────────────────────┬─────────┘
                                      │                     │
                ┌─────────────────────┴──────┐       ┌──────┴──────────────────────┐
                ▼                            ▼       ▼                             ▼
        [SQLAlchemy ORM]            [Media Storage]  [PyTorch Vision Engine] [PennyLane QML]
        PostgreSQL / SQLite         uploads/         Swin Transformer        4-Qubit VQC
        - users                     reports/         768-D Latent Vector     Angle Embedding
        - patients                                          │                Ring CNOT Layers
        - medical_images                                    ▼                      │
        - analyses                                   [Dense Projector]             │
        - predictions                                768-D ──► 4-D ────────────────┤
        - reports                                                                  ▼
                                                                           [Pauli-Z ⟨Z_i⟩]
                                                                                   │
                                                                                   ▼
                                                                        [Hybrid Fusion Layer]
                                                                        8-D Latent ──► Logits
                                                                                   │
                                                                                   ▼
                                                                          [ReportLab PDF]
```

---

## 2. The Hybrid Classical-Quantum Machine Learning Pipeline

### Phase A: Medical Image Ingestion & Standardization
1. **Input Scan**: High-resolution raster scan (Histology, Chest X-ray, Dermoscopy).
2. **Integrity Validation**: Python Imaging Library (PIL) verifies MIME structure and dimensions to prevent arbitrary payload execution.
3. **Preprocessing**:
   \[
   x_{\text{norm}} = \frac{x - \mu}{\sigma}, \quad \mu = [0.485, 0.456, 0.406], \; \sigma = [0.229, 0.224, 0.225]
   \]
   Output shape: \([B, 3, 224, 224]\).

### Phase B: Classical Feature Extraction (Swin Transformer)
1. **Patch Partitioning**: Splits the input into non-overlapping \(4 \times 4\) patches.
2. **Shifted Window Self-Attention**:
   Computes localized multi-head self-attention within local \(M \times M\) windows, with window shifts between layers:
   \[
   \text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{QK^T}{\sqrt{d}} + B\right)V
   \]
   where \(B\) is the learned relative position bias.
3. **Global Representation**: Global average pooling outputs a 768-dimensional latent vector \(h_{\text{swin}} \in \mathbb{R}^{768}\).

### Phase C: Dimensionality Projection & Angular Mapping
Quantum computers with noisy intermediate-scale quantum (NISQ) architectures operate effectively with a modest qubit budget (\(N = 4\)):
\[
z = \text{BatchNorm}(\text{Linear}_{768 \to 4}(h_{\text{swin}})) \in \mathbb{R}^4
\]
The latent vector is bounded into the angular domain \([0, \pi]\) via Sigmoid scaling:
\[
\theta_i = \pi \cdot \sigma(z_i), \quad i \in \{0, 1, 2, 3\}
\]

### Phase D: PennyLane Variational Quantum Circuit (VQC)
1. **Qubit Allocation**: 4 qubits on `default.qubit` simulator initialized to state \(|0000\rangle\).
2. **Angle Embedding**:
   Rotational Pauli-Y unitary encodes classical angular features:
   \[
   |\psi_{\text{enc}}\rangle = \left(\bigotimes_{i=0}^3 R_y(\theta_i)\right) |0000\rangle
   \]
3. **Variational Entangling Layers**:
   For \(L = 2\) layers, parameterized single-qubit arbitrary rotations \(\text{Rot}(\phi, \theta, \omega) = R_z(\omega)R_y(\theta)R_z(\phi)\) and circular ring CNOT gates are applied:
   \[
   U_{\text{layer}}(l) = \left(\prod_{i=0}^3 \text{CNOT}_{(i, (i+1)\%4)}\right) \left(\bigotimes_{i=0}^3 \text{Rot}(\phi_{l,i}, \theta_{l,i}, \omega_{l,i})\right)
   \]
4. **Hermitian Observable Measurement**:
   Computes the expectation value of the Pauli-Z operator for each wire:
   \[
   q_i = \langle \psi | Z_i | \psi \rangle \in [-1.0, 1.0], \quad i \in \{0, 1, 2, 3\}
   \]

### Phase E: Hybrid Fusion & Classification
The classical reduced features \(z\) and quantum expectation features \(q\) are fused:
\[
h_{\text{hybrid}} = [z_0, z_1, z_2, z_3, \; q_0, q_1, q_2, q_3]^T \in \mathbb{R}^8
\]
Optional clinical biomarker embeddings and genomic indicators are concatenated when available. The hybrid vector passes through a linear classification head:
\[
\hat{y} = \text{Softmax}(\text{Linear}_{8 \to 3}(h_{\text{hybrid}}))
\]
Yielding probabilities across classes:
1. *Normal / Non-Pathological*
2. *Early-Stage Suspicious Anomaly*
3. *Elevated Risk Neoplasm*

---

## 3. Medical Safety & Operational Limits

- **Prototype Classification**: Designed exclusively for college coursework, academic seminars, and computational proofs-of-concept.
- **Labeling Standard**: No diagnostic claim is validated by clinical regulatory bodies (FDA, CE, EMA). All user interfaces must show:
  > **"AI Research Prediction – Not a Medical Diagnosis"**
