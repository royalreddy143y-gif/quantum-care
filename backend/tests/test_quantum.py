import pytest
import torch
import numpy as np
from app.quantum.quantum_model import VariationalQuantumClassifier
from app.quantum.quantum_features import scale_features_for_quantum, calculate_quantum_metrics


def test_quantum_circuit_execution():
    n_qubits = 4
    n_layers = 2
    vqc = VariationalQuantumClassifier(n_qubits=n_qubits, n_layers=n_layers)
    vqc.eval()

    # Input tensor of 2 batches with 4 classical features
    dummy_input = torch.tensor([
        [0.1, 0.5, 1.2, 2.5],
        [2.1, 1.8, 0.4, 0.9]
    ], dtype=torch.float32)

    with torch.no_grad():
        output = vqc(dummy_input)

    # Verify tensor shape
    assert output.shape == (2, n_qubits)

    # Verify expectation values are within physical bounds [-1.0, 1.0]
    out_list = output.tolist()
    for row in out_list:
        for val in row:
            assert -1.0 <= val <= 1.0


def test_quantum_feature_scaling():
    features = torch.tensor([-5.0, 0.0, 5.0])
    scaled = scale_features_for_quantum(features, target_min=0.0, target_max=np.pi)

    # Values must be within [0, pi]
    assert torch.all(scaled >= 0.0)
    assert torch.all(scaled <= np.pi)


def test_quantum_metrics_calculation():
    expectations = [0.85, -0.42, 0.12, -0.10]
    metrics = calculate_quantum_metrics(expectations)

    assert "mean_polarization" in metrics
    assert "dispersion" in metrics
    assert "purity_proxy" in metrics
    assert metrics["active_qubits"] == 4
