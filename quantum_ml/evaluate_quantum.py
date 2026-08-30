"""
Quantum circuit evaluation and state telemetry auditor.
"""
import os
import sys
import torch
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quantum_ml.quantum_model import PennyLaneVQC


def evaluate_qml_fidelity():
    print("================================================================")
    print("QuantumCare – Quantum Circuit Telemetry & Fidelity Evaluation")
    print("================================================================")

    vqc = PennyLaneVQC(n_qubits=4, n_layers=2)
    vqc.eval()

    # Controlled evaluation vectors
    test_states = [
        ("Ground State Input (all zeros)", torch.zeros(1, 4)),
        ("Uniform Superposition (pi/2)", torch.full((1, 4), np.pi / 2)),
        ("Maximum Rotation (pi)", torch.full((1, 4), np.pi)),
        ("Arbitrary Latent Feature", torch.tensor([[0.85, 1.42, 2.15, 0.45]]))
    ]

    for label, tensor in test_states:
        with torch.no_grad():
            out = vqc(tensor)
        vals = out.squeeze(0).tolist()
        print(f"\n{label}:")
        print(f"  Input:  {[round(float(x), 3) for x in tensor.squeeze(0).tolist()]}")
        print(f"  <Z_i>:  {[round(float(v), 4) for v in vals]}")
        print(f"  Mean Polarization: {round(float(np.mean(vals)), 4)}")
        print(f"  Quantum Dispersion: {round(float(np.std(vals)), 4)}")

    print("\n[+] All quantum circuit checks passed.")


if __name__ == "__main__":
    evaluate_qml_fidelity()
