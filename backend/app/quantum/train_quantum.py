"""
Standalone training script for the PennyLane Variational Quantum Circuit (VQC).
Demonstrates variational parameter optimization using PyTorch and Adam optimizer.
"""
import torch
import torch.nn as nn
import pennylane as qml
import numpy as np
from app.quantum.quantum_model import VariationalQuantumClassifier


def generate_synthetic_quantum_data(n_samples: int = 100, n_qubits: int = 4):
    """Generates synthetic normalized medical latent features and binary labels."""
    X = torch.rand(n_samples, n_qubits) * np.pi  # Angles in [0, pi]
    # Simple non-linear separation boundary for quantum kernel demonstration
    y = (torch.sin(X[:, 0]) + torch.cos(X[:, 1]) > 0.5).long()
    return X, y


def train_vqc(epochs: int = 15, lr: float = 0.05, n_qubits: int = 4, n_layers: int = 2):
    print("=========================================================")
    print("QuantumCare – PennyLane Variational Quantum Training Demo")
    print(f"Qubits: {n_qubits} | Variational Layers: {n_layers} | Epochs: {epochs}")
    print("=========================================================")

    X, y = generate_synthetic_quantum_data(n_samples=60, n_qubits=n_qubits)

    vqc = VariationalQuantumClassifier(n_qubits=n_qubits, n_layers=n_layers)
    post_classifier = nn.Linear(n_qubits, 2)
    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        list(vqc.parameters()) + list(post_classifier.parameters()),
        lr=lr
    )

    for epoch in range(epochs):
        optimizer.zero_grad()
        # Quantum forward pass
        q_exp = vqc(X)
        logits = post_classifier(q_exp)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()

        preds = torch.argmax(logits, dim=-1)
        acc = (preds == y).float().mean().item() * 100

        print(f"Epoch [{epoch+1:02d}/{epochs:02d}] Loss: {loss.item():.4f} | Accuracy: {acc:.1f}%")

    print("\n[+] Quantum Variational Optimization complete.")


if __name__ == "__main__":
    train_vqc()
