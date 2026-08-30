# Quantum Machine Learning (QML) Subsystem

This directory houses the **Variational Quantum Circuit (VQC)** implementation for **QuantumCare**, constructed using **PennyLane** and interfaced natively with **PyTorch**.

---

## 1. Theoretical Architecture

The Quantum Machine Learning pipeline operates as a **Quantum Neural Network (QNN)** layer embedded in our hybrid inference stack:

```
Classical Reduced Features (4D)
            │
            ▼
    [Feature Scaling] (Mapped to [0, π])
            │
            ▼
   [Quantum Angle Embedding] (RY Rotations on Qubits 0-3)
            │
            ▼
 [Variational Parameterized Layers] (Rot(φ, θ, ω) on each qubit)
            │
            ▼
    [Entangling Gates] (Circular Ring Topology CNOT Gates)
            │
            ▼
 [Pauli-Z Observable Measurements] (⟨Z_i⟩ Expectation Values)
            │
            ▼
  Quantum Feature Vector (4D) ──► Classical Hybrid Head
```

### Mathematical Formulation

1. **State Initialization**:
   \[
   |\psi_0\rangle = |0\rangle^{\otimes N}, \quad \text{for } N = 4 \text{ qubits}
   \]

2. **Angle Embedding**:
   Each classical feature \(x_i \in [0, \pi]\) is encoded via a Pauli-Y rotation:
   \[
   U_{\text{embed}}(x) = \bigotimes_{i=0}^{N-1} R_y(x_i)
   \]

3. **Parameterized Variational Unitary**:
   For layer \(l \in \{1, \dots, L\}\):
   \[
   U_{\text{var}}(\boldsymbol{\theta}) = \left( \prod_{i=0}^{N-1} \text{CNOT}_{(i, (i+1) \bmod N)} \right) \left( \bigotimes_{i=0}^{N-1} \text{Rot}(\phi_{l,i}, \theta_{l,i}, \omega_{l,i}) \right)
   \]
   where \(\text{Rot}(\phi, \theta, \omega) = R_z(\omega) R_y(\theta) R_z(\phi)\).

4. **Measurement**:
   We measure the expectation value of the Pauli-Z observable on wire \(i\):
   \[
   \langle Z_i \rangle = \langle \psi | Z_i | \psi \rangle \in [-1.0, 1.0]
   \]

---

## 2. Hardware Simulation & Execution

By default, the platform uses PennyLane's high-speed state-vector simulator:
```python
dev = qml.device("default.qubit", wires=4)
```

To run on an actual quantum processor or Qiskit simulator in the future:
```python
# Install pennylane-qiskit
# pip install pennylane-qiskit qiskit-ibm-runtime

import pennylane as qml
dev = qml.device('qiskit.ibmq', wires=4, backend='ibm_kyoto')
```

---

## 3. Running Standalone Scripts

### Training Variational Parameters
```bash
python train_quantum.py
```

### Circuit Telemetry and Metric Verification
```bash
python evaluate_quantum.py
```

---

## 4. Medical Disclaimer
This quantum simulation is an educational and research implementation demonstrating algorithmic concepts. It does not provide medical diagnoses or replace clinical evaluations.
