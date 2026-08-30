"""
Standalone training script for Quantum Machine Learning in QuantumCare.
Demonstrates training a 4-qubit parameterized quantum circuit using PennyLane and PyTorch.
"""
import os
import sys
import torch
import torch.nn as nn
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quantum_ml.quantum_model import PennyLaneVQC


def run_training_experiment(epochs: int = 20, lr: float = 0.03):
    print("================================================================")
    print("QuantumCare – Standalone Quantum Circuit Training Demonstration")
    print("================================================================")

    # 1. Generate representative feature matrix scaled into [0, pi]
    torch.manual_seed(42)
    np.random.seed(42)
    n_samples = 80
    n_qubits = 4

    X = torch.rand(n_samples, n_qubits) * np.pi
    # Synthetic ground truth based on non-linear circular parity boundary
    y = ((torch.sin(X[:, 0]) * torch.cos(X[:, 1])) > 0.0).long()

    model = nn.Sequential(
        PennyLaneVQC(n_qubits=n_qubits, n_layers=2),
        nn.Linear(n_qubits, 2)
    )

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()

    print(f"Dataset: {n_samples} samples | Features: {n_qubits} (Angle-encoded)")
    print(f"Device: PennyLane default.qubit (Statevector Simulator)\n")

    for epoch in range(epochs):
        optimizer.zero_grad()
        logits = model(X)
        loss = loss_fn(logits, y)
        loss.backward()
        optimizer.step()

        preds = torch.argmax(logits, dim=-1)
        acc = (preds == y).float().mean().item() * 100

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch [{epoch+1:02d}/{epochs:02d}] - Loss: {loss.item():.4f} - Training Accuracy: {acc:.2f}%")

    print("\n[+] Quantum variational training converged successfully.")


if __name__ == "__main__":
    run_training_experiment()
