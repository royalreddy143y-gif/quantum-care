import pennylane as qml
from pennylane.qnn.torch import TorchLayer
import torch
import torch.nn as nn
from typing import Tuple, List, Any
from app.core.config import settings


def create_quantum_circuit(n_qubits: int = 4, n_layers: int = 2):
    """
    Creates a PennyLane Variational Quantum Circuit (VQC) using default.qubit simulator.
    """
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev, interface="torch", diff_method="backprop")
    def circuit(inputs, weights):
        """
        inputs: shape [n_qubits] (classical features scaled to [0, pi])
        weights: shape [n_layers, n_qubits, 3] (trainable variational parameters)
        """
        # 1. State Preparation / Quantum Feature Encoding
        qml.AngleEmbedding(inputs, wires=range(n_qubits), rotation="Y")

        # 2. Variational Quantum Layers with Entanglement
        for layer in range(n_layers):
            # Parameterized Single-Qubit Rotations
            for i in range(n_qubits):
                qml.Rot(
                    weights[layer, i, 0],
                    weights[layer, i, 1],
                    weights[layer, i, 2],
                    wires=i
                )

            # Entangling Gates (Ring Topology CNOTs)
            for i in range(n_qubits):
                qml.CNOT(wires=[i, (i + 1) % n_qubits])

        # 3. Measurement: Pauli-Z expectation values on each wire
        return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

    return circuit


class VariationalQuantumClassifier(nn.Module):
    """
    Hybrid PyTorch layer integrating the PennyLane VQC.
    Allows forward evaluation and classical gradient optimization.
    """
    def __init__(self, n_qubits: int = 4, n_layers: int = 2):
        super().__init__()
        self.n_qubits = n_qubits
        self.n_layers = n_layers

        # Build circuit
        self.circuit = create_quantum_circuit(n_qubits, n_layers)
        weight_shapes = {"weights": (n_layers, n_qubits, 3)}

        # Wrap into PyTorch TorchLayer
        self.q_layer = TorchLayer(self.circuit, weight_shapes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: [B, n_qubits]
        returns: [B, n_qubits] quantum expectation values
        """
        return self.q_layer(x)
