import math
import torch
import numpy as np
from typing import List, Dict, Any


def scale_features_for_quantum(features: torch.Tensor, target_min: float = 0.0, target_max: float = math.pi) -> torch.Tensor:
    """
    Scales a feature vector into the angular interval [0, pi]
    suitable for Pauli-Y and Pauli-X rotation gates without phase ambiguity.
    """
    # Use Sigmoid or MinMax scaling
    scaled = torch.sigmoid(features) * (target_max - target_min) + target_min
    return scaled


def calculate_quantum_metrics(expectation_values: List[float]) -> Dict[str, Any]:
    """
    Computes statistical and quantum information metrics from qubit Pauli-Z expectation values.
    """
    values = np.array(expectation_values, dtype=float)
    mean_polarization = float(np.mean(values))
    std_dispersion = float(np.std(values))
    # Simulated entanglement measure / purity proxy
    purity_proxy = float(np.mean(values ** 2))

    return {
        "mean_polarization": round(mean_polarization, 4),
        "dispersion": round(std_dispersion, 4),
        "purity_proxy": round(purity_proxy, 4),
        "active_qubits": len(values)
    }
