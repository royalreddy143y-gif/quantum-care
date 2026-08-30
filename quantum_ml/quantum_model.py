"""
Quantum Machine Learning (QML) Module for QuantumCare
Built with PennyLane, supporting default.qubit simulator and future Qiskit backends.
"""
import pennylane as qml
from pennylane.qnn.torch import TorchLayer
import torch
import torch.nn as nn
from typing import List


def create_variational_circuit(n_qubits: int = 4, n_layers: int = 2):
    """
    Constructs a PennyLane QNode executing a Parameterized Variational Quantum Circuit (VQC).
    
    Circuit Anatomy:
    1. Angle Embedding: Maps classical feature components to initial single-qubit RY rotation states.
    2. Variational Layers:
       - Parameterized arbitrary rotations (Rot: phi, theta, omega) on every qubit wire.
       - Ring-entangling CNOT gates for non-local quantum state correlation.
    3. Observable Measurement: Pauli-Z expectation values on each wire, bounded in [-1.0, 1.0].
    """
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev, interface="torch", diff_method="backprop")
    def circuit(inputs, weights):
        # 1. State Encoding
        qml.AngleEmbedding(inputs, wires=range(n_qubits), rotation="Y")

        # 2. Entangling Variational Layers
        for l in range(n_layers):
            for i in range(n_qubits):
                qml.Rot(weights[l, i, 0], weights[l, i, 1], weights[l, i, 2], wires=i)

            # Circular CNOT Entanglement
            for i in range(n_qubits):
                qml.CNOT(wires=[i, (i + 1) % n_qubits])

        # 3. Measurement
        return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

    return circuit


class PennyLaneVQC(nn.Module):
    """PyTorch-compatible Variational Quantum Classifier Layer."""
    def __init__(self, n_qubits: int = 4, n_layers: int = 2):
        super().__init__()
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.qnode = create_variational_circuit(n_qubits, n_layers)
        self.q_layer = TorchLayer(self.qnode, {"weights": (n_layers, n_qubits, 3)})

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.q_layer(x)
